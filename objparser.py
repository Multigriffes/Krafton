class ObjParser:
    def __init__(self,filename):
        self.filename = filename
        self.file = open(self.filename,'r')
        self.vertices = []
        self.normals = []
        self.textures = []
        self.facesNormals = []
        self.facesTextures = []
        self.facesVertices = []
        self.faces=[self.facesVertices,self.facesTextures,self.facesNormals]

    def parse(self):
        for line in self.file.readlines():
            line = line.rstrip()
            match line[0:3]:
                case 'v  ':
                    vertexCoord = []
                    usefulPart = line[3:]
                    for Coord in usefulPart.split(' '):
                        vertexCoord.append(float(Coord))
                    self.vertices.append(vertexCoord)
                case 'vn ':
                    vertexNormal = []
                    usefulPart = line[3:]
                    for Coord in usefulPart.split(' '):
                        vertexNormal.append(float(Coord))
                    self.normals.append(vertexNormal)
                case 'vt ':
                    vertexTexture = []
                    usefulPart = line[3:]
                    for Coord in usefulPart.split(' '):
                        vertexTexture.append(float(Coord))
                    self.textures.append(vertexTexture)
                case 'f  ':
                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    usefulPart = line[2:]
                    for vertex in usefulPart.split(' '):
                        infos = vertex.split('/')
                        if not infos[0] == '':
                            faceVertices.append(int(infos[0]))
                        else:
                            faceVertices.append(None)
                        if not infos[1] == '':
                            faceTextures.append(int(infos[1]))
                        else:
                            faceTextures.append(None)
                        if not infos[2] == '':
                            faceNormals.append(int(infos[2]))
                        else:
                            faceNormals.append(None)
                    self.facesVertices.append(faceVertices)
                    self.facesNormals.append(faceNormals)
                    self.facesTextures.append(faceTextures)
                case _:
                    match line[0:2]:
                        case 'v ':
                            vertexCoord = []
                            usefulPart = line[2:]
                            for Coord in usefulPart.split(' '):
                                vertexCoord.append(float(Coord))
                            self.vertices.append(vertexCoord)
                        case 'vn':
                            vertexNormal = []
                            usefulPart = line[2:]
                            for Coord in usefulPart.split(' '):
                                vertexNormal.append(float(Coord))
                            self.normals.append(vertexNormal)
                        case 'vt':
                            vertexTexture = []
                            usefulPart = line[2:]
                            for Coord in usefulPart.split(' '):
                                vertexTexture.append(float(Coord))
                            self.textures.append(vertexTexture)
                        case 'f ':
                            faceVertices = []
                            faceTextures = []
                            faceNormals = []
                            usefulPart = line[2:]
                            for vertex in usefulPart.split(' '):
                                infos = vertex.split('/')
                                if not infos[0] == '':
                                    faceVertices.append(int(infos[0]))
                                else:
                                    faceVertices.append(None)
                                if not infos[1] == '':
                                    faceTextures.append(int(infos[1]))
                                else:
                                    faceTextures.append(None)
                                if not infos[2] == '':
                                    faceNormals.append(int(infos[2]))
                                else:
                                    faceNormals.append(None)
                            self.facesVertices.append(faceVertices)
                            self.facesNormals.append(faceNormals)
                            self.facesTextures.append(faceTextures)


    def releaseFile(self):
        self.file.close()