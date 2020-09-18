from random import randint
from Grid_class import Grid


class Speler:
    def __init__(self):
        self.grid = Grid()
        self.grid.initBuren()
        self.boten = []
        self.aantalSchoten = 0
        self.aantalSchotenRaak = 0
        self.tegenstander = None
        self.botenTegenstander = []

    def plaatsBoten(self):
        gekozenCellenMetRichting = {}
        for boot in self.boten:
            geplaatst = False
            x = randint(0, 99)
            while geplaatst is False:
                while self.grid.getCellen()[x] == 2:
                    x = randint(0, 99)
                rotatie = randint(0, 3)
                teller = 0
                while teller < 4 and geplaatst is False:
                    geplaatst = boot.setPositie(self.grid.getCellen()[x], rotatie, boot, gekozenCellenMetRichting)
                    rotatie = (rotatie + 1) % 4
                    teller = teller + 1
                # anders blijft het in een loop als er in deze cel op geen enkele rotatie de boot kan geplaatst worden
                x = randint(0, 99)
            boot.initStatus()

    def updateBoten(self, cel):
        for boot in self.botenTegenstander:
            if boot.containsCel(cel):
                boot.geraakt()
                if boot.isDood():
                    self.botenTegenstander.remove(boot)
                    return True
        return False

    def vuur(self, cel):  # geeft true terug als een boot gezonken is, op deze manier worden er attributen bespaard
        gezonken = False
        if cel.sterf():
            gezonken = self.updateBoten(cel)
        self.aantalSchoten += 1
        if cel.getStatus() == 3:
            self.aantalSchotenRaak += 1
        return gezonken

    def getStatistics(self):
        list = [self.aantalSchoten, self.aantalSchotenRaak]
        return list

    def getGrid(self):
        return self.grid

    def getBoten(self):
        return self.boten

    def setBoten(self, boten):
        self.boten = boten

    def setTegenstander(self, tegenstander):
        self.tegenstander = tegenstander

    def getTegenstander(self):
        return self.tegenstander

    def setBotenTegenstander(self):
        self.botenTegenstander = self.tegenstander.getBoten()

    def remove(self, boot):
        self.boten.remove(boot)