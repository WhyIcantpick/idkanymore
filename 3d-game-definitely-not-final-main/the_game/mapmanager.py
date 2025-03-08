from direct.showbase.ShowBase import ShowBase
import pickle


class Mapmanager():
    def __init__(self, base):
        self.base = base
        self.model = 'CubeReal.obj'  # Модель кубика
        self.texture = 'placeholder.png'  # Текстура кубика
        self.land = self.base.render.attachNewNode("Land")  # Створення вузла для "землі"
        self.colors = [(0.5, 0.3, 0.0, 1),
                       (0.2, 0.2, 0.3, 1),
                       (0.5, 0.5, 0.2, 1),
                       (0.0, 0.6, 0.0, 1),]

    def addBlock(self, position):
        pos = position
        # Завантаження моделі та текстури
        self.block = self.base.loader.loadModel(self.model)  # Використовуємо self.base.loader
        self.block.setTexture(self.base.loader.loadTexture(self.texture))
        self.block.setScale(0.5) #delete
        self.block.setPos(position)
        self.block.reparentTo(self.land)
        self.color = self.getColor(position[2])
        self.block.setColor(self.color)
       # Додаємо блок до "землі"
        self.block.setTag("at", str(pos))

    def addGreen(self, position):
        pos = position
        self.block = self.base.loader.loadModel(self.model)  # Використовуємо self.base.loader
        self.block.setTexture(self.base.loader.loadTexture("grass.png"))
        self.block.setPos(position)
        self.block.setScale(0.5) #delete
        self.block.reparentTo(self.land)
        self.block.setTag("at", str(pos))

    def addWhite(self, position):
        pos = position
        self.block = self.base.loader.loadModel(self.model)  # Використовуємо self.base.loader
        self.block.setTexture(self.base.loader.loadTexture("bedrock.png"))
        self.block.setPos(position)
        self.block.setScale(0.5) #delete
        self.block.reparentTo(self.land)
        self.block.setTag("at", str(pos))

    def addBrown(self, position):
        pos = position
        self.block = self.base.loader.loadModel(self.model)  # Використовуємо self.base.loader
        self.block.setTexture(self.base.loader.loadTexture("wood.png"))
        self.block.setPos(position)
        self.block.reparentTo(self.land)
        self.block.setScale(0.5) #delete

        self.block.setTag("at", str(pos))

    def startNew(self):
        # Скидання або оновлення "землі"
        self.land.removeNode()
        self.land = self.base.render.attachNewNode("Land")

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
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x, y, z0 ))
                    x += 1
                y += 1

    def TREE(self, pos):
        self.clear()
        pos = (10, 10, 10)
        leaf = self.addGreen(pos)

    def getColor(self, z):
        if int(z / 2) < len(self.colors):
            return self.colors[int(z / 2)]
        else:
            return self.colors[len(self.colors) - 1]
    
    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            print("зайнято") #delete
            return False
        else:
            print("вільно") #delete
            return True

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))
    
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    
    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def buildGreen(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addGreen(new)

    def buildWhite(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addWhite(new)

    def buildBrown(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBrown(new)
        
    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z - 1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)