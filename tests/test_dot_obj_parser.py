"""Tests unitaires pour engine/dot_obj_parser.py."""

import os
import tempfile

import pytest

from engine.dot_obj_parser import OBJ_FILE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def write_tmp_obj(content: str) -> str:
    """Écrit content dans un fichier .obj temporaire et retourne son chemin."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".obj", delete=False, encoding="utf-8"
    ) as f:
        f.write(content)
        return f.name


# ---------------------------------------------------------------------------
# _parse_face_token
# ---------------------------------------------------------------------------


class TestParseFaceToken:
    def setup_method(self):
        # On instancie avec un chemin fictif — __init__ n'ouvre pas le fichier
        self.parser = OBJ_FILE("dummy.obj")

    def test_vertex_only(self):
        v, vt, vn = self.parser._parse_face_token("5")
        assert v == 5
        assert vt is None
        assert vn is None

    def test_vertex_texture(self):
        v, vt, vn = self.parser._parse_face_token("1/2")
        assert v == 1
        assert vt == 2
        assert vn is None

    def test_vertex_normal_no_texture(self):
        v, vt, vn = self.parser._parse_face_token("1//3")
        assert v == 1
        assert vt is None
        assert vn == 3

    def test_vertex_texture_normal(self):
        v, vt, vn = self.parser._parse_face_token("1/2/3")
        assert v == 1
        assert vt == 2
        assert vn == 3

    def test_large_indices(self):
        v, vt, vn = self.parser._parse_face_token("100/200/300")
        assert v == 100
        assert vt == 200
        assert vn == 300


# ---------------------------------------------------------------------------
# parseFile
# ---------------------------------------------------------------------------

TRIANGLE_OBJ = """\
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.0 1.0 0.0
vn 0.0 0.0 1.0
f 1//1 2//1 3//1
"""

QUAD_OBJ = """\
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 0.0 1.0 0.0
vn 0.0 0.0 1.0
f 1//1 2//1 3//1 4//1
"""

MIXED_OBJ = """\
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.0 1.0 0.0
v 1.0 1.0 0.0
vn 0.0 0.0 1.0
vt 0.0 0.0
f 1/1/1 2/1/1 3/1/1
f 1/1/1 2/1/1 3/1/1 4/1/1
"""


class TestParseFile:
    def test_vertices_loaded(self):
        path = write_tmp_obj(TRIANGLE_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.vertices) == 3
            assert p.vertices[0] == [0.0, 0.0, 0.0]
            assert p.vertices[1] == [1.0, 0.0, 0.0]
        finally:
            os.unlink(path)

    def test_normals_loaded(self):
        path = write_tmp_obj(TRIANGLE_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.normals) == 1
            assert p.normals[0] == [0.0, 0.0, 1.0]
        finally:
            os.unlink(path)

    def test_triangle_face(self):
        path = write_tmp_obj(TRIANGLE_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.trianglesVertices) == 1
            assert len(p.quadsVertices) == 0
            assert p.trianglesVertices[0] == [1, 2, 3]
        finally:
            os.unlink(path)

    def test_quad_face(self):
        path = write_tmp_obj(QUAD_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.quadsVertices) == 1
            assert len(p.trianglesVertices) == 0
            assert p.quadsVertices[0] == [1, 2, 3, 4]
        finally:
            os.unlink(path)

    def test_mixed_faces(self):
        path = write_tmp_obj(MIXED_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.trianglesVertices) == 1
            assert len(p.quadsVertices) == 1
        finally:
            os.unlink(path)

    def test_texture_coords_loaded(self):
        path = write_tmp_obj(MIXED_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.textures) == 1
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        p = OBJ_FILE("/nonexistent/path/missing.obj")
        with pytest.raises(FileNotFoundError):
            p.parseFile()

    def test_empty_file(self):
        path = write_tmp_obj("")
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert p.vertices == []
            assert p.normals == []
            assert p.trianglesVertices == []
            assert p.quadsVertices == []
        finally:
            os.unlink(path)

    def test_comments_ignored(self):
        content = "# commentaire\nv 1.0 2.0 3.0\n# autre commentaire\n"
        path = write_tmp_obj(content)
        try:
            p = OBJ_FILE(path)
            p.parseFile()
            assert len(p.vertices) == 1
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# parse (force_parse)
# ---------------------------------------------------------------------------


class TestParse:
    def test_force_parse_reads_file(self):
        path = write_tmp_obj(TRIANGLE_OBJ)
        try:
            p = OBJ_FILE(path)
            p.parse(force_parse=True)
            assert len(p.vertices) == 3
        finally:
            os.unlink(path)

    def test_force_parse_missing_file(self):
        p = OBJ_FILE("/nonexistent/missing.obj")
        with pytest.raises(FileNotFoundError):
            p.parse(force_parse=True)
