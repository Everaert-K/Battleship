from Cel_class import Cel
from Boot_class import Boot
from Grid_class import Grid
from Speler_class import Speler
from random import randint


class Computer(Speler):
    def __init__(self, tegenstander):
        # print("Computer gemaakt")
        Speler.__init__(self)
        self.moeilijkheid = 1
        self.eerstGeraakteCel = None
        self.laatstGeraakteCel = None
        self.zoekmodus = True
        self.tegenstander = tegenstander
        self.pariteitCellen = []
        self.initPariteitCellen(2)
        self.schietRichting = None
        self.cellenSchiet0 = self.tegenstander.getGrid().getCellen()
        self.aantalBotenVanlengte = {5: 1, 4: 2, 3: 3, 2: 4}

    def lijstCellenHoogsteDensiteit(self):
        list = []
        try:
            i = 0
            while not self.pariteitCellen[i].isLevend():
                i += 1
            max = self.pariteitCellen[i].getDensiteit()
        except:
            self.pariteitCellen = []
            self.pariteitCellen = self.tegenstander.getGrid().getCellen()
            i = 0
            while not self.pariteitCellen[i].isLevend():
                i += 1
            max = self.pariteitCellen[i].getDensiteit()
        print("Lengte pariteitcellen = " + str(len(self.pariteitCellen)))
        for i in range(len(self.pariteitCellen)):  # lijst maken met alle cellen van hoogste densiteit
            # print("densiteit cel = " + str(self.pariteitCellen[i].getDensiteit()))
            if self.pariteitCellen[i].getDensiteit() > max and self.pariteitCellen[i].isLevend():
                max = self.pariteitCellen[i].getDensiteit()
                list = []
                list.append(self.pariteitCellen[i])
            elif self.pariteitCellen[i].getDensiteit() == max and self.pariteitCellen[i].isLevend():
                list.append(self.pariteitCellen[i])
        print("Max = " + str(max))
        print("Lengte list = " + str(len(list)))
        return list

    # kijkt in alle richtingen van de laatstgeraaktecel waar er het meeste lege cellen zijn
    def bepaalInitiëleSchietrichting(self, buren):
        meesteLegeCellen = 0
        list = []
        for i in range(len(buren)):
            legeCellenInRichting = 0
            if buren[i] is not None and buren[i].isLevend():
                laatsteBuur = buren[i]
                legeCellenInRichting += 1
                while laatsteBuur.getBuur(i) is not None and laatsteBuur.getBuur(i).isLevend():
                    legeCellenInRichting += 1
                    laatsteBuur = laatsteBuur.getBuur(i)
                if legeCellenInRichting > meesteLegeCellen:
                    meesteLegeCellen = legeCellenInRichting
                    list = []
                    list.append(i)
                elif legeCellenInRichting == meesteLegeCellen:
                    list.append(i)
        # als er meer dan 1 richting is die de meeste cellen heeft wordt willekeurig 1 van die richtingen gekozen,
        # hierdoor is het algoritme net iets minder voorspelbaar
        if len(list) > 0:
            x = randint(0, len(list)-1)
            self.schietRichting = list[x]

    # voorbeeld van pariteit is te zien in de link op de wiki
    def initPariteitCellen(self, getal):
        for i in range(10):
            if i % getal == 0:
                for x in range(10):
                    if x % getal == 0:
                        self.pariteitCellen.append(self.tegenstander.getGrid().getCel(i, x))
            elif i % getal == 1:
                for x in range(10):
                    if x % getal == 1:
                        self.pariteitCellen.append(self.tegenstander.getGrid().getCel(i, x))
            elif i % getal == 2:
                for x in range(10):
                    if x % getal == 2:
                        self.pariteitCellen.append(self.tegenstander.getGrid().getCel(i, x))
            elif i % getal == 3:
                for x in range(10):
                    if x % getal == 3:
                        self.pariteitCellen.append(self.tegenstander.getGrid().getCel(i, x))
            elif i % getal == 4:
                for x in range(10):
                    if x % getal == 4:
                        self.pariteitCellen.append(self.tegenstander.getGrid().getCel(i, x))
        """for i in range(len(self.pariteitCellen)-1):
                    print(self.pariteitCellen[i])"""

    def updateModusEnTargetParameters(self, cel, gezonken):
        if cel.getStatus() == 3 and gezonken is False:
            self.eerstGeraakteCel = cel
            self.laatstGeraakteCel = self.eerstGeraakteCel
            self.zoekmodus = False
        elif cel.getStatus() == 1 or gezonken is True:
            self.zoekmodus = True

    def updateModusEnSchietrichting(self,gezonken, buren):
        if gezonken:
            self.zoekmodus = True
            self.schietRichting = None
        else:
            if buren[self.schietRichting].getStatus() == 3:
                self.laatstGeraakteCel = buren[self.schietRichting]
            else:
                if self.laatstGeraakteCel == self.eerstGeraakteCel:
                    self.schietRichting = None
                else:
                    self.schietRichting = (self.schietRichting+2) % 4
                    self.laatstGeraakteCel = self.eerstGeraakteCel
                    print("Richting veranderd, richting = " + str(self.schietRichting))

    def schietInRichtingVanGeraakteCel(self, buren, geschoten):
        cel = None
        for i in range(len(buren)):
            buren = self.laatstGeraakteCel.getBuren()
            if (buren[i] is not None and buren[i].getStatus() != 1) and geschoten is False:
                while buren[i] != None and buren[i].getStatus() == 3:
                    buren = buren[i].getBuren()
                if buren[i] != None and buren[i].getStatus() != 1:
                    gezonken = self.vuur(buren[i])
                    geschoten = True
                    if buren[i].getStatus() == 3 and gezonken is not True:
                        self.eerstGeraakteCel = buren[i]
                        self.laatstGeraakteCel = self.eerstGeraakteCel
                        self.zoekmodus = False
                    elif buren[i].getStatus() == 1 or gezonken is True:
                        self.zoekmodus = True
                    cel = buren[i]
        return cel

    def specialeGevallenRichtingVeranderen(self, buren):
        print("self.schietrichting = " + str(self.schietRichting))
        if buren[self.schietRichting] is None or not buren[self.schietRichting].isLevend():
            print("Kan niet in deze richting schieten")
            if buren[self.schietRichting] is not None and buren[self.schietRichting].getStatus() != 1:
                print("Status buur in huidige schietrichting = " + str(buren[self.schietRichting].getStatus()))
                if buren[self.schietRichting].getStatus() == 3 and (self.eerstGeraakteCel.getBuur((self.schietRichting+2) % 4) is None or self.eerstGeraakteCel.getBuur((self.schietRichting+2) % 4).getStatus() == 1):
                    tempCel = buren[self.schietRichting]
                    print("tempCel = " + str(tempCel.getNummer()))
                    while tempCel.getStatus() == 3:
                        buren = tempCel.getBuren()
                        tempCel = tempCel.getBuur(self.schietRichting)
                elif buren[self.schietRichting].getStatus() == 3 and (self.eerstGeraakteCel.getBuur((self.schietRichting + 2) % 4) is not None or self.eerstGeraakteCel.getBuur((self.schietRichting+2) % 4).isLevend()):
                    self.schietRichting = (self.schietRichting+2) % 4
                    self.laatstGeraakteCel = self.eerstGeraakteCel
                    buren = self.laatstGeraakteCel.getBuren()
                    print("Richting veranderd, richting = " + str(self.schietRichting))
            else:
                self.schietRichting = (self.schietRichting+2) % 4
                self.laatstGeraakteCel = self.eerstGeraakteCel
                buren = self.laatstGeraakteCel.getBuren()
                print("Richting veranderd, richting = " + str(self.schietRichting))
                while buren[self.schietRichting].getStatus() == 3:
                    buren = buren[self.schietRichting].getBuren()
        return buren

    def schietInRichting(self, buren):
        buren = self.specialeGevallenRichtingVeranderen(buren)
        gezonken = self.vuur(buren[self.schietRichting])
        cel = buren[self.schietRichting]
        self.updateModusEnSchietrichting(gezonken, buren)
        print("Gezonken = " + str(gezonken))
        return cel

    def schietEerstLevendeBuur(self):
        buren = self.laatstGeraakteCel.getBuren()
        geschoten = False
        cel = None
        for i in range(4):
            if geschoten is False:
                if buren[i] is not None and buren[i].isLevend():
                    gezonken = self.vuur(buren[i])
                    cel = buren[i]
                    geschoten = True
                    if buren[i].getStatus() == 3 and gezonken is False:
                        self.eerstGeraakteCel = buren[i]
                        self.laatstGeraakteCel = self.eerstGeraakteCel
                        self.zoekmodus = False
                    elif gezonken is True:
                        self.zoekmodus = True
        return cel

    def schietRandomCel(self):
        x = randint(0, len(self.cellenSchiet0)-1)
        while not self.cellenSchiet0[x].isLevend():
            x = randint(0, len(self.cellenSchiet0)-1)
        gezonken = self.vuur(self.cellenSchiet0[x])
        self.updateModusEnTargetParameters(self.cellenSchiet0[x], gezonken)
        cel = self.cellenSchiet0[x]
        return cel

    def schiet(self):
        if self.moeilijkheid == 0:
            cel = self.algoritmeEasy()
        elif self.moeilijkheid == 1:
            cel = self.algoritmeAverage()
        elif self.moeilijkheid == 2:
            cel = self.algoritmeHard()
        return cel

    def algoritmeHard(self):
        print("\nAlgoritme start:")
        cel = None
        if self.zoekmodus:
            print("Zoekmodus")
            list = self.lijstCellenHoogsteDensiteit()
            if len(list) > 0:
                x = randint(0, len(list)-1)
                gezonken = self.vuur(list[x])
                self.updateModusEnTargetParameters(list[x], gezonken)
                cel = list[x]
        else:
            print("Targetmodus")
            buren = self.laatstGeraakteCel.getBuren()
            if self.schietRichting is None:
                self.bepaalInitiëleSchietrichting(buren)
                print("Schietrichting = " + str(self.schietRichting))
                if self.schietRichting is None:
                    # deze if wordt getriggered in het geval dat er een cel werd geraakt waarvan alle buren al beschoten
                    # zijn en de boot nog niet gezonken is, dit geval heeft een heel kleine kans op voorkomen,
                    # er wordt geschoten in een richting waar er al geraakte cellen waren als dit niet lukt wordt een random schot gevuurd
                    print("Speciaal geval")
                    geschoten = False
                    cel = self.schietInRichtingVanGeraakteCel(buren, geschoten)
                    if geschoten is False:
                        x = randint(0, len(self.pariteitCellen)-1)
                        gezonken = self.vuur(self.pariteitCellen[x])
                        self.updateModusEnTargetParameters(self.pariteitCellen[x], gezonken)
                        cel = self.pariteitCellen[x]
                else:
                    cel = self.schietInRichting(buren)
            else:
                cel = self.schietInRichting(buren)
        print("Cel geschoten met nummer: " + str(cel.getNummer()))
        print("Einde Algoritme")
        return cel

    def algoritmeAverage(self):
        print("\nAlgoritme start:")
        cel = None
        if self.zoekmodus:
            print("Zoekmodus")
            cel = self.schietRandomCel()
        else:
            print("Targetmodus")
            buren = self.laatstGeraakteCel.getBuren()
            if self.schietRichting is None:
                self.bepaalInitiëleSchietrichting(buren)
                print("Schietrichting = " + str(self.schietRichting))
                if self.schietRichting is None:
                    # deze if wordt getriggered in het geval dat er een cel werd geraakt waarvan alle buren al beschoten
                    # zijn en de boot nog niet gezonken is, dit geval heeft een heel kleine kans op voorkomen,
                    # er wordt geschoten in een richting waar er al geraakte cellen waren als dit niet lukt wordt een random schot gevuurd
                    print("Speciaal geval")
                    geschoten = False
                    cel = self.schietInRichtingVanGeraakteCel(buren, geschoten)
                    if geschoten is False:
                        x = randint(0, len(self.pariteitCellen) - 1)
                        gezonken = self.vuur(self.pariteitCellen[x])
                        self.updateModusEnTargetParameters(self.pariteitCellen[x], gezonken)
                        cel = self.pariteitCellen[x]
                else:
                    cel = self.schietInRichting(buren)
            else:
                cel = self.schietInRichting(buren)
        print("Cel geschoten met nummer: " + str(cel.getNummer()))
        print("Einde Algoritme")
        return cel

    def algoritmeEasy(self):
        print("\nAlgoritme start:")
        cel = None
        if self.zoekmodus:
            print("Zoekmodus")
            cel = self.schietRandomCel()
        else:
            print("Targetmodus")
            cel = self.schietEerstLevendeBuur()
            if cel is None:
                self.laatstGeraakteCel = self.eerstGeraakteCel
                cel = self.schietEerstLevendeBuur()
            if cel is None:
                self.zoekmodus = True
                cel = self.schietRandomCel()
        print("Cel geschoten met nummer: " + str(cel.getNummer()))
        print("Einde Algoritme")
        return cel

    def setMoeilijkheid(self, moeilijkheid):
        self.moeilijkheid = moeilijkheid
        print("Moeilijkheid = " + str(self.moeilijkheid))

    """def bepaalMinimumLengte(self,boten):
        minimumLengte = 6
        for boot in boten:
            if boot.getLengte() < minimumLengte:
                minimumLengte = boot.getLengte()
        return minimumLengte

    def checkGenoegPlaatsVoorBoot(self,cel):
        mogelijk = True
        minimumLengte = self.bepaalMinimumLengte(self.botenTegenstander) # nog in te vullen
        aantalVrijePlaatsenBoven = 0
        aantalVrijePlaatsenRechts = 0
        aantalVrijePlaatsenOnder = 0
        aantalVrijePlaatsenLinks = 0

        buur = cel
        for x in range(1,minimumLengte):
           if buur is None or buur.getStatus()==1 or buur.getStatus()==3:
               break
           else:
               aantalVrijePlaatsenBoven+=1
               buur = buur.getBuur(0)
        buur = cel
        for x in range(1,minimumLengte):
           if buur is None or buur.getStatus()==1 or buur.getStatus()==3:
               break
           else:
               aantalVrijePlaatsenRechts+=1
               buur = buur.getBuur(1)
        buur = cel
        for x in range(1,minimumLengte):
           if buur is None or buur.getStatus()==1 or buur.getStatus()==3:
               break
           else:
               aantalVrijePlaatsenOnder+=1
               buur = buur.getBuur(2)
        buur = cel
        for x in range(1,minimumLengte):
           if buur is None or buur.getStatus()==1 or buur.getStatus()==3:
               break
           else:
               aantalVrijePlaatsenLinks+=1
               buur = buur.getBuur(3)

        aantalOverHorizontaal = aantalVrijePlaatsenBoven+aantalVrijePlaatsenOnder
        aantalOverVerticaal = aantalVrijePlaatsenLinks+aantalVrijePlaatsenRechts
        if minimumLengte > aantalOverHorizontaal or minimumLengte > aantalOverVerticaal:
            return False
        else:
            return True"""

    """def schietTest(self): 
            print("\nAlgoritme start:")
            cel = None
            if self.zoekmodus:
                print("Zoekmodus")
                list = []
                max = -1000  # laag genoeg dat een densiteit hier nooit onder gaat
                print("Lengte pariteitcellen = " + str(len(self.pariteitCellen)))
                for i in range(len(self.pariteitCellen)):  # lijst maken met alle cellen van hoogste densiteit
                    # print("densiteit cel = " + str(self.pariteitCellen[i].getDensiteit()))
                    if self.pariteitCellen[i].getDensiteit() > max and self.pariteitCellen[i].isLevend():
                        max = self.pariteitCellen[i].getDensiteit()
                        list = []
                        list.append(self.pariteitCellen[i])
                    elif self.pariteitCellen[i].getDensiteit() == max and self.pariteitCellen[i].isLevend():
                        list.append(self.pariteitCellen[i])
                print("Max = " + str(max))
                print("Lengte list = " + str(len(list)))
                # checken of len(list) > 0, anders gewoon random schieten
                x = randint(0, len(list) - 1)
                # print(x)
                # print(list[x])
                while self.checkGenoegPlaatsVoorBoot(list[x]) == False:
                    x = randint(0,len(list)-1)
                gezonken = self.vuur(list[x])
                # print(list[x])
                if list[x].getStatus() == 3 and gezonken is False:
                    self.eerstGeraakteCel = list[x]
                    self.laatstGeraakteCel = self.eerstGeraakteCel
                    self.zoekmodus = False
                cel = list[x]
            else:  # niet af
                print("Targetmodus")
                buren = self.laatstGeraakteCel.getBuren()
                if self.schietRichting is None:
                    meesteLegeCellen = 0
                    list = []
                    for i in range(len(buren)):
                        legeCellenInRichting = 0
                        if buren[i] is not None and buren[i].isLevend():
                            laatsteBuur = buren[i]
                            legeCellenInRichting += 1
                            while laatsteBuur.getBuur(i) != None and laatsteBuur.getBuur(i).isLevend():
                                legeCellenInRichting += 1
                                laatsteBuur = laatsteBuur.getBuur(i)
                            if legeCellenInRichting > meesteLegeCellen:
                                meesteLegeCellen = legeCellenInRichting
                                list = []
                                list.append(i)
                            elif legeCellenInRichting == meesteLegeCellen:
                                list.append(i)
                    if len(list) > 0:
                        x = randint(0, len(list) - 1)
                        self.schietRichting = list[x]
                    # deze if wordt getriggered in het geval dat er een cel werd geraakt waarvan alle buren al beschoten
                    # zijn en de boot nog niet gezonken, dit geval heeft een heel kleine kans op voorkomen,
                    # er wordt dan gewoon een schot in het niets gevuurd
                    print("Schietrichting = " + str(self.schietRichting))
                    if self.schietRichting is None:
                        print("Speciaal geval")
                        geschoten = False
                        for i in range(len(buren)):
                            if (buren[i] is not None and buren[i].getStatus() != 1) and geschoten is False:
                                while buren[i].getBuur(i).getStatus() == 3:
                                    buren[i] = buren[i].getBuur(i)
                                if buren[i].getBuur(i).getStatus() != 1:
                                    gezonken = self.vuur(buren[i].getBuur(i))
                                    geschoten = True
                                    if buren[i].getBuur(i).getStatus() == 3 and gezonken is not True:
                                        self.eerstGeraakteCel = buren[i].getBuur(i)
                                        self.laatstGeraakteCel = self.eerstGeraakteCel
                                        self.zoekmodus = False
                                    elif buren[i].getBuur(i).getStatus() == 1 or gezonken is True:
                                        self.zoekmodus = True
                                    cel = buren[i].getBuur(i)
                        if geschoten is False:
                            x = randint(0, len(self.pariteitCellen) - 1)
                            gezonken = self.vuur(self.pariteitCellen[x])
                            if self.pariteitCellen[x].getStatus() == 3 and gezonken is not True:
                                self.eerstGeraakteCel = self.pariteitCellen[x]
                                self.laatstGeraakteCel = self.eerstGeraakteCel
                                self.zoekmodus = False
                            elif self.pariteitCellen[x].getStatus() == 1 or gezonken is True:
                                self.zoekmodus = True
                            cel = self.pariteitCellen[x]
                    else:
                        if buren[self.schietRichting] == None or not buren[self.schietRichting].isLevend():
                            print("AAA")
                            if buren[self.schietRichting] != None and buren[self.schietRichting].getStatus() != 1:
                                print("BBB")
                                if buren[self.schietRichting].getStatus() == 3 and (self.eerstGeraakteCel.getBuur(
                                        (self.schietRichting + 2) % 4) == None or self.eerstGeraakteCel.getBuur(
                                        (self.schietRichting + 2) % 4) == 1):
                                    tempCel = buren[self.schietRichting]
                                    print("tempCel = " + str(tempCel.getNummer()))
                                    while tempCel.getStatus() == 3:
                                        tempCel = tempCel.getBuur(self.schietRichting)
                                    buren = tempCel.getBuren()
                            else:
                                self.schietRichting = (self.schietRichting + 2) % 4
                                self.laatstGeraakteCel = self.eerstGeraakteCel
                                buren = self.laatstGeraakteCel.getBuren()
                                print("Richting veranderd lijn 154, richting = " + str(self.schietRichting))
                                while buren[self.schietRichting].getStatus() == 3:
                                    buren[self.schietRichting] = buren[self.schietRichting].getBuur(self.schietRichting)
                        gezonken = self.vuur(buren[self.schietRichting])
                        cel = buren[self.schietRichting]
                        if gezonken:
                            self.zoekmodus = True
                            self.schietRichting = None
                        else:
                            if buren[self.schietRichting].getStatus() == 3:
                                self.laatstGeraakteCel = buren[self.schietRichting]
                            else:
                                if self.laatstGeraakteCel == self.eerstGeraakteCel:
                                    self.schietRichting = None
                                else:
                                    self.schietRichting = (self.schietRichting + 2) % 4
                                    self.laatstGeraakteCel = self.eerstGeraakteCel
                                    print("Richting veranderd lijn 148, richting = " + str(self.schietRichting))
                else:
                    print("self.schietrichting = " + str(self.schietRichting))
                    if buren[self.schietRichting] == None or not buren[self.schietRichting].isLevend():
                        print("AAA")
                        if buren[self.schietRichting] != None and buren[self.schietRichting].getStatus() != 1:
                            print("BBB " + str(buren[self.schietRichting].getStatus()))
                            # print("CCC " + str(self.eerstGeraakteCel.getBuur((self.schietRichting+2)%4).getStatus()))
                            if buren[self.schietRichting].getStatus() == 3 and (self.eerstGeraakteCel.getBuur(
                                    (self.schietRichting + 2) % 4) == None or self.eerstGeraakteCel.getBuur(
                                    (self.schietRichting + 2) % 4).getStatus() == 1):
                                tempCel = buren[self.schietRichting]
                                print("tempCel = " + str(tempCel.getNummer()))
                                while tempCel.getStatus() == 3:
                                    buren = tempCel.getBuren()
                                    tempCel = tempCel.getBuur(self.schietRichting)
                        else:
                            self.schietRichting = (self.schietRichting + 2) % 4
                            self.laatstGeraakteCel = self.eerstGeraakteCel
                            buren = self.laatstGeraakteCel.getBuren()
                            print("Richting veranderd lijn 154, richting = " + str(self.schietRichting))
                            while buren[self.schietRichting].getStatus() == 3:
                                buren[self.schietRichting] = buren[self.schietRichting].getBuur(self.schietRichting)
                    gezonken = self.vuur(buren[self.schietRichting])
                    cel = buren[self.schietRichting]
                    print("Gezonken = " + str(gezonken))
                    if gezonken:
                        self.zoekmodus = True
                        self.schietRichting = None
                    else:
                        if buren[self.schietRichting].getStatus() == 3:
                            self.laatstGeraakteCel = buren[self.schietRichting]
                        else:
                            if self.laatstGeraakteCel == self.eerstGeraakteCel:
                                self.schietRichting = None
                            else:
                                self.schietRichting = (self.schietRichting + 2) % 4
                                self.laatstGeraakteCel = self.eerstGeraakteCel
                                print("Richting veranderd lijn 170, richting = " + str(self.schietRichting))
            print("Cel geschoten met nummer: " + str(cel.getNummer()))
            # print(self.tegenstander.getGrid().toString(1))
            print("Einde Algoritme")
            return cel"""
