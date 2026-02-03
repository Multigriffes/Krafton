class OBJ_FILE:
    def __init__(self, filePath):
        self.cache=None
        self.filePath = filePath
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

    def parse(self,forceParse=False):
        print('Parse')
        if forceParse:
            self.parseFile()
        else:
            from models.models_cache import cache
            self.cache=cache
            if not (f'{self.fileName}_Vertices' in self.cache.keys()):
                self.parseFile()
            else:
                self.parseCache()

    def parseCache(self):
        print('ParseCache')
        self.vertices = self.cache[f'{self.fileName}_Vertices']
        self.normals = self.cache[f'{self.fileName}_Normals']
        self.textures = self.cache[f'{self.fileName}_Textures']
        self.triangles = self.cache[f'{self.fileName}_Triangles']
        self.quads = self.cache[f'{self.fileName}_Quads']

    def parseFile(self):
        print('ParseFile')
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
                                    faceVertices.append(int(infos[0])) if not infos[0] == '' else faceVertices.append(None)
                                    faceTextures.append(int(infos[1])) if not infos[1] == '' else faceTextures.append(None)
                                    faceNormals.append(int(infos[2])) if not infos[2] == '' else faceNormals.append(None)
                                self.trianglesVertices.append(faceVertices)
                                self.trianglesTextures.append(faceTextures)
                                self.trianglesNormals.append(faceNormals)
                            case 4:
                                for word in line[1:]:
                                    infos = word.split('/')
                                    faceVertices.append(int(infos[0])) if not infos[0]=='' else faceVertices.append(None)
                                    faceTextures.append(int(infos[1])) if not infos[1]=='' else faceTextures.append(None)
                                    faceNormals.append(int(infos[2])) if not infos[2]=='' else faceNormals.append(None)
                                self.quadsVertices.append(faceVertices)
                                self.quadsTextures.append(faceTextures)
                                self.quadsNormals.append(faceNormals)
        self.file.close()
        self.writeToCache()

    def writeToCache(self):
        print('WriteToCache')
        self.cache[f'{self.fileName}_Vertices'] = self.vertices
        self.cache[f'{self.fileName}_Normals'] = self.normals
        self.cache[f'{self.fileName}_Textures'] = self.textures
        self.cache[f'{self.fileName}_Triangles'] = self.triangles
        self.cache[f'{self.fileName}_Quads'] = self.quads

        self.cacheFile = open('models/models_cache.py', 'w')
        self.cacheFile.write(f'cache = {self.cache}')
        self.cacheFile.close()
