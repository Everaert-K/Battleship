import csv


class Boot:
    def __init__(self, type):
        self.type = type  # zie csv
        self.cellen = []
        self.dood = False
        self.ankerPunt = None
        self.lengte = None  # variabelen initaliseren uit de if lus
        self.breedte = None  # variabelen initaliseren uit de if lus
        self.aantalLevens = None  # variabelen initaliseren uit de if lus
        self.afbeelding = None  # variabelen initaliseren uit de if lus
        self.rotatie = None
        try:
            Boot = open('Boot.csv', 'r', encoding="windows-1252").read()  # zoekt of het bestand bestaat
        except:
            while Boot != "Boot.csv":  # produceert een error indien het bestand niet geopend is
                print("Kan het bestand", Boot, "niet openen")
        else:
            with open("Boot.csv") as csvfile:
                lezer = csv.reader(csvfile, delimiter=';')  # zet delimiter op ; en opend het bestand
                next(lezer)  # skipt de eerste rij, de hoofding
                for row in lezer:
                    if int(row[0]) == type:  # checkt het type boot dat aangemaakt moet worden
                        self.lengte = int(row[1])
                        self.breedte = int(row[2])
                        self.aantalLevens = int(row[3])
                        self.afbeelding = row[4]  # image naam

    def containsCel(self, cel):
        if cel in self.cellen:
            return True
        else:
            return False

    # geeft False terug als boot niet in veld past
    def setPositie(self, ankerPunt, rotatie, boot, gekozenCellenMetRichting):
        self.ankerPunt = ankerPunt
        self.rotatie = rotatie  # 0 standaard naar boven, 1 naar rechts,....
        self.cellen = []
        if ankerPunt.getStatus() == 2:
            return False
        else:
            self.cellen.append(ankerPunt)
            buur = ankerPunt
        count = 1
        while count < self.lengte:
            if buur.getBuur(rotatie) is not None and buur.getBuur(rotatie).getStatus() != 2:
                buur = buur.getBuur(rotatie)
                self.cellen.append(buur)
                count += 1
            else:
                self.cellen = []
                return False
        if self.geldigePositieBoot(boot, gekozenCellenMetRichting):
            return True
        return False

    def geraakt(self):
        self.aantalLevens -= 1
        if self.aantalLevens <= 0:
            self.dood = True

    def isDood(self):
        return self.dood

    def getAantalLevens(self):
        return self.aantalLevens

    def getType(self):
        return self.type

    def getAfbeelding(self):
        return self.afbeelding

    def getAnkerPunt(self):
        return self.ankerPunt

    def getCellenVanBoot(self):
        return self.cellen

    def getRotatie(self):
        return self.rotatie

    def getLengte(self):
        return self.lengte

    @staticmethod
    def initPakket(keuze):
        lijstBoten = [None]*5
        if keuze == 0:
            lijstBoten[0] = Boot(5)
            lijstBoten[1] = Boot(3)
            lijstBoten[2] = Boot(2)
            lijstBoten[3] = Boot(2)
            lijstBoten[4] = Boot(1)
        elif keuze == 1:
            lijstBoten[0] = Boot(4)
            lijstBoten[1] = Boot(2)
            lijstBoten[2] = Boot(2)
            lijstBoten[3] = Boot(1)
            lijstBoten[4] = Boot(1)
        elif keuze == 2:
            lijstBoten[0] = Boot(5)
            lijstBoten[1] = Boot(4)
            lijstBoten[2] = Boot(4)
            lijstBoten[3] = Boot(3)
            lijstBoten[4] = Boot(2)
        return lijstBoten

    def initStatus(self):
        for i in range(len(self.cellen)):
            self.cellen[i].setStatus(2)

    @staticmethod
    def vulDictionaryAanMetCelEnRichting(dictionary, cel, richting, lengte):
        nummerCel = cel.getNummer()
        dictionary[nummerCel] = richting
        ankerCel = cel
        for x in range(lengte-1):
            nummerCel = ankerCel.getBuur(richting).getNummer()
            dictionary[nummerCel] = richting
            ankerCel = ankerCel.getBuur(richting)

    def geldigePositieBoot(self, boot, gekozenCellenMetRichting):
        lengte = boot.getLengte()
        self.vulDictionaryAanMetCelEnRichting(gekozenCellenMetRichting, boot.getAnkerPunt(), boot.getRotatie(), lengte)
        ankercel = boot.getAnkerPunt()
        lengteBoot = boot.getLengte()
        richtingBoot = boot.getRotatie()
        for celletje in ankercel.getBuren():
            if celletje is not None:
                if celletje.getStatus() == 2 and (gekozenCellenMetRichting.get(celletje.getNummer()) == richtingBoot or gekozenCellenMetRichting.get(celletje.getNummer()) == (richtingBoot+2) % 4):
                    return False
        cel = ankercel
        for x in range(lengteBoot-1):
            cel = cel.getBuur(richtingBoot)
            for celletje in cel.getBuren():
                if celletje is not None:
                    if celletje.getStatus() == 2 and (gekozenCellenMetRichting.get(celletje.getNummer()) == richtingBoot or gekozenCellenMetRichting.get(celletje.getNummer()) == (richtingBoot+2) % 4):
                        return False
        return True