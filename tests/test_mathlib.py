"""Tests unitaires pour engine/mathlib.py."""

import math
import pytest

from engine.mathlib import (
    QUATERNION,
    crossProduct,
    crossProductNormalized,
    degrees,
    dotProduct,
    normalize,
    radians,
)


# ---------------------------------------------------------------------------
# radians / degrees
# ---------------------------------------------------------------------------


class TestConversions:
    def test_radians_zero(self):
        assert radians(0) == 0.0

    def test_radians_180(self):
        assert radians(180) == pytest.approx(math.pi)

    def test_radians_360(self):
        assert radians(360) == pytest.approx(2 * math.pi)

    def test_degrees_pi(self):
        assert degrees(math.pi) == pytest.approx(180.0)

    def test_roundtrip(self):
        assert degrees(radians(45)) == pytest.approx(45.0)

    def test_roundtrip_negative(self):
        assert degrees(radians(-90)) == pytest.approx(-90.0)


# ---------------------------------------------------------------------------
# QUATERNION
# ---------------------------------------------------------------------------


class TestQuaternionInit:
    def test_default_values(self):
        q = QUATERNION()
        assert q.w == 0.0
        assert q.x == 0.0
        assert q.y == 0.0
        assert q.z == 0.0

    def test_explicit_values(self):
        q = QUATERNION(1, 2, 3, 4)
        assert q.w == 1
        assert q.x == 2
        assert q.y == 3
        assert q.z == 4

    def test_list_attribute(self):
        q = QUATERNION(1, 2, 3, 4)
        assert q.list == [1, 2, 3, 4]

    def test_getitem(self):
        q = QUATERNION(1, 2, 3, 4)
        assert q[0] == 1
        assert q[1] == 2
        assert q[2] == 3
        assert q[3] == 4


class TestGetLengthNoSqrt:
    def test_unit_vector(self):
        q = QUATERNION(0, 1, 0, 0)
        assert q.getLengthNoSqrt() == pytest.approx(1.0)

    def test_known_value(self):
        # 3² + 4² = 25
        q = QUATERNION(0, 3, 4, 0)
        assert q.getLengthNoSqrt() == pytest.approx(25.0)

    def test_all_components(self):
        q = QUATERNION(1, 1, 1, 1)
        assert q.getLengthNoSqrt() == pytest.approx(4.0)

    def test_zero_quaternion(self):
        q = QUATERNION(0, 0, 0, 0)
        assert q.getLengthNoSqrt() == pytest.approx(0.0)


class TestQuaternionMultiply:
    def test_type_error(self):
        q = QUATERNION(1, 0, 0, 0)
        with pytest.raises(AssertionError):
            _ = q * 5

    def test_identity_right(self):
        q = QUATERNION(1, 2, 3, 4)
        identity = QUATERNION(1, 0, 0, 0)
        result = q * identity
        assert result.w == pytest.approx(q.w)
        assert result.x == pytest.approx(q.x)
        assert result.y == pytest.approx(q.y)
        assert result.z == pytest.approx(q.z)

    def test_identity_left(self):
        q = QUATERNION(1, 2, 3, 4)
        identity = QUATERNION(1, 0, 0, 0)
        result = identity * q
        assert result.w == pytest.approx(q.w)
        assert result.x == pytest.approx(q.x)
        assert result.y == pytest.approx(q.y)
        assert result.z == pytest.approx(q.z)

    def test_i_times_j_equals_k(self):
        # i * j = k  en quaternions purs
        i = QUATERNION(0, 1, 0, 0)
        j = QUATERNION(0, 0, 1, 0)
        result = i * j
        assert result.w == pytest.approx(0.0)
        assert result.x == pytest.approx(0.0)
        assert result.y == pytest.approx(0.0)
        assert result.z == pytest.approx(1.0)

    def test_j_times_i_equals_minus_k(self):
        # j * i = -k
        i = QUATERNION(0, 1, 0, 0)
        j = QUATERNION(0, 0, 1, 0)
        result = j * i
        assert result.w == pytest.approx(0.0)
        assert result.x == pytest.approx(0.0)
        assert result.y == pytest.approx(0.0)
        assert result.z == pytest.approx(-1.0)

    def test_not_commutative(self):
        a = QUATERNION(1, 2, 3, 4)
        b = QUATERNION(5, 6, 7, 8)
        ab = a * b
        ba = b * a
        # Au moins un composant doit différer
        assert not (
            ab.w == pytest.approx(ba.w)
            and ab.x == pytest.approx(ba.x)
            and ab.y == pytest.approx(ba.y)
            and ab.z == pytest.approx(ba.z)
        )


class TestQuaternionInverse:
    def test_unit_quaternion_inverse(self):
        # Pour un quaternion unitaire q, q * q⁻¹ ≈ identité
        angle = math.pi / 3
        q = QUATERNION(
            math.cos(angle / 2), math.sin(angle / 2), 0, 0
        )
        inv = q.inverse()
        result = q * inv
        assert result.w == pytest.approx(1.0, abs=1e-9)
        assert result.x == pytest.approx(0.0, abs=1e-9)
        assert result.y == pytest.approx(0.0, abs=1e-9)
        assert result.z == pytest.approx(0.0, abs=1e-9)

    def test_negates_vector_part(self):
        # Pour w=1, x=0.5 : l'inverse doit avoir x négatif
        q = QUATERNION(w=1, x=0.5, y=0, z=0)
        inv = q.inverse()
        assert inv.x < 0


