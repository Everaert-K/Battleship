class Cel:
    fotoKeuze = 0
    # xOrigin is x-coördinaat van het punt linkerbovenhoek volledige grid, waarde wordt ingesteld in de methode setX
    xOrigin = 0
    # yOrigin is y-coördinaat van het punt linkerbovenhoek volledige grid, waarde wordt ingesteld in de methode setY
    yOrigin = 0
    zijdeCel = 50  # de zijde van de getekende cel in de klasse Speelveld

    def __init__(self, nummer):
        self.status = 0
        self.nummer = nummer

        # waarde wordt ingesteld in de methode setX
        self.xCoordinaatLinkerBovenhoek = 0
        # waarde wordt ingesteld in de methode setY
        self.yCoordinaatLinkerBovenhoek = 0
        self.buren = [None, None, None, None]
        self.initDensiteit(self.getRij())

    def initBuren(self, grid):
        if self.nummer == 0 or self.nummer == 9 or self.nummer == 90 or self.nummer == 99:
            if self.nummer == 0:
                self.buren[1] = grid.getCellen()[self.nummer + 1]
                self.buren[2] = grid.getCellen()[self.nummer + 10]
            if self.nummer == 9:
                self.buren[2] = grid.getCellen()[self.nummer + 10]
                self.buren[3] = grid.getCellen()[self.nummer - 1]
            if self.nummer == 90:
                self.buren[0] = grid.getCellen()[self.nummer - 10]
                self.buren[1] = grid.getCellen()[self.nummer + 1]
            if self.nummer == 99:
                self.buren[0] = grid.getCellen()[self.nummer - 10]
                self.buren[3] = grid.getCellen()[self.nummer - 1]
        elif 0 < self.nummer < 9 or 90 < self.nummer < 99:
            if 0 < self.nummer < 9:
                self.buren[1] = grid.getCellen()[self.nummer + 1]
                self.buren[2] = grid.getCellen()[self.nummer + 10]
                self.buren[3] = grid.getCellen()[self.nummer - 1]
            else:
                self.buren[0] = grid.getCellen()[self.nummer - 10]
                self.buren[1] = grid.getCellen()[self.nummer + 1]
                self.buren[3] = grid.getCellen()[self.nummer - 1]
        elif self.getKolom() == 0 or self.getKolom() == 9:
            if self.getKolom() == 0:
                self.buren[0] = grid.getCellen()[self.nummer - 10]
                self.buren[1] = grid.getCellen()[self.nummer + 1]
                self.buren[2] = grid.getCellen()[self.nummer + 10]
            else:
                self.buren[0] = grid.getCellen()[self.nummer - 10]
                self.buren[2] = grid.getCellen()[self.nummer + 10]
                self.buren[3] = grid.getCellen()[self.nummer - 1]
        else:
            self.buren[0] = grid.getCellen()[self.nummer - 10]
            self.buren[1] = grid.getCellen()[self.nummer + 1]
            self.buren[2] = grid.getCellen()[self.nummer + 10]
            self.buren[3] = grid.getCellen()[self.nummer - 1]

    def __str__(self):
        s = "Nummer: " + str(self.nummer)
        s += "\nStatus: " + str(self.status)
        s += "\nRij: " + str(self.getRij()) + "  Kolom: " + str(self.getKolom())
        s += "\nBuren: ("
        if self.buren[0] is None:
            s += "None, "
        else:
            s += str(self.buren[0].getNummer()) + ", "
        if self.buren[1] is None:
            s += "None, "
        else:
            s += str(self.buren[1].getNummer()) + ", "
        if self.buren[2] is None:
            s += "None, "
        else:
            s += str(self.buren[2].getNummer()) + ", "
        if self.buren[3] is None:
            s += "None"
        else:
            s += str(self.buren[3].getNummer())
        s += ")"
        s += "\nDensiteit: " + str(self.densiteit) + "\n"
        return str(s)

    def sterf(self):
        # 0 geen boot niet geschoten, 1 geen boot wel geschoten, 2 boot niet geschoten, 3 boot geschoten
        raak = False
        if self.status == 0:
            self.status = 1
        elif self.status == 2:
            self.status = 3
            raak = True
        self.updateDensiteit()
        print("Raak = " + str(raak))
        return raak

    def getNummer(self):
        return self.nummer

    def getRij(self):
        return int((self.nummer - self.getKolom()) / 10)

    def getKolom(self):
        return self.nummer % 10

    def getXCoordinaat(self):
        return self.xCoordinaatLinkerBovenhoek

    def getYCoordinaat(self):
        return self.yCoordinaatLinkerBovenhoek

    def setStatus(self, getal):
        if 0 <= getal < 4:
            self.status = getal
            print("Cel " + str(self.nummer) + " is van status veranderd")
        else:
            print("foute status ingegeven bij setStatus")

    def setFoto(self):
        if self.status == 1:
            return 0
        elif self.status == 3:
            return 1
        else:
            return None

    def initDensiteit(self, rij):
        if self.nummer == 0 or self.nummer == 9 or self.nummer == 90 or self.nummer == 99:
            self.densiteit = -5
        elif self.nummer % 10 == 0 or self.nummer % 10 == 9 or rij == 0 or rij == 9:
            self.densiteit = -4
        elif self.nummer % 10 == 1 or self.nummer % 10 == 8 or rij == 1 or rij == 8:
            self.densiteit = -3
        elif self.nummer % 10 == 2 or self.nummer % 10 == 7 or rij == 2 or rij == 7:
            self.densiteit = -2
        elif self.nummer % 10 == 3 or self.nummer % 10 == 6 or rij == 3 or rij == 6:
            self.densiteit = -1
        else:
            self.densiteit = 0

    def getBuren(self):
        return self.buren

    def getBuur(self, getal):  # 0 is boven, 1 is rechts, 2 is onder, 3 is links
        return self.buren[getal]

    def updateDensiteit(self):
        aftrekken = -3
        self.densiteit += aftrekken
        lijstBuren1 = self.buren
        for x in range(0, 4):
            buur1 = lijstBuren1[x]
            if buur1 is not None:
                buur1.densiteit -= 2
                buur2 = buur1.buren[x]
                if buur2 is not None:
                    buur2.densiteit -= 1

    def bepaalNummer(self, xCoordinaat, yCoordinaat):
        if xCoordinaat + yCoordinaat < 10:
            return int(xCoordinaat)
        else:
            getal = str(yCoordinaat) + "" + str(xCoordinaat)
            getal = int(getal)
            return getal

    def getStatus(self):
        return self.status

    def getDensiteit(self):
        return self.densiteit

    # de cel houdt zijn eigen x-coördinaat bij, deze zal ingesteld worden door het speelveld want
    # de cellen worden daar getekend
    # de 5 is de onderlinge marge tussen de cellen in de klasse Speelveld
    def setX(self, x):
        self.xOrigin = x
        self.xCoordinaatLinkerBovenhoek = self.xOrigin + ((self.zijdeCel + 5) * self.getKolom())

    # idem als de bovenliggende methode maar dan voor de y-coördinaat
    def setY(self, y):
        self.yOrigin = y
        self.yCoordinaatLinkerBovenhoek = self.yOrigin + ((self.zijdeCel + 5) * self.getRij())

    def isLevend(self):
        if self.status == 0 or self.status == 2:
            return True
        else:
            return False
