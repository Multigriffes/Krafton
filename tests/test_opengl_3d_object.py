"""Tests unitaires pour engine/opengl_3d_object.py.

On teste uniquement les méthodes qui n'appellent pas l'API OpenGL :
  - OBJECT_BASE : addCoordinates, addRotation
  - CAMERA : init, déplacements (forward/backward/…), rotations (yaw/pitch/roll), reset

Les méthodes compile() et draw() nécessitent un contexte OpenGL actif
et ne sont pas testées ici.
"""

import math
import pytest

from engine.opengl_3d_object import CAMERA, OBJECT_BASE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def axes_are_orthonormal(cam: CAMERA, tol: float = 1e-9) -> bool:
    """Vérifie que front, up et right sont unitaires et mutuellement orthogonaux."""
    front = cam.front
    up = cam.up
    right = cam.right

    def length(q):
        return math.sqrt(q.x**2 + q.y**2 + q.z**2)

    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    return (
        abs(length(front) - 1.0) < tol
        and abs(length(up) - 1.0) < tol
        and abs(length(right) - 1.0) < tol
        and abs(dot(front, up)) < tol
        and abs(dot(front, right)) < tol
        and abs(dot(up, right)) < tol
    )


# ---------------------------------------------------------------------------
# OBJECT_BASE
# ---------------------------------------------------------------------------


class TestObjectBase:
    def make(self, coords=None, rotation=None):
        return OBJECT_BASE(
            coordinates=coords if coords is not None else [0, 0, 0],
            rotation=rotation if rotation is not None else [0, 0, 0],
        )

    # --- addCoordinates ---

    def test_add_coordinates_updates_position(self):
        obj = self.make()
        obj.addCoordinates([1, 2, 3])
        assert obj.coordinates == [1, 2, 3]

    def test_add_coordinates_accumulates(self):
        obj = self.make()
        obj.addCoordinates([1, 0, 0])
        obj.addCoordinates([1, 0, 0])
        assert obj.coordinates[0] == pytest.approx(2.0)

    def test_add_coordinates_none_is_noop(self):
        obj = self.make()
        obj.addCoordinates(None)
        assert obj.coordinates == [0, 0, 0]

    def test_add_coordinates_negative(self):
        obj = self.make(coords=[5, 5, 5])
        obj.addCoordinates([-5, -5, -5])
        assert obj.coordinates == [0, 0, 0]

    # --- addRotation ---

    def test_add_rotation_updates_angles(self):
        obj = self.make()
        obj.addRotation([30, 0, 0])
        assert obj.rotation == [30, 0, 0]

    def test_add_rotation_accumulates(self):
        obj = self.make()
        obj.addRotation([10, 20, 30])
        obj.addRotation([10, 20, 30])
        assert obj.rotation == [20, 40, 60]

    def test_add_rotation_none_is_noop(self):
        obj = self.make()
        obj.addRotation(None)
        assert obj.rotation == [0, 0, 0]


# ---------------------------------------------------------------------------
# CAMERA — état initial
# ---------------------------------------------------------------------------


class TestCameraInit:
    def test_default_coordinates(self):
        cam = CAMERA()
        assert cam.coordinates == [0, 0, 0]

    def test_default_speed(self):
        cam = CAMERA()
        assert cam.speed == pytest.approx(0.05)

    def test_custom_speed(self):
        cam = CAMERA(speed=0.2)
        assert cam.speed == pytest.approx(0.2)

    def test_default_front(self):
        cam = CAMERA()
        assert cam.front.x == pytest.approx(0.0)
        assert cam.front.y == pytest.approx(0.0)
        assert cam.front.z == pytest.approx(-1.0)

    def test_default_up(self):
        cam = CAMERA()
        assert cam.up.x == pytest.approx(0.0)
        assert cam.up.y == pytest.approx(1.0)
        assert cam.up.z == pytest.approx(0.0)

    def test_default_right(self):
        cam = CAMERA()
        assert cam.right.x == pytest.approx(1.0)
        assert cam.right.y == pytest.approx(0.0)
        assert cam.right.z == pytest.approx(0.0)

    def test_initial_axes_are_orthonormal(self):
        assert axes_are_orthonormal(CAMERA())


# ---------------------------------------------------------------------------
# CAMERA — déplacement
# ---------------------------------------------------------------------------


