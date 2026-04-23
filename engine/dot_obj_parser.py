class OBJ_FILE:
    def __init__(self, file_path: str) -> None:
        self.filePath = file_path
        self.file = None
        self.fileName = self.filePath.split('/')[-1].rstrip('.obj')
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
        self.triangles = [self.trianglesVertices,self.trianglesTextures,self.trianglesNormals]

    def parse(self) -> None:
        self.file = open(self.filePath, "r")
        for line in self.file.readlines():
            line = line.split()
            if not line == []:
                match line[0]:
                    case 'v':
                        vertexCords=[]
                        for word in line[1:]:
                            vertexCords.append(float(word))
                        self.vertices.append(vertexCords)
                    case 'vn':
                        normalCords = []
                        for word in line[1:]:
                            normalCords.append(float(word))
                        self.normals.append(normalCords)
                    case 'vt':
                        textureCords = []
                        for word in line[1:]:
                            textureCords.append(float(word))
                        self.textures.append(textureCords)
                    case 'f':
                        faceVertices = []
                        faceTextures = []
                        faceNormals = []
                        match len(line[1:]):
                            case 3:
                                for word in line[1:]:
                                    infos = word.split('/')
                                    match len(infos):
                                        case 1:
                                            faceVertices.append(int(word)) if not word == '' else faceVertices.append(None)
                                            faceTextures.append(None)
                                            faceNormals.append(None)
                                        case 2:
                                            faceVertices.append(int(infos[0])) if not infos[0] == '' else faceVertices.append(None)
                                            faceTextures.append(int(infos[1])) if not infos[1] == '' else faceTextures.append(None)
                                            faceNormals.append(None)
                                        case 3:
                                            faceVertices.append(int(infos[0])) if not infos[0] == '' else faceVertices.append(None)
                                            faceTextures.append(int(infos[1])) if not infos[1] == '' else faceTextures.append(None)
                                            faceNormals.append(int(infos[2])) if not infos[2] == '' else faceNormals.append(None)

                                self.trianglesVertices.append(faceVertices)
                                self.trianglesTextures.append(faceTextures)
                                self.trianglesNormals.append(faceNormals)
                            case 4:
                                for word in line[1:]:
                                    infos = word.split('/')
                                    match len(infos):
                                        case 1:
                                            faceVertices.append(int(word)) if not word == '' else faceVertices.append(None)
                                            faceTextures.append(None)
                                            faceNormals.append(None)
                                        case 2:
                                            faceVertices.append(int(infos[0])) if not infos[0] == '' else faceVertices.append(None)
                                            faceTextures.append(int(infos[1])) if not infos[1] == '' else faceTextures.append(None)
                                            faceNormals.append(None)
                                        case 3:
                                            faceVertices.append(int(infos[0])) if not infos[0] == '' else faceVertices.append(None)
                                            faceTextures.append(int(infos[1])) if not infos[1] == '' else faceTextures.append(None)
                                            faceNormals.append(int(infos[2])) if not infos[2] == '' else faceNormals.append(None)

                                self.quadsVertices.append(faceVertices)
                                self.quadsTextures.append(faceTextures)
                                self.quadsNormals.append(faceNormals)
        self.file.close()
