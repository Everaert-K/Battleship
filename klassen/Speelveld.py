import pygame
import sys
from random import randint
from pygame.locals import *
from Computer_class import Computer
from Speler_class import Speler
from Boot_class import Boot
from Cel_class import Cel
from Knop import Knop
from SaveLoad_class import SaveLoad
from Grafische_hulpklasse import Hulpklasse
from Music import Music


class Speelveld:
    # verschillende kleuren die nodig kunnen zijn
    WIT = (255, 255, 255)
    ZWART = (0, 0, 0)
    GRIJS = (192, 192, 192)
    DONKERGRIJS = (126, 126, 126)
    BLAUWGRIJS = (148, 150, 173)

    def __init__(self, scherm, breedte, hoogte):
        pygame.init()  # de gui wordt aangemaakt
        self.hulp = Hulpklasse(scherm, breedte, hoogte)

        # deze opdracht stelt het scherm in (fullscreen)
        self.scherm = scherm

        self.menu = None
        self.muziek = Music()

        # deze variabelen bevatten de afmetingen van het scherm
        self.breedte = breedte
        self.hoogte = hoogte

        # achtergrond wordt ingeladen en bijgehouden
        self.achtergrond = pygame.image.load('img/back.jpg').convert()

        # Om bijvoorbeeld de fps in te stellen
        self.klok = pygame.time.Clock()

        # deze variabelen definiëren de grootte van de cellen en de plaats ertussen
        self.cel_breedte = 50
        self.cel_hoogte = 50
        self.marge = 5

        # hier creëren we 2 2D arrays om de grids te kunnen voorstellen (speler = linkse grid en computer = rechtse)
        # de derde dient om de vakjes te laten kleuren wanneer een speler de boten handmatig plaatst
        self.grid_speler = []
        self.grid_computer = []
        self.eig_grid_speler = []
        for i in range(10):
            self.grid_speler.append([])
            self.grid_computer.append([])
            self.eig_grid_speler.append([])

        for rij in range(10):
            for kolom in range(10):
                self.eig_grid_speler[kolom].append(Knop(self.GRIJS, None, None, None, None))

        self.beurt_speler_grid = Knop(self.WIT, None,None,None,None, False)
        self.beurt_computer_grid = Knop(self.WIT, None, None, None, None, False)

        # info voor getaangekliktecel
        self.res = []

        # de grids worden opgevuld en de foto's voor de cellen worden geladen
        self.initGrids()
        self.foto_cellen = [pygame.transform.scale(pygame.image.load('img/cel/mis.png'), (self.cel_breedte, self.cel_hoogte)),
                            pygame.transform.scale(pygame.image.load('img/cel/raak.png'), (self.cel_breedte, self.cel_hoogte))]

        # de grenzen van de grids worden bijgehouden in een array in deze volgorde: links rechts boven onder
        self.grenzen_speler = [self.grid_speler[0][0].left, self.grid_speler[9][0].right, self.grid_speler[9][0].top, self.grid_speler[9][9].bottom]
        self.grenzen_computer = [self.grid_computer[0][0].left, self.grid_computer[9][0].right, self.grid_computer[9][0].top, self.grid_computer[9][9].bottom]
        self.gridL = Rect(self.grenzen_speler[0],self.grenzen_speler[2], self.grenzen_speler[1]-self.grenzen_speler[0], self.grenzen_speler[3]-self.grenzen_speler[3])

        # eigenschappen voor het eindscherm
        self.eigenschappen_knoppen = [Knop(self.DONKERGRIJS, None, None, None, None),
                                      Knop(self.DONKERGRIJS, None, None, None, None),
                                      Knop(self.DONKERGRIJS, None, None, None, None)]

        # de grids, de speler en de computer worden ingesteld
        self.sp = Speler()
        self.cm = Computer(self.sp)
        self.sp.setTegenstander(self.cm)
        self.getekendeBoten = []
        self.stelCoordinatenCellenIn()
        self.automatischPlaatsen = False
        self.beurtSpeler = True
        self.boot_keuze = 0
        self.afgelopen = 0
        self.final_shot = None
        self.safeBoten = []
        self.safeFoto = []
        pygame.display.update()

    # hier worden de 2 2D arrays opgevuld met de getekende cellen, zo kunnen we checken op een muisklik
    # deze mogen ook maar 1 keer aangemaakt worden zodat we correct de data kunnen bijhouden over elke cel
    def initGrids(self):
        for rij in range(10):
            for kolom in range(10):
                self.grid_speler[kolom].append(pygame.draw.rect(self.scherm, self.GRIJS,
                                                                [(self.marge + self.cel_breedte) * kolom + self.marge +
                                                                    (self.breedte / 7.0),
                                                                 (self.marge + self.cel_hoogte) * (
                                                                             rij + 1) + self.marge + self.hoogte / 5.0,
                                                                 self.cel_breedte, self.cel_hoogte]))

                self.grid_computer[kolom].append(pygame.draw.rect(self.scherm, self.GRIJS,
                                                                 [(self.marge + self.cel_breedte) * kolom + self.marge +
                                                                  (2.81 * self.breedte / 5),
                                                                   (self.marge + self.cel_hoogte) * (
                                                                    rij + 1) + self.marge + self.hoogte / 5.0,
                                                                   self.cel_breedte, self.cel_hoogte]))

    # alle componenten van het speelveld worden getekend
    # handig wanneer we terugkeren uit het scherm met de regels of wanneer de gui gestart wordt
    def tekenSpeelveld(self):
        self.scherm.blit(self.achtergrond, [0, 0])
        self.tekenGridsOpnieuw()
        self.initTeksten()
        self.knoppen()
        self.tekenCoordinaten()
        self.tekenBoten()

    # hier worden de coördinaten rond de grids getekend
    # bepaling van de locatie waar er moet getekend worden, gebeurt op basis van de grids zelf
    def tekenCoordinaten(self):
        begin = ord('A')  # om gemakkelijk de letters te kunnen printen
        lettergrootte = 17  # grootte van de tekst, dan moet het enkel hier aangepast worden
        lettertype = 'Verdana'

        for i in range(10):
            # kolom rechts naast gridComputer + letters in het midden van de cel printen
            tijdelijk = pygame.draw.rect(self.scherm, self.beurt_speler_grid.get_kleur(),
                                         [self.grid_computer[9][0].right + self.marge,
                                          self.grid_computer[9][0].top - self.marge + i * (
                                                  self.cel_hoogte + self.marge),
                                          self.cel_breedte, self.cel_hoogte + self.marge])
            self.schrijfInMiddenVanCel(tijdelijk, chr(begin + i), lettertype, lettergrootte)

            # de rij boven gridComputer + getallen in het midden van de cel printen
            tijdelijk2 = pygame.draw.rect(self.scherm, self.beurt_speler_grid.get_kleur(),
                                          [self.grid_computer[0][0].left + i * (self.cel_breedte + self.marge),
                                           self.grid_computer[0][0].top - self.marge - self.cel_breedte,
                                           self.cel_breedte + self.marge, self.cel_hoogte])
            self.schrijfInMiddenVanCel(tijdelijk2, str(i + 1), lettertype, lettergrootte)

            # kolom links naast gridSpeler + letters in het midden van de cel printen
            tijdelijk3 = pygame.draw.rect(self.scherm, self.beurt_computer_grid.get_kleur(),
                                          [self.grid_speler[0][0].left - self.cel_breedte - self.marge,
                                           (self.marge + self.cel_hoogte) * i + self.grid_speler[0][
                                               0].top - self.marge,
                                           self.cel_breedte, self.cel_hoogte + self.marge])
            self.schrijfInMiddenVanCel(tijdelijk3, chr(begin + i), lettertype, lettergrootte)

            # rij boven gridSpeler + getallen in het midden van de cel printen
            tijdelijk4 = pygame.draw.rect(self.scherm, self.beurt_computer_grid.get_kleur(), [
                self.grid_speler[0][0].left - self.marge + i * (self.cel_breedte + self.marge),
                self.grid_computer[0][0].top - self.marge - self.cel_breedte,
                self.cel_breedte + self.marge, self.cel_hoogte])
            self.schrijfInMiddenVanCel(tijdelijk4, str(i + 1), lettertype, lettergrootte)

        # de leegte links bovenaan opvullen in de grid van de speler
        pygame.draw.rect(self.scherm, self.beurt_computer_grid.get_kleur(),
                         [self.grid_speler[0][0].left - self.marge - self.cel_breedte,
                          self.grid_speler[0][0].top - self.marge - self.cel_hoogte,
                          self.cel_breedte, self.cel_hoogte])

        # de leegte rechts bovenaan opvullen in de grid van de computer
        pygame.draw.rect(self.scherm, self.beurt_speler_grid.get_kleur(),
                         [self.grid_computer[9][0].right + self.marge,
                          self.grid_computer[9][0].top - self.cel_hoogte - self.marge,
                          self.cel_breedte, self.cel_hoogte])

    # hier worden de afsluit- en hulpknop getekend
    # hier moet er convert_alpha() gebruikt worden omdat het png-bestanden zijn
    # we houden de afsluit- en hulpknop bij zodat we kunnen checken of erop geklikt is
    def knoppen(self):
        afsluitknop = pygame.image.load("img/afsluitknop.png").convert_alpha()
        afsluitknop_geschaald = pygame.transform.scale(afsluitknop, (30, 30))
        self.close = self.scherm.blit(afsluitknop_geschaald, (self.breedte - 50, 30))

        hulpknop = pygame.image.load("img/hulpknop.png").convert_alpha()
        hulpknop_geschaald = pygame.transform.scale(hulpknop, (22, 22))
        self.help = self.scherm.blit(hulpknop_geschaald, (self.breedte - 90, 35))

    # deze methode is nodig want telkens we initGrids aanroepen,
    # worden er nieuwe cellen toegevoegd aan grid_speler en grid_computer en dit is niet de bedoeling.
    # deze methode zullen we dan gebruiken om de bestaande cellen opnieuw te tekenen
    # handig wanneer we bijvoorbeeld terugkeren uit het scherm met de regels
    def tekenGridsOpnieuw(self):
        pygame.draw.rect(self.scherm, self.beurt_computer_grid.get_kleur(),
                         (self.grenzen_speler[0] - 5, self.grenzen_speler[2] - 5, 550, 550))
        pygame.draw.rect(self.scherm, self.beurt_speler_grid.get_kleur(),
                         (self.grenzen_computer[0], self.grenzen_computer[2] - 5, 550, 550))
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(self.scherm, self.eig_grid_speler[j][i].get_kleur(), self.grid_speler[j][i])
                pygame.draw.rect(self.scherm, self.GRIJS, self.grid_computer[j][i])

    # Tekent de druppels, vlammen en kruisjes over de onderste boten opnieuw
    def tekenHitsEnMisses(self):
        for i in range(10):
            for j in range(10):
                cel = self.cm.getGrid().getCel(i, j)
                if cel.setFoto() is not None:
                    self.scherm.blit(self.foto_cellen[cel.setFoto()], self.grid_computer[j][i])
                cel2 = self.sp.getGrid().getCel(i, j)
                if cel2.setFoto() is not None:
                    self.scherm.blit(self.foto_cellen[cel2.setFoto()], self.grid_speler[j][i])
        for x in range(5 - len(self.cm.getBoten())):
            self.scherm.blit(pygame.transform.scale(pygame.image.load('img/afsluitknop.png'), (200, 200)),
                             (((self.breedte / 2) - 500) + x * 200, self.hoogte - 200))
        pygame.display.update()

    # De boten hertekenen (zowel op de grid als onderaan)
    def tekenBoten(self):
        self.witteRechthoek = pygame.draw.rect(self.scherm, self.WIT, ((self.breedte/2) - 500,
                                                                              self.hoogte-180, 1000, 160))
        for x in range(5):
            self.scherm.blit(pygame.transform.scale(pygame.image.load('img/boten/boot_beneden.png'), (200, 200)),
                             (((self.breedte/2) - 500) + x*200, self.hoogte-200))
        for b in range(len(self.getekendeBoten)):
            self.scherm.blit(self.getekendeBoten[b][0], self.getekendeBoten[b][1])

    # Hulpmethode om de cellen te doen veranderen van kleur afhankelijk vd situatie
    def kleurVakje(self, anker, richting, lengte, waarde=None):
        for x in range(lengte):
            if richting == 1:
                self.eig_grid_speler[anker.getKolom() + x][anker.getRij()].setFouteBoot(waarde)
            else:
                self.eig_grid_speler[anker.getKolom()][anker.getRij() + x].setFouteBoot(waarde)

    # om duplicated code te vermijden in de methode tekenCoordinaten
    # zo kunnen we handig tekst schrijven in het midden van een Rect
    def schrijfInMiddenVanCel(self, cel, tekst, lettertype, grootte):
        mijn_font = pygame.font.SysFont(lettertype, grootte)
        tekst = mijn_font.render(tekst, False, self.ZWART)
        text_rect = tekst.get_rect(center=cel.center)
        self.scherm.blit(tekst, text_rect)

    # versienummer printen, titel printen + titels van de grids printen adhv bovenstaande methode
    def initTeksten(self):
        font_versie = pygame.font.SysFont('Verdana', 20)
        versie = font_versie.render('Ver 3.7.11', False, self.WIT)
        self.scherm.blit(versie, (20, self.hoogte - 40))

        self.hulp.printGecentreerdeTekst('Georgia', 38, 'Battleship', self.WIT, (self.breedte / 2, 50))
        self.hulp.printGecentreerdeTekst('Verdana', 20, 'Your grid', self.WIT,
                                    (self.grid_speler[4][0].center[0], 185))  # positie adhv de middenste cel
        self.hulp.printGecentreerdeTekst('Verdana', 20, 'Computer\'s grid', self.WIT,
                                    (self.grid_computer[5][0].center[0], 185))  # positie adhv de middenste cel

    # methode om boten op het scherm te plaatsen
    def botenGrafischPlaatsen(self):
        botenSpeler = Boot.initPakket(self.boot_keuze)
        self.sp.setBoten(botenSpeler)
        botenComputer = Boot.initPakket(self.boot_keuze)
        self.cm.setBoten(botenComputer)
        self.sp.setBotenTegenstander()
        self.cm.setBotenTegenstander()
        self.cm.plaatsBoten()

        # in deze if worden de boten random geplaatst
        if self.automatischPlaatsen == 1:
            self.sp.plaatsBoten()
            for b in range(len(botenSpeler)):
                rotatie = botenSpeler[b].getRotatie()
                lengte = botenSpeler[b].getLengte()
                type = str(botenSpeler[b].getType())
                positieX = None
                positieY = None
                if rotatie == 1 or rotatie == 2:
                    positieX = self.grenzen_speler[0] + (botenSpeler[b].getAnkerPunt().getKolom() * (self.cel_breedte + self.marge))
                    positieY = self.grenzen_speler[2] + (botenSpeler[b].getAnkerPunt().getRij() * (self.cel_breedte + self.marge))
                elif rotatie == 3:
                    positieX = self.grenzen_speler[0] + (
                                (botenSpeler[b].getAnkerPunt().getKolom() - (lengte - 1)) * (self.cel_breedte + self.marge))
                    positieY = self.grenzen_speler[2] + (botenSpeler[b].getAnkerPunt().getRij() * (self.cel_breedte + self.marge))
                else:
                    positieX = self.grenzen_speler[0] + (botenSpeler[b].getAnkerPunt().getKolom() * (self.cel_breedte + self.marge))
                    positieY = self.grenzen_speler[2] + (
                                (botenSpeler[b].getAnkerPunt().getRij() - (lengte - 1)) * (self.cel_breedte + self.marge))
                lengteX = botenSpeler[b].getLengte() * self.cel_breedte + (botenSpeler[b].getLengte() - 1) * self.marge
                lengteY = self.cel_hoogte
                foto = pygame.image.load(botenSpeler[b].getAfbeelding())
                if rotatie == 0 or rotatie == 2:
                    temp = lengteX
                    lengteX = lengteY
                    lengteY = temp
                    foto = pygame.image.load("img/boten/boot" + type + "gedraaid.png")

                self.getekendeBoten.append([pygame.transform.scale(foto, (lengteX, lengteY)), (positieX, positieY)])
                self.safeFoto.append([type, rotatie])
                self.safeBoten.append([lengteX, lengteY, positieX, positieY])

                self.tekenGridsOpnieuw()
                self.tekenBoten()
                self.scherm.blit(pygame.transform.scale(foto, (lengteX, lengteY)), (positieX, positieY))
                pygame.display.update()
        # hier worden de boten handmatig geplaatst
        else:
            gekozenCellenMetRichting = {}
            for b in range(len(botenSpeler)):
                richting = 1
                positieX = self.grenzen_speler[0]
                lengteX = botenSpeler[b].getLengte() * self.cel_breedte + (botenSpeler[b].getLengte() - 1) * self.marge
                positieY = self.grenzen_speler[2]
                lengteY = self.cel_hoogte
                self.ankercel = Cel(0)
                foto = pygame.image.load(botenSpeler[b].getAfbeelding())
                self.scherm.blit(pygame.transform.scale(foto, (lengteX, lengteY)), (positieX, positieY))

                gepl = False
                while not gepl:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONDOWN:
                            x, y = event.pos
                            if self.close.collidepoint(x, y):
                                pygame.quit()
                                sys.exit()
                            elif self.help.collidepoint(x, y):
                                self.handelEventsRegelsAf()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                if positieX + lengteX < self.grenzen_speler[1]:
                                    positieX += (self.cel_breedte + self.marge)
                            elif event.key == pygame.K_LEFT:
                                if positieX > self.grenzen_speler[0]:
                                    positieX -= (self.cel_breedte + self.marge)
                            elif event.key == pygame.K_DOWN:
                                if positieY + lengteY < self.grenzen_speler[3]:
                                    positieY += (self.cel_breedte + self.marge)
                            elif event.key == pygame.K_UP:
                                if positieY - (self.cel_breedte + self.marge) >= self.grenzen_speler[2]:
                                    positieY -= (self.cel_breedte + self.marge)
                            elif event.key == pygame.K_SPACE:
                                if richting == 1:
                                    richting = 2
                                else:
                                    richting = 1
                                hulp = lengteY
                                lengteY = lengteX
                                lengteX = hulp

                                if positieX + lengteX > self.grenzen_speler[1]:
                                    positieX = self.grenzen_speler[1] - lengteX
                                if positieY + lengteY > self.grenzen_speler[3]:
                                    positieY = self.grenzen_speler[3] - lengteY
                                foto = pygame.transform.rotate(foto, 90)

                            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                                self.ankercel = self.sp.grid.getCel(int((positieY - self.grenzen_speler[2]) / (self.cel_breedte + self.marge)),
                                                                    int((positieX - self.grenzen_speler[0]) / (self.cel_breedte + self.marge)))
                                gepl = botenSpeler[b].setPositie(self.ankercel, richting, botenSpeler[b],
                                                                 gekozenCellenMetRichting)
                                if not gepl:
                                    # vakjes even rood zetten tot volgende beweging
                                    self.kleurVakje(self.ankercel, richting, botenSpeler[b].getLengte(), True)
                                    pass
                                else:
                                    Boot.vulDictionaryAanMetCelEnRichting(gekozenCellenMetRichting, self.ankercel,
                                                                          richting, botenSpeler[b].getLengte())

                                    self.getekendeBoten.append(
                                        [pygame.transform.scale(foto, (lengteX, lengteY)), (positieX, positieY)])
                                    type = str(botenSpeler[b].getType())

                                    self.safeFoto.append([type, richting])
                                    self.safeBoten.append([lengteX, lengteY, positieX, positieY])

                                    self.kleurVakje(self.ankercel, richting, botenSpeler[b].getLengte(), False)
                                    botenSpeler[b].initStatus()
                                    self.muziek.play("blub")
                        self.tekenGridsOpnieuw()
                        self.tekenBoten()
                        self.scherm.blit(pygame.transform.scale(foto, (lengteX, lengteY)), (positieX, positieY))
                        self.kleurVakje(self.ankercel, richting, botenSpeler[b].getLengte())
                        pygame.display.update()
            self.kleurVakje(self.ankercel, richting, botenSpeler[b].getLengte())

    # de coördinaten van de cellen van de speler en de computer worden ingesteld
    def stelCoordinatenCellenIn(self):
        for i in range(10):
            for j in range(10):
                self.sp.getGrid().getCel(i, j).setX(self.grenzen_speler[0])
                self.sp.getGrid().getCel(i, j).setY(self.grenzen_speler[2])
                self.cm.getGrid().getCel(i, j).setX(self.grenzen_computer[0])
                self.cm.getGrid().getCel(i, j).setY(self.grenzen_computer[2])

    # de 2 2D arrays worden overlopen en mbv de collidepoint kan de aangeklikte cel bepaald worden
    # zowel in de grid van de speler als de grid van de computer kan de aangeklikte cel bepaald worden
    # (de positie van de muisklik is de parameter)
    def getAangeklikteCel(self, muis_x, muis_y):
        self.res = []
        for i in range(10):
            for j in range(10):
                if self.grid_speler[j][i].collidepoint((muis_x, muis_y)):
                    self.res.append(j)
                    self.res.append(i)
                    return self.res
                elif self.grid_computer[j][i].collidepoint((muis_x, muis_y)):
                    self.res.append(j)
                    self.res.append(i)
                    return self.res
        return None

    # Het volledige spel wordt hieruit gespeeld en verbindt hier dus alle klassen
    def spelVerloop(self, safe):
        if safe is False:
            self.botenGrafischPlaatsen()
        else:
            for index, item in enumerate(self.safeBoten):
                type = self.safeFoto[index][0]
                rotatie = self.safeFoto[index][1]
                if rotatie == 0 or rotatie == 2:
                    foto = pygame.image.load("img/boten/boot" + type + "gedraaid.png")
                else:
                    foto = pygame.image.load("img/boten/boot" + type + ".png")
                self.getekendeBoten.append([pygame.transform.scale(foto, (item[0], item[1])), (item[2], item[3])])
        self.tekenGridsOpnieuw()
        self.tekenBoten()
        pygame.display.update()

        # while-lus die iedereen telkens aan de beurt laat tot iemand wint
        beurt_speler = self.beurtSpeler
        beurt_computer = not self.beurtSpeler
        self.lichtCorrecteGridOp(beurt_speler,beurt_computer)

        while self.afgelopen == 0:
            event = None
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    # algemeen voor sluiten van programma en herhaling regels
                    if self.close.collidepoint(event.pos):
                        # testing laden en saven
                        self.opslaan()
                    elif self.help.collidepoint(event.pos):
                        self.handelEventsRegelsAf()

            if beurt_speler:
                event = pygame.event.wait()
                if event.type == MOUSEBUTTONDOWN:
                    if self.grenzen_computer[0] <= event.pos[0] <= self.grenzen_computer[1] and self.grenzen_computer[2] <= event.pos[1] <= self.grenzen_computer[3]:
                        x, y = event.pos
                        lijst = self.getAangeklikteCel(x, y)
                        if lijst is not None:
                            cel = self.cm.getGrid().getCel(lijst[1], lijst[0])
                            if cel.getStatus() == 0 or cel.getStatus() == 2:
                                self.sp.vuur(cel)
                                self.muziek.play("schiet")
                                self.scherm.blit(self.foto_cellen[cel.setFoto()], self.grid_computer[lijst[0]][lijst[1]])
                                for x in range(5 - len(self.cm.getBoten())):
                                    self.scherm.blit(pygame.transform.scale(pygame.image.load('img/afsluitknop.png'), (200, 200)), (((self.breedte / 2) - 500) + x * 200, self.hoogte - 200))
                                self.updateAfgelopen()
                                beurt_speler = False
                                beurt_computer = True
                                self.lichtCorrecteGridOp(beurt_speler, beurt_computer)
                    if self.close.collidepoint(event.pos):
                        # laden en saven
                        self.opslaan()
                    elif self.help.collidepoint(event.pos):
                        self.handelEventsRegelsAf()

            elif beurt_computer and self.afgelopen == 0:
                # het is aan de computer en die zal schieten op basis van het algoritme
                cel_pc = self.cm.schiet()
                self.hulp.vertraging(1.1)
                self.scherm.blit(self.foto_cellen[cel_pc.setFoto()], self.grid_speler[cel_pc.getKolom()][cel_pc.getRij()])
                self.updateAfgelopen()
                beurt_speler = True
                beurt_computer = False
                self.hulp.vertraging(0.8)
                self.lichtCorrecteGridOp(beurt_speler,beurt_computer)

        if self.afgelopen == 1:
            pygame.draw.rect(self.scherm, self.BLAUWGRIJS, ((self.breedte / 2) - 250, (int(self.hoogte / 2) - 250), 550, 200))
            self.hulp.toon_tekst("georgia", 100, "YOU LOSE", ((self.breedte / 2 - 220), (int(self.hoogte / 2 - 200))))
        else:
            pygame.draw.rect(self.scherm, self.BLAUWGRIJS, ((self.breedte / 2) - 250, (int(self.hoogte / 2)-250), 550, 200))
            self.hulp.toon_tekst("georgia", 100, "YOU WIN", ((self.breedte / 2 - 190), (int(self.hoogte / 2 - 200))))

    # De keuze geven om op te slaan wanneer je afsluit
    def opslaan(self):
        self.scherm.blit(pygame.transform.scale(self.achtergrond, (self.breedte, self.hoogte)), (0, 0))
        self.opslaan_knoppen = [pygame.draw.rect(self.scherm, self.eigenschappen_knoppen[0].get_kleur(), ((self.breedte / 2)-250, 200, 500, 150)),
                                 pygame.draw.rect(self.scherm, self.eigenschappen_knoppen[1].get_kleur(), ((self.breedte / 2)-250, 400, 500, 150)),
                                 pygame.draw.rect(self.scherm, self.eigenschappen_knoppen[2].get_kleur(), ((self.breedte / 2)-250, 600, 500, 150))]

        self.hulp.toon_tekst("georgia", 65, 'Save and leave', ((self.breedte / 2)-210, 230))
        self.hulp.toon_tekst("georgia", 80, "Don't save",((self.breedte / 2)-190, 420))
        self.hulp.toon_tekst("georgia", 80, "Cancel", ((self.breedte / 2)-130, 620))

        gedaan = False
        while not gedaan:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for x in range(len(self.opslaan_knoppen)):
                        if self.opslaan_knoppen[x].collidepoint(pygame.mouse.get_pos()):
                            if x == 0:
                                # de nodige variabelen opslaan
                                self.naamgeving_opslaan()
                            elif x == 1:
                                pygame.quit()
                                sys.exit()
                            else:
                                self.tekenSpeelveld()
                                self.tekenHitsEnMisses()
                                gedaan = True

                pygame.display.update()

    # bij keuze opslaan kan je uw versie een naam geven
    def naamgeving_opslaan(self):
        self.scherm.blit(self.achtergrond, [0, 0])
        self.hulp.printGecentreerdeTekst("georgia", 70, "Under which name do you want to save the game?", self.WIT, (self.breedte/2, 200))
        pygame.draw.rect(self.scherm, self.GRIJS, ((self.breedte / 2)-350, (int(self.hoogte / 3)), 700, 150))
        enter_knop = pygame.draw.rect(self.scherm, self.ZWART, ((self.breedte / 2) - 100, int(self.hoogte / 2), 200, 60))
        self.hulp.toon_tekst("georgia", 30, 'ENTER', (self.breedte/2-45, int(self.hoogte /2) + 15), self.WIT)
        pygame.display.update()
        enter = False
        naam_bestand = ""
        while not enter :
            for event in pygame.event.get():
                #de enterknop nog adden + min 1 karakter voor enter
                if event.type == KEYDOWN:
                    if event.unicode.isalpha() and len(naam_bestand) <= 15:
                        naam_bestand += event.unicode
                    elif event.key == K_BACKSPACE:
                        naam_bestand = naam_bestand[:-1]

                    pygame.draw.rect(self.scherm, self.GRIJS, ((self.breedte / 2) - 350, (int(self.hoogte / 3)), 700, 150))
                    self.hulp.printGecentreerdeTekst("georgia", 60, naam_bestand, self.ZWART, (self.breedte / 2, int(self.hoogte / 3) + 65))
                    pygame.display.update()
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(naam_bestand) > 0:
                        enter = True
                        opslag = SaveLoad()
                        opslag.saving(naam_bestand, self.grid_speler, self.grid_computer, self.eig_grid_speler, self.sp,
                                      self.cm, self.boot_keuze, self.final_shot, self.safeFoto, self.safeBoten)
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if enter_knop.collidepoint(event.pos[0],event.pos[1]) and len(naam_bestand) > 0:
                        enter = True
                        opslag = SaveLoad()
                        opslag.saving(naam_bestand, self.grid_speler, self.grid_computer, self.eig_grid_speler, self.sp,
                                      self.cm, self.boot_keuze, self.final_shot, self.safeFoto, self.safeBoten)
                        pygame.quit()
                        sys.exit()

    # Om te zien in welk scherm van de regels we ons bevinden en of we terug moeten keren naar het speelveld
    def handelEventsRegelsAf(self):
        aantalNext = 0
        self.hulp.regels(aantalNext)
        nextKnop = self.hulp.next_knop()
        goback = self.hulp.go_back_knop()
        pygame.display.update()

        gedaan = False
        while not gedaan:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if nextKnop.collidepoint(mouse_pos):
                        aantalNext += 1
                        if aantalNext <= 2:
                            self.hulp.regels(aantalNext)
                            self.hulp.go_back_knop()
                            self.hulp.next_knop()
                            pygame.display.update()
                        else:
                            aantalNext = 0
                            self.tekenSpeelveld()
                            self.tekenHitsEnMisses()
                            gedaan = True
                    if goback.collidepoint(mouse_pos):
                        aantalNext = 0
                        self.tekenSpeelveld()
                        self.tekenHitsEnMisses()
                        gedaan = True


    def setNiveauEnBotenpakket(self, keuzes):
        self.cm.setMoeilijkheid(keuzes[0])
        self.automatischPlaatsen = keuzes[2]
        self.boot_keuze = keuzes[1]
        if keuzes[3] == 1:
            self.beurtSpeler = False
        elif keuzes[3] == 2:
            if randint(0, 1) == 0:
                self.beurtSpeler = False

    # om duplicated code te vermijden in de methode spelVerloop()
    def lichtCorrecteGridOp(self, beurt_speler, beurt_computer):
        self.beurt_speler_grid.set_achtergrond(beurt_speler)
        self.beurt_computer_grid.set_achtergrond(beurt_computer)
        self.tekenCoordinaten()
        self.tekenGridsOpnieuw()
        self.tekenBoten()
        self.tekenHitsEnMisses()

    # Na elk schot wordt hier gecontroleerd of het spel afgelopen zou kunnen zijn
    # self.afgelopen is 1 als de speler verliest en 2 als de computer verliest
    def updateAfgelopen(self):
        if(len(self.sp.getBoten())) == 0:
            self.afgelopen = 1
        elif(len(self.cm.getBoten())) == 0:
            self.afgelopen = 2

    # Hulpmethode zodat het menu de eindsituatie ter beschikking heeft
    def get_finale_info(self):
        lijst = [self.afgelopen, self.cm.getStatistics(), self.sp.getStatistics()]
        return lijst