# ---------------------------------------------------------------------------
# dotProduct
# ---------------------------------------------------------------------------


class TestDotProduct:
    def test_orthogonal_vectors(self):
        assert dotProduct([1, 0, 0], [0, 1, 0]) == pytest.approx(0.0)

    def test_parallel_unit_vectors(self):
        assert dotProduct([1, 0, 0], [1, 0, 0]) == pytest.approx(1.0)

    def test_known_value(self):
        # [1,2,3]·[4,5,6] = 4+10+18 = 32
        assert dotProduct([1, 2, 3], [4, 5, 6]) == pytest.approx(32.0)

    def test_negative_values(self):
        assert dotProduct([1, 0, 0], [-1, 0, 0]) == pytest.approx(-1.0)

    def test_length_mismatch(self):
        with pytest.raises(AssertionError):
            dotProduct([1, 2], [1, 2, 3])


# ---------------------------------------------------------------------------
# crossProduct
# ---------------------------------------------------------------------------


class TestCrossProduct:
    def test_i_cross_j_equals_k(self):
        i = QUATERNION(0, 1, 0, 0)
        j = QUATERNION(0, 0, 1, 0)
        k = crossProduct(i, j)
        assert k.w == pytest.approx(0.0)
        assert k.x == pytest.approx(0.0)
        assert k.y == pytest.approx(0.0)
        assert k.z == pytest.approx(1.0)

    def test_j_cross_k_equals_i(self):
        j = QUATERNION(0, 0, 1, 0)
        k = QUATERNION(0, 0, 0, 1)
        result = crossProduct(j, k)
        assert result.x == pytest.approx(1.0)
        assert result.y == pytest.approx(0.0)
        assert result.z == pytest.approx(0.0)

    def test_anticommutative(self):
        a = QUATERNION(0, 1, 2, 3)
        b = QUATERNION(0, 4, 5, 6)
        ab = crossProduct(a, b)
        ba = crossProduct(b, a)
        assert ab.x == pytest.approx(-ba.x)
        assert ab.y == pytest.approx(-ba.y)
        assert ab.z == pytest.approx(-ba.z)

    def test_self_cross_is_zero(self):
        a = QUATERNION(0, 1, 2, 3)
        result = crossProduct(a, a)
        assert result.x == pytest.approx(0.0, abs=1e-10)
        assert result.y == pytest.approx(0.0, abs=1e-10)
        assert result.z == pytest.approx(0.0, abs=1e-10)

    def test_type_error(self):
        with pytest.raises(AssertionError):
            crossProduct([1, 0, 0], QUATERNION(0, 1, 0, 0))

    def test_w_is_always_zero(self):
        a = QUATERNION(0, 1, 2, 3)
        b = QUATERNION(0, 4, 5, 6)
        result = crossProduct(a, b)
        assert result.w == 0


# ---------------------------------------------------------------------------
# normalize
# ---------------------------------------------------------------------------


class TestNormalize:
    def test_unit_vector_unchanged(self):
        v = QUATERNION(0, 1, 0, 0)
        result = normalize(v)
        assert result.x == pytest.approx(1.0)
        assert result.y == pytest.approx(0.0)
        assert result.z == pytest.approx(0.0)

    def test_result_has_unit_length(self):
        v = QUATERNION(0, 3, 4, 0)
        result = normalize(v)
        length = math.sqrt(result.x**2 + result.y**2 + result.z**2)
        assert length == pytest.approx(1.0)

    def test_direction_preserved(self):
        v = QUATERNION(0, 0, 5, 0)
        result = normalize(v)
        assert result.x == pytest.approx(0.0)
        assert result.y == pytest.approx(1.0)
        assert result.z == pytest.approx(0.0)

    def test_type_error(self):
        with pytest.raises(AssertionError):
            normalize([1, 0, 0])


# ---------------------------------------------------------------------------
# crossProductNormalized
# ---------------------------------------------------------------------------


class TestCrossProductNormalized:
    def test_result_has_unit_length(self):
        a = QUATERNION(0, 1, 0, 0)
        b = QUATERNION(0, 0, 1, 0)
        result = crossProductNormalized(a, b)
        length = math.sqrt(result.x**2 + result.y**2 + result.z**2)
        assert length == pytest.approx(1.0)

    def test_result_perpendicular_to_inputs(self):
        a = QUATERNION(0, 1, 0, 0)
        b = QUATERNION(0, 0, 1, 0)
        result = crossProductNormalized(a, b)
        dot_a = dotProduct([result.x, result.y, result.z], [a.x, a.y, a.z])
        dot_b = dotProduct([result.x, result.y, result.z], [b.x, b.y, b.z])
        assert dot_a == pytest.approx(0.0, abs=1e-10)
        assert dot_b == pytest.approx(0.0, abs=1e-10)

    def test_known_axes(self):
        # Gram-Schmidt : up × right = front (0,0,-1) dans la config caméra par défaut
        up = QUATERNION(0, 0, 1, 0)
        right = QUATERNION(0, 1, 0, 0)
        front = crossProductNormalized(up, right)
        assert front.z == pytest.approx(-1.0, abs=1e-10)