class TestCameraMovement:
    SPEED = 0.1  # vitesse explicite pour des assertions nettes

    def make(self):
        return CAMERA(speed=self.SPEED)

    # forward / backward : front = (0,0,-1)

    def test_forward_decreases_z(self):
        cam = self.make()
        cam.forward3D()
        assert cam.coordinates[2] == pytest.approx(-self.SPEED)
        assert cam.coordinates[0] == pytest.approx(0.0)
        assert cam.coordinates[1] == pytest.approx(0.0)

    def test_backward_increases_z(self):
        cam = self.make()
        cam.backward3D()
        assert cam.coordinates[2] == pytest.approx(self.SPEED)

    def test_forward_backward_cancel(self):
        cam = self.make()
        cam.forward3D()
        cam.backward3D()
        assert cam.coordinates == pytest.approx([0, 0, 0])

    # right / left : right = (1,0,0)

    def test_right_increases_x(self):
        cam = self.make()
        cam.right3D()
        assert cam.coordinates[0] == pytest.approx(self.SPEED)

    def test_left_decreases_x(self):
        cam = self.make()
        cam.left3D()
        assert cam.coordinates[0] == pytest.approx(-self.SPEED)

    # up / down : up = (0,1,0)

    def test_up_increases_y(self):
        cam = self.make()
        cam.up3D()
        assert cam.coordinates[1] == pytest.approx(self.SPEED)

    def test_down_decreases_y(self):
        cam = self.make()
        cam.down3D()
        assert cam.coordinates[1] == pytest.approx(-self.SPEED)

    # 2D variants (ignore Y)

    def test_forward2d_does_not_change_y(self):
        cam = self.make()
        cam.forward2D()
        assert cam.coordinates[1] == pytest.approx(0.0)

    def test_backward2d_does_not_change_y(self):
        cam = self.make()
        cam.backward2D()
        assert cam.coordinates[1] == pytest.approx(0.0)

    # speed override

    def test_speed_override(self):
        cam = self.make()
        cam.forward3D(speed=1.0)
        assert cam.coordinates[2] == pytest.approx(-1.0)

    # addCoordinates

    def test_add_coordinates(self):
        cam = self.make()
        cam.addCoordinates([3, 4, 5])
        assert cam.coordinates == [3, 4, 5]

    def test_add_coordinates_none_is_noop(self):
        cam = self.make()
        cam.addCoordinates(None)
        assert cam.coordinates == [0, 0, 0]


# ---------------------------------------------------------------------------
# CAMERA — rotations (orthonormalité)
# ---------------------------------------------------------------------------


class TestCameraRotations:
    """
    Propriété invariante : après toute séquence de rotations,
    les axes front / up / right doivent rester orthonormaux.
    """

    def test_yaw_preserves_orthonormality(self):
        cam = CAMERA()
        cam.addYaw(45)
        assert axes_are_orthonormal(cam)

    def test_yaw_90_preserves_orthonormality(self):
        cam = CAMERA()
        cam.addYaw(90)
        assert axes_are_orthonormal(cam)

    def test_pitch_preserves_orthonormality(self):
        cam = CAMERA()
        cam.addPitch(45)
        assert axes_are_orthonormal(cam)

    def test_roll_preserves_orthonormality(self):
        cam = CAMERA()
        cam.addRoll(45)
        assert axes_are_orthonormal(cam)

    def test_combined_rotations_preserve_orthonormality(self):
        cam = CAMERA()
        for _ in range(10):
            cam.addYaw(13)
            cam.addPitch(7)
            cam.addRoll(5)
        assert axes_are_orthonormal(cam)

    def test_full_yaw_360_returns_to_initial(self):
        cam = CAMERA()
        initial_front = (cam.front.x, cam.front.y, cam.front.z)
        for _ in range(4):
            cam.addYaw(90)
        assert cam.front.x == pytest.approx(initial_front[0], abs=1e-9)
        assert cam.front.y == pytest.approx(initial_front[1], abs=1e-9)
        assert cam.front.z == pytest.approx(initial_front[2], abs=1e-9)

    def test_full_pitch_360_returns_to_initial(self):
        cam = CAMERA()
        initial_up = (cam.up.x, cam.up.y, cam.up.z)
        for _ in range(4):
            cam.addPitch(90)
        assert cam.up.x == pytest.approx(initial_up[0], abs=1e-9)
        assert cam.up.y == pytest.approx(initial_up[1], abs=1e-9)
        assert cam.up.z == pytest.approx(initial_up[2], abs=1e-9)

    def test_yaw_changes_front_not_up(self):
        cam = CAMERA()
        up_before = (cam.up.x, cam.up.y, cam.up.z)
        cam.addYaw(30)
        assert cam.up.x == pytest.approx(up_before[0], abs=1e-9)
        assert cam.up.y == pytest.approx(up_before[1], abs=1e-9)
        assert cam.up.z == pytest.approx(up_before[2], abs=1e-9)

    def test_pitch_changes_up_not_right(self):
        cam = CAMERA()
        right_before = (cam.right.x, cam.right.y, cam.right.z)
        cam.addPitch(30)
        assert cam.right.x == pytest.approx(right_before[0], abs=1e-9)
        assert cam.right.y == pytest.approx(right_before[1], abs=1e-9)
        assert cam.right.z == pytest.approx(right_before[2], abs=1e-9)

    def test_roll_changes_right_not_front(self):
        cam = CAMERA()
        front_before = (cam.front.x, cam.front.y, cam.front.z)
        cam.addRoll(30)
        assert cam.front.x == pytest.approx(front_before[0], abs=1e-9)
        assert cam.front.y == pytest.approx(front_before[1], abs=1e-9)
        assert cam.front.z == pytest.approx(front_before[2], abs=1e-9)


# ---------------------------------------------------------------------------
# CAMERA — reset
# ---------------------------------------------------------------------------


class TestCameraReset:
    def test_reset_restores_default_axes(self):
        cam = CAMERA()
        cam.addYaw(45)
        cam.addPitch(30)
        cam.addRoll(20)
        cam.reset()
        assert cam.front.z == pytest.approx(-1.0)
        assert cam.up.y == pytest.approx(1.0)
        assert cam.right.x == pytest.approx(1.0)

    def test_reset_restores_coordinates(self):
        cam = CAMERA()
        cam.addCoordinates([10, 20, 30])
        cam.reset()
        assert cam.coordinates == [0, 0, 0]

    def test_reset_orthonormality(self):
        cam = CAMERA()
        cam.addYaw(123)
        cam.addPitch(456)
        cam.reset()
        assert axes_are_orthonormal(cam)
