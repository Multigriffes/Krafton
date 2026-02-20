"""Tests unitaires pour cameras/fonctions_images.py.

Le répertoire cameras/ est ajouté au sys.path dans conftest.py,
ce qui permet les imports directs utilisés par ces scripts.
"""

import math

import numpy as np
import pytest

from fonctions_images import (
    build_v_ij,
    compute_homography,
    groupe_leds,
    rotation_matrix_x,
    triangulate_parallel,
)


# ---------------------------------------------------------------------------
# rotation_matrix_x
# ---------------------------------------------------------------------------


class TestRotationMatrixX:
    def test_angle_zero_is_identity(self):
        R = rotation_matrix_x(0.0)
        assert R == pytest.approx(np.eye(3))

    def test_angle_pi_half(self):
        R = rotation_matrix_x(math.pi / 2)
        expected = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=float)
        assert R == pytest.approx(expected, abs=1e-10)

    def test_angle_pi(self):
        R = rotation_matrix_x(math.pi)
        expected = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=float)
        assert R == pytest.approx(expected, abs=1e-10)

    def test_is_orthogonal(self):
        R = rotation_matrix_x(0.7)
        assert R.T @ R == pytest.approx(np.eye(3), abs=1e-10)

    def test_determinant_is_one(self):
        R = rotation_matrix_x(1.2)
        assert np.linalg.det(R) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# triangulate_parallel
# ---------------------------------------------------------------------------


class TestTriangulateParallel:
    # K = (f, cx, cy), B = baseline
    K = (100.0, 320.0, 240.0)
    B = 0.1

    def test_zero_disparity_returns_none(self):
        result = triangulate_parallel((300, 240), (300, 240), self.K, self.B)
        assert result is None

    def test_known_depth(self):
        # disparity = 10 → Z = 100 * 0.1 / 10 = 1.0
        # X = 1.0 * (330 - 320) / 100 = 0.1
        # Y = 1.0 * (240 - 240) / 100 = 0.0
        result = triangulate_parallel((330, 240), (320, 240), self.K, self.B)
        assert result is not None
        X, Y, Z = result
        assert Z == pytest.approx(1.0)
        assert X == pytest.approx(0.1)
        assert Y == pytest.approx(0.0)

    def test_depth_inversely_proportional_to_disparity(self):
        # Double la disparité → moitié de la profondeur
        r1 = triangulate_parallel((330, 240), (320, 240), self.K, self.B)
        r2 = triangulate_parallel((340, 240), (320, 240), self.K, self.B)
        assert r1[2] == pytest.approx(r2[2] * 2, rel=1e-6)

    def test_negative_disparity(self):
        # Disparité négative → profondeur négative (hors plan)
        result = triangulate_parallel((310, 240), (320, 240), self.K, self.B)
        assert result is not None
        assert result[2] < 0


# ---------------------------------------------------------------------------
# groupe_leds  (distance_max = 50 px défini dans parameters.py)
# ---------------------------------------------------------------------------


class TestGroupeLeds:
    def test_empty_list(self):
        assert groupe_leds([]) == []

    def test_single_point(self):
        result = groupe_leds([(0.0, 0.0)])
        assert result == [[(0.0, 0.0)]]

    def test_two_close_points_same_cluster(self):
        # distance = 10 < 50 → un seul cluster
        result = groupe_leds([(0.0, 0.0), (10.0, 0.0)])
        assert len(result) == 1
        assert len(result[0]) == 2

    def test_two_far_points_different_clusters(self):
        # distance = 100 > 50 → deux clusters
        result = groupe_leds([(0.0, 0.0), (100.0, 0.0)])
        assert len(result) == 2

    def test_all_points_in_cluster_are_present(self):
        pts = [(0.0, 0.0), (10.0, 0.0), (20.0, 0.0)]
        result = groupe_leds(pts)
        assert len(result) == 1
        assert len(result[0]) == 3

    def test_two_separated_clusters(self):
        # Deux groupes séparés de 200 px
        close = [(0.0, 0.0), (10.0, 0.0), (20.0, 0.0)]
        far = [(200.0, 0.0), (210.0, 0.0)]
        result = groupe_leds(close + far)
        assert len(result) == 2
        sizes = sorted(len(g) for g in result)
        assert sizes == [2, 3]

    def test_boundary_distance_excluded(self):
        # distance exactement = distance_max (50) → hors cluster (< strict)
        result = groupe_leds([(0.0, 0.0), (50.0, 0.0)])
        assert len(result) == 2

    def test_boundary_distance_included(self):
        # distance légèrement < 50 → même cluster
        result = groupe_leds([(0.0, 0.0), (49.9, 0.0)])
        assert len(result) == 1


# ---------------------------------------------------------------------------
# build_v_ij
# ---------------------------------------------------------------------------


class TestBuildVij:
    def test_shape(self):
        H = np.eye(3)
        v = build_v_ij(H, 0, 1)
        assert v.shape == (6,)

    def test_identity_v01(self):
        # H = I, i=0, j=1 → [0, 1, 0, 0, 0, 0]
        H = np.eye(3)
        v = build_v_ij(H, 0, 1)
        expected = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
        assert v == pytest.approx(expected)

    def test_identity_v00(self):
        # H = I, i=0, j=0 → [1, 0, 0, 0, 0, 0]
        H = np.eye(3)
        v = build_v_ij(H, 0, 0)
        expected = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        assert v == pytest.approx(expected)

    def test_identity_v11(self):
        # H = I, i=1, j=1 → [0, 0, 1, 0, 0, 0]
        H = np.eye(3)
        v = build_v_ij(H, 1, 1)
        expected = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        assert v == pytest.approx(expected)

    def test_symmetry(self):
        # v_ij = v_ji
        H = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
        assert build_v_ij(H, 0, 1) == pytest.approx(build_v_ij(H, 1, 0))


# ---------------------------------------------------------------------------
# compute_homography
# ---------------------------------------------------------------------------


class TestComputeHomography:
    def test_identity_mapping(self):
        # Points vers eux-mêmes → H ≈ identité (normalisée)
        pts = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=float)
        H = compute_homography(pts, pts)
        for pt in pts:
            p = np.array([pt[0], pt[1], 1.0])
            mapped = H @ p
            mapped /= mapped[2]
            assert mapped[0] == pytest.approx(pt[0], abs=1e-6)
            assert mapped[1] == pytest.approx(pt[1], abs=1e-6)

    def test_translation(self):
        obj_pts = np.array(
            [[0, 0], [1, 0], [0, 1], [1, 1], [2, 1]], dtype=float
        )
        tx, ty = 5.0, 3.0
        img_pts = obj_pts + np.array([tx, ty])
        H = compute_homography(obj_pts, img_pts)
        for obj_pt, img_pt in zip(obj_pts, img_pts):
            p = np.array([obj_pt[0], obj_pt[1], 1.0])
            mapped = H @ p
            mapped /= mapped[2]
            assert mapped[0] == pytest.approx(img_pt[0], abs=1e-5)
            assert mapped[1] == pytest.approx(img_pt[1], abs=1e-5)

    def test_output_shape(self):
        pts = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=float)
        H = compute_homography(pts, pts)
        assert H.shape == (3, 3)

    def test_normalized_h22(self):
        # H[2,2] doit être 1 (normalisé)
        pts = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=float)
        img_pts = pts * 2.0
        H = compute_homography(pts, img_pts)
        assert H[2, 2] == pytest.approx(1.0)
