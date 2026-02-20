"""Parser de fichiers Wavefront OBJ avec système de cache optionnel."""

import logging

logger = logging.getLogger(__name__)


class OBJ_FILE:
    """Charge et parse un fichier .obj en listes de sommets, normales, textures et faces.

    Les faces sont séparées en triangles (3 sommets) et quads (4 sommets).
    Chaque liste de faces est de la forme [vertices, textures, normales].
    """

    def __init__(self, file_path: str) -> None:
        self.cache = {}
        self.filePath = file_path
        self.file = None
        self.fileName = self.filePath.split("/")[-1].rstrip(".obj")
        self.cacheFile = None
        self.vertices = []
        self.normals = []
        self.textures = []
        self.quadsNormals = []
        self.quadsTextures = []
        self.quadsVertices = []
        self.quads = [self.quadsVertices, self.quadsTextures, self.quadsNormals]
        self.trianglesNormals = []
        self.trianglesTextures = []
        self.trianglesVertices = []
        self.triangles = [
            self.trianglesVertices,
            self.trianglesTextures,
            self.trianglesNormals,
        ]

    def parse(self, force_parse: bool = False) -> None:
        """Parse le fichier OBJ. Utilise le cache si disponible, sauf si force_parse=True."""
        if force_parse:
            logger.info("Parsing forcé de '%s'.", self.fileName)
            self.parseFile()
        else:
            from engine.models.models_cache import cache

            self.cache = cache
            if not (f"{self.fileName}_Vertices" in self.cache.keys()):
                logger.info(
                    "Cache absent pour '%s', lecture du fichier.", self.fileName
                )
                self.parseFile()
            else:
                logger.info(
                    "Cache trouvé pour '%s', chargement depuis le cache.", self.fileName
                )
                self.parseCache()

    def parseCache(self) -> None:
        """Charge les données depuis le cache en mémoire (models_cache.py)."""
        self.vertices = self.cache[f"{self.fileName}_Vertices"]
        self.normals = self.cache[f"{self.fileName}_Normals"]
        self.textures = self.cache[f"{self.fileName}_Textures"]
        self.triangles = self.cache[f"{self.fileName}_Triangles"]
        self.quads = self.cache[f"{self.fileName}_Quads"]
        logger.debug(
            "Cache chargé : %d sommets, %d triangles, %d quads.",
            len(self.vertices),
            len(self.triangles[0]),
            len(self.quads[0]),
        )

    def _parse_face_token(self, token: str) -> tuple:
        """
        Parse un token de face OBJ. Formats supportés :
          v        →  (v, None, None)
          v/vt     →  (v, vt, None)
          v//vn    →  (v, None, vn)
          v/vt/vn  →  (v, vt, vn)
        """
        parts = token.split("/")
        v = int(parts[0]) if len(parts) > 0 and parts[0] != "" else None
        vt = int(parts[1]) if len(parts) > 1 and parts[1] != "" else None
        vn = int(parts[2]) if len(parts) > 2 and parts[2] != "" else None
        return v, vt, vn

    def parseFile(self) -> None:
        """Lit et parse le fichier .obj ligne par ligne (v, vn, vt, f)."""
        logger.debug("Ouverture du fichier : %s", self.filePath)
        self.file = open(self.filePath, "r")
        for line in self.file.readlines():
            line = line.split()
            if not line == []:
                match line[0]:
                    case "v":
                        vertexCords = []
                        for word in line[1:]:
                            vertexCords.append(float(word))
                        self.vertices.append(vertexCords)
                    case "vn":
                        normalCords = []
                        for word in line[1:]:
                            normalCords.append(float(word))
                        self.normals.append(normalCords)
                    case "vt":
                        textureCords = []
                        for word in line[1:]:
                            textureCords.append(float(word))
                        self.textures.append(textureCords)
                    case "f":
                        faceVertices = []
                        faceTextures = []
                        faceNormals = []
                        match len(line[1:]):
                            case 3:
                                for word in line[1:]:
                                    v, vt, vn = self._parse_face_token(word)
                                    faceVertices.append(v)
                                    faceTextures.append(vt)
                                    faceNormals.append(vn)
                                self.trianglesVertices.append(faceVertices)
                                self.trianglesTextures.append(faceTextures)
                                self.trianglesNormals.append(faceNormals)
                            case 4:
                                for word in line[1:]:
                                    v, vt, vn = self._parse_face_token(word)
                                    faceVertices.append(v)
                                    faceTextures.append(vt)
                                    faceNormals.append(vn)
                                self.quadsVertices.append(faceVertices)
                                self.quadsTextures.append(faceTextures)
                                self.quadsNormals.append(faceNormals)
        self.file.close()
        logger.info(
            "Fichier parsé : %d sommets, %d normales, %d triangles, %d quads.",
            len(self.vertices),
            len(self.normals),
            len(self.trianglesVertices),
            len(self.quadsVertices),
        )
        # self.writeToCache()

    def writeToCache(self) -> None:
        """Sauvegarde les données parsées dans models_cache.py (actuellement désactivé)."""
        logger.debug("Écriture du cache pour '%s'.", self.fileName)
        self.cache[f"{self.fileName}_Vertices"] = self.vertices
        self.cache[f"{self.fileName}_Normals"] = self.normals
        self.cache[f"{self.fileName}_Textures"] = self.textures
        self.cache[f"{self.fileName}_Triangles"] = self.triangles
        self.cache[f"{self.fileName}_Quads"] = self.quads

        self.cacheFile = open("engine/models/models_cache.py", "w")
        self.cacheFile.write(f"cache = {self.cache}")
        self.cacheFile.close()
