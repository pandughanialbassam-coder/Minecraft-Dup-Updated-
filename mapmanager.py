# write the code for creating and managing the map here

import pickle
class Mapmanager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'
        #self.color = (0.2, 0.6, 0.3, 1)
        self.colors = [
            (0.4, 0.6, 0.3, 1),
            (0.1, 0.7, 0.3, 1),
            (0.8, 0.4, 0.3, 1),
            (0.2, 0.3, 0.3, 1),
        ]

        self.startNew()

        #self.addBlock((0, 10, 5), (0.5, 0.6, 0.3, 1))
        #self.addBlock((1, 10, 5), (0.7, 0.6, 0.3, 1))
        #self.addBlock((2, 10, 5), (0.9, 0.6, 0.3, 1))
    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors)-1]

    def startNew(self):
        self.land = render.attachNewNode('Land')

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        #self.block.setColor(self.color)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.setTag('at', str(position))
        self.block.reparentTo(self.land)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0 
                line = line.split(' ') 
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y 

    def findBlocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))
        
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos 
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z-1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as file_out:
            pickle.dump(len(blocks), file_out)

            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file_out)
    
    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as file_in:
            length = pickle.load(file_in)

            for i in range(length):
                pos = pickle.load(file_in)
                self.addBlock(pos)