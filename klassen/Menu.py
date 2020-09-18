import pygame
import ctypes
import sys
from pygame.locals import *
from Knop import Knop
from Speelveld import Speelveld
from Music import Music
from SaveLoad_class import SaveLoad
from Grafische_hulpklasse import Hulpklasse


class Menu:
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    # foto's inladen
    backg = pygame.image.load('img/achtergrond.png')
    logo = pygame.image.load('img/logo2.png')
    keuzes_afbeelding = pygame.image.load('img/back.jpg')

    # extra attributen
    keuze = 0  # keuze van het scherm
    aantalNext = 0  # aantal schermen voor regels
    opties_tonen = False  # variabele boor load-opties te tonen
    opgeslagen_spellen = ['optie1', 'optie2', 'optie3', "optie4", "azertyuiopmlkjh", "azertyuiopmlkjh",
                          "azertyuiopmlkjh", "azertyuiopmlkjh", "azertyuiopmlkjh", "azertyuiopmlkjh"]

    eigenschappen_keuze = [None]*3  # eigenschappen van de kleuren van knoppen van niveau
    eigenschappen_boten = [None]*3  # idem maar knoppen van boten
    manier_plaatsen = [None]*2  # twee opties: random of niet
    eigenschappen_first = [None]*3
    alle_keuzes = [0, 0, 0, 0]
    muziek = Music()
    safe = False
    sv = None

    GRIJS = (199, 199, 199)
    DONKERGRIJS = (126, 126, 126)
    BLAUWGRIJS = (120, 116, 141)
    ZWART = (0, 0, 0)
    WIT = (255, 255, 255)

    # constructor van menu, maakt display aan, en initialiseert de knoppen voor later gebruik
    def __init__(self):
        # initialisatie van de belangrijkste dingen
        ctypes.windll.user32.SetProcessDPIAware()
        self.true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        try :
            self.gameDisplay = pygame.display.set_mode(self.true_res, pygame.FULLSCREEN)
        except:
            print("geen scherm groot genoeg")
            self.gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.muziek.intro()
        self.grootte_scherm = pygame.display.get_surface()
        self.display_height = self.grootte_scherm.get_height()
        self.display_width = self.grootte_scherm.get_width()
        self.hulp = Hulpklasse(self.gameDisplay, self.display_width, self.display_height)
        pygame.display.set_caption('Battleship')
        self.wis_eigenschappen()

    def wis_eigenschappen(self):
            self.eig_nextN = Knop(self.GRIJS, None, None, False, None)
            self.eig_nextB = Knop(self.GRIJS, None, None, False, None)
            self.eig_next_last = Knop(self.GRIJS, None, None, False, None)
            for x in range(3):
                self.eigenschappen_keuze[x] = (Knop(self.DONKERGRIJS, None, None, None, None))
                self.eigenschappen_boten[x] = (Knop(self.DONKERGRIJS, None, None, None, None))
                self.eigenschappen_first[x] = (Knop(self.DONKERGRIJS, None, None, None, None))
            for x in range(2):
                self.manier_plaatsen[x] = (Knop(self.DONKERGRIJS, None, None, None, None))

    # bij het startscherm maak je een keuze tussen de verschillende buttons,
    # ook keuzes voor later schermen (niveau en boten kiezen)
    def game_main(self, keuze):
        crashed = False
        self.keuze = keuze  # welk scherm wil je: start, load, quit, regels
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
            if self.keuze == 0:
                self.game_initialisatie()
            elif self.keuze == 1:
                self.laatste_keuzes()
            elif self.keuze == 2:
                self.laden_interface()
            elif self.keuze == 3:
                self.hulp.regels(self.aantalNext)
                self.regels_events()
            elif self.keuze == 4:  # dit is eigenlijk bij de startknop
                self.niveau_kiezen()
            elif self.keuze == 5:
                self.keuze_botenpakket()
            elif self.keuze == 6:
                self.spel_starten()
            elif self.keuze == 7:
                self.eindscherm()
            elif self.keuze == 8:
                self.first_shot_kiezen()

            pygame.display.update()
            self.clock.tick(60)  # frames per second
        pygame.quit()
        sys.exit()

    # het hoofdmenu wordt geinitialiseerd
    def game_initialisatie(self):
        # alles dat getekend moet worden, wordt getekend
        self.gameDisplay.blit(pygame.transform.scale(self.backg, (self.display_width, self.display_height)), (0, 0))
        self.gameDisplay.blit(pygame.transform.scale(self.logo, (int(self.logo.get_width() * (3 / 4)), int(self.logo.get_height() * (3 / 4)))),
                              (int((self.display_width / 2) - (self.logo.get_width() * (3 / 4) / 2)), self.display_height / 100))
        self.hulp.toon_tekst("georgia", 20, "Versie 3.7.11", (0, self.display_height - 30))

        # Knoppen maken
        startknop = pygame.draw.rect(self.gameDisplay, self.BLAUWGRIJS, ((self.display_width / 2) - 350 / 2, (self.display_height / 20) * 5, 350, 100))
        laadknop = pygame.draw.rect(self.gameDisplay, self.BLAUWGRIJS, ((self.display_width / 2) - 350 / 2, (self.display_height / 20) * 8, 350, 100))
        regelsknop = pygame.draw.rect(self.gameDisplay, self.BLAUWGRIJS, ((self.display_width / 2) - 350 / 2, (self.display_height / 20) * 11, 350, 100))
        quitknop = pygame.draw.rect(self.gameDisplay, self.BLAUWGRIJS, ((self.display_width / 2) - 350 / 2, (self.display_height / 20) * 14, 350, 100))

        # tekst op de knoppen
        self.hulp.toon_tekst("georgia", 45, "Start", ((self.display_width / 2) - 45, (self.display_height / 20) * 5 + 25))
        self.hulp.toon_tekst("georgia", 45, "Load", ((self.display_width / 2) - 45, (self.display_height / 20) * 8 + 25))
        self.hulp.toon_tekst("georgia", 45, "Rules", ((self.display_width / 2) - 45, (self.display_height / 20) * 11 + 25))
        self.hulp.toon_tekst("georgia", 45, "Quit", ((self.display_width / 2) - 45, (self.display_height / 20) * 14 + 25))

        # er wordt nagegaan welke eventen er plaatsvinden, vooral het kiezen van start/load/rules/quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if laadknop.collidepoint(mouse_pos):
                    self.game_main(2)
                elif startknop.collidepoint(mouse_pos):
                    self.wis_eigenschappen()
                    self.game_main(4)
                elif regelsknop.collidepoint(mouse_pos):
                    self.game_main(3)
                elif quitknop.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

    # bij de keuze van load wordt hier je keuze afgehandeld, NOG TE IMPLEMENTEREN!!
    def laden_interface(self):
        # testing laden en saven
        go_back = self.hulp.go_back_knop()
        self.gameDisplay.blit(self.keuzes_afbeelding, [0, 0])
        opslag = SaveLoad()
        self.opgeslagen_spellen = opslag.getSaves()
        tijdelijke_var = len(self.opgeslagen_spellen)
        if tijdelijke_var == 0:
            self.hulp.printGecentreerdeTekst("georgia", 80, "You don't have any games saved.",
                                             self.WIT, (self.display_width / 2, 200))
            pygame.display.update()
            self.hulp.vertraging(2)
            self.game_main(0)

        else:
            self.hulp.printGecentreerdeTekst("georgia", 70, "Which game do you want to open?",
                                             self.WIT, (self.display_width / 2, 200))
            pygame.draw.rect(self.gameDisplay, self.GRIJS, ((self.display_width / 2) - 350, (int(self.display_height / 3)), 700, 150))
            enter_knop = pygame.draw.rect(self.gameDisplay, self.ZWART, ((self.display_width / 2) - 100, int(self.display_height / 2), 200, 60))
            self.hulp.toon_tekst("georgia", 30, 'ENTER', (self.display_width / 2 - 45, int(self.display_height / 2) + 15),
                                 self.WIT)
            go_back = self.hulp.go_back_knop()
            if self.opties_tonen:
                self.hulp.printGecentreerdeTekst("georgia", 40, "Maybe try one of these: ", self.WIT,
                                                 (self.display_width / 2, int(self.display_height / 2) + 100))
                for x in range(len(self.opgeslagen_spellen)):
                    if x < 5:
                        self.hulp.toon_tekst("georgia", 40, self.opgeslagen_spellen[x],
                                                     ((self.display_width/2)-320, int(self.display_height / 2) + 150 + (x * 50)), self.WIT)
                    else:
                        self.hulp.toon_tekst("georgia", 40, self.opgeslagen_spellen[x],
                                             ((self.display_width / 2) + 50,
                                              int(self.display_height / 2) + 150 + ((x-5) * 50)), self.WIT)

            pygame.display.update()

            enter = False
            naam_bestand = ""
            while not enter:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.unicode.isalpha() and len(naam_bestand) <= 15:
                            naam_bestand += event.unicode
                        elif event.key == K_BACKSPACE:
                            naam_bestand = naam_bestand[:-1]
                        pygame.draw.rect(self.gameDisplay, self.GRIJS, ((self.display_width / 2) - 350, (int(self.display_height / 3)), 700, 150))
                        self.hulp.printGecentreerdeTekst("georgia", 60, naam_bestand, self.ZWART, (self.display_width / 2, int(self.display_height / 3) + 65))

                        if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(naam_bestand) > 0:
                                enter = True
                                self.laden(naam_bestand)

                        pygame.display.update()
                    if event.type == MOUSEBUTTONDOWN:
                        if enter_knop.collidepoint(event.pos[0], event.pos[1]) and len(naam_bestand) > 0:
                            enter = True
                            self.laden(naam_bestand)

                        if go_back.collidepoint(event.pos):
                            self.game_main(0)

    def laden(self, naam):
        opslag = SaveLoad()
        self.opties_tonen = False
        if not opslag.loading(naam):
            self.opties_tonen = True
            self.laden_interface()
        data = opslag.getData()
        self.safe = True
        self.sv = Speelveld(self.gameDisplay, self.display_width, self.display_height)
        self.sv.grid_speler = data[0]
        self.sv.grid_computer = data[1]
        self.sv.eig_grid_speler = data[2]
        self.sv.sp = data[3]
        self.sv.cm = data[4]
        self.sv.boot_keuze = data[5]
        self.sv.final_shot = data[6]
        self.sv.safeFoto = data[7]
        self.sv.safeBoten = data[8]
        print('het is geladen')
        self.game_main(6)

    def regels_events(self):
        nextKnop = self.hulp.next_knop()
        goback = self.hulp.go_back_knop()
        # Er wordt nagegaan welke events er plaatsvinden, zoals sluiten van het spel en klikken op de knoppen
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if nextKnop.collidepoint(mouse_pos):
                    self.aantalNext += 1
                    if self.aantalNext <= 2:
                        pygame.display.update()
                    else:
                        self.aantalNext = 0
                        self.game_main(0)

                if goback.collidepoint(mouse_pos):
                    self.aantalNext = 0
                    self.game_main(0)

    # Door op de knop te klikken van welk niveau je wilt wordt deze keuze bijgehouden voor het spel
    def niveau_kiezen(self):
        self.safe = False
        self.gameDisplay.blit(pygame.transform.scale(self.keuzes_afbeelding, (self.display_width, self.display_height)), (0, 0))
        self.goback = self.hulp.go_back_knop()
        self.hulp.toon_tekst("georgia", 50, "Choose the difficulty of the game.", (self.display_width / 22, self.display_height / 4), self.WIT)

        # 3 rectangles maken
        self.opties = [pygame.draw.rect(self.gameDisplay, self.eigenschappen_keuze[0].get_kleur(),((self.display_width / 20), (int(self.display_height / 2.5)), 500, 150)),
                       pygame.draw.rect(self.gameDisplay, self.eigenschappen_keuze[1].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 40), (int(self.display_height / 2.5)), 500, 150)),
                       pygame.draw.rect(self.gameDisplay, self.eigenschappen_keuze[2].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 20), (int(self.display_height / 2.5)), 500, 150))]

        self.hulp.toon_tekst("georgia", 80, "Easy", (4 * (self.display_width / 30), (int(self.display_height / 2.5)) + 20))
        self.hulp.toon_tekst("georgia", 80, "Average", (13 * (self.display_width / 30), (int(self.display_height / 2.5)) + 20))
        self.hulp.toon_tekst("georgia", 80, "Hard", (23 * (self.display_width / 30), (int(self.display_height / 2.5)) + 20))

        self.keuzes_events(self.opties, self.eigenschappen_keuze, 0, 5)
        pygame.display.update()

    # Je kiest hier je botenpakket voor het spel
    def keuze_botenpakket(self):
        self.gameDisplay.blit(pygame.transform.scale(self.keuzes_afbeelding, (self.display_width, self.display_height)), (0, 0))
        self.goback = self.hulp.go_back_knop()
        self.hulp.toon_tekst("georgia", 50, "Choose your boats.", (self.display_width / 22, self.display_height / 5), self.WIT)

        self.boten = [pygame.draw.rect(self.gameDisplay, self.eigenschappen_boten[0].get_kleur(),((self.display_width / 20), (int(self.display_height / 3)), 450, 500)),
                      pygame.draw.rect(self.gameDisplay, self.eigenschappen_boten[1].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 40), (int(self.display_height / 3)), 450, 500)),
                      pygame.draw.rect(self.gameDisplay, self.eigenschappen_boten[2].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 20), (int(self.display_height / 3)), 450, 500))]
        self.gameDisplay.blit(pygame.transform.scale(pygame.image.load('img/boten/bootpakket1.png'), (450, 500)), ((self.display_width / 20), (int(self.display_height / 3))))
        self.gameDisplay.blit(pygame.transform.scale(pygame.image.load('img/boten/bootpakket2.png'), (450, 500)), ((self.display_width / 20) + 13 * (self.display_width / 40), (int(self.display_height / 3))))
        self.gameDisplay.blit(pygame.transform.scale(pygame.image.load('img/boten/bootpakket3.png'), (450, 500)), ((self.display_width / 20) + 13 * (self.display_width / 20), (int(self.display_height / 3))))

        self.keuzes_events(self.boten, self.eigenschappen_boten, 1, 1)
        pygame.display.update()

    # Hier beslist de speler of hij de boten zelf wilt plaatsen en wie er eerst aan de beurt zal zijn
    def laatste_keuzes(self):
        self.gameDisplay.blit(pygame.transform.scale(self.keuzes_afbeelding, (self.display_width, self.display_height)), (0, 0))
        self.goback = self.hulp.go_back_knop()
        self.hulp.toon_tekst("georgia", 50, "Do you want to place your boats yourself?", (self.display_width / 22, self.display_height / 5), self.WIT)

        manier_van_plaatsen = [ pygame.draw.rect(self.gameDisplay, self.manier_plaatsen[0].get_kleur(), ((self.display_width / 20), (int(self.display_height / 3)), 500, 150)),
                                pygame.draw.rect(self.gameDisplay, self.manier_plaatsen[1].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 40), (int(self.display_height / 3)), 500, 150))]
        self.hulp.toon_tekst("georgia", 80, "Yes!", (int(4 * (self.display_width / 30)-12), (int(self.display_height / 2.75))))
        self.hulp.toon_tekst("georgia", 60, "No, random", (int(12 * (self.display_width / 30))-6, (int(self.display_height / 2.75))))

        # knop naar het spel
        self.keuzes_events(manier_van_plaatsen, self.manier_plaatsen, 2, 2)
        pygame.display.update()

    def first_shot_kiezen(self):
        # wie begint er
        self.goback = self.hulp.go_back_knop()
        self.hulp.toon_tekst("georgia", 50, "Who will fire the first shot?", (self.display_width / 22, self.display_height / 2), self.WIT)

        self.eerste = [pygame.draw.rect(self.gameDisplay, self.eigenschappen_first[0].get_kleur(),((self.display_width / 20), (int(self.display_height / 1.5)), 500, 150)),
                  pygame.draw.rect(self.gameDisplay, self.eigenschappen_first[1].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 40), (int(self.display_height / 1.5)), 500, 150)),
                  pygame.draw.rect(self.gameDisplay, self.eigenschappen_first[2].get_kleur(), ((self.display_width / 20) + 13 * (self.display_width / 20), (int(self.display_height / 1.5)), 500, 150))]

        self.hulp.toon_tekst("georgia", 60, "I will", (int(4 * (self.display_width / 30)), (int(self.display_height / 1.5)) + 30))
        self.hulp.toon_tekst("georgia", 60, "The computer", (int(13 * (self.display_width / 30)) - 27, (int(self.display_height / 1.5)) + 30))
        self.hulp.toon_tekst("georgia", 60, "Random", (int(23 * (self.display_width / 30)) - 10, (int(self.display_height / 1.5)) + 30))

        self.keuzes_events(self.eerste, self.eigenschappen_first, 3, 6)
        pygame.display.update()

    # Het spel gaat van start na je keuzes en er wordt een speelveld gemaakt
    # Alle volgende events spelen zich af in speelveld en verder,
    # wanneer er een winnaar is keert men terug naar deze klasse
    def spel_starten(self):
        if self.safe is False:
            self.sv = Speelveld(self.gameDisplay, self.display_width, self.display_height)
            self.sv.setNiveauEnBotenpakket(self.alle_keuzes)
        while not self.sv.afgelopen:  # zolang er geen winnaar is
            self.sv.tekenSpeelveld()
            self.sv.spelVerloop(self.safe)
            self.sv.klok.tick(60)
            pygame.display.update()

        self.finale_info = self.sv.get_finale_info()  # dit is de info omtrent de winnaar en de statestieken
        self.hulp.vertraging(3)
        self.game_main(7)  # via main naar het eindscherm

    # als het spel ten einde komt wordt hier nog eens de winnaar vermeld + statestieken
    # er is een mogelijkheid om opnieuw te spelen, naar het menu te gaan of het spel te sluiten
    def eindscherm(self):
        self.gameDisplay.blit(pygame.transform.scale(pygame.image.load("img/back.jpg"), (self.display_width, self.display_height)), (0, 0))
        text = "YOU LOST"
        if self.finale_info[0] == 1:
            text = "YOU LOSE"
        else:
            text = "YOU WIN"

        self.hulp.toon_tekst("georgia", 100, text, ((self.display_width / 2 - 240), (int(30))), self.WIT)
        afsluitknop = pygame.image.load("img/afsluitknop.png").convert_alpha()
        afsluitknop_geschaald = pygame.transform.scale(afsluitknop, (40, 40))
        close = self.gameDisplay.blit(afsluitknop_geschaald, (self.display_width - 50, 30))

        menu = pygame.image.load("img/home.png").convert_alpha()
        menu_geschaald = pygame.transform.scale(menu, (40, 40))
        menuknop = self.gameDisplay.blit(menu_geschaald, (self.display_width - 90, 35))
        starthoogte = 230
        breedte = (self.display_width / 2 - 240)
        self.hulp.toon_tekst("georgia", 50, 'Statistics', (breedte, starthoogte), self.WIT)

        self.hulp.toon_tekst("georgia", 40, 'Computer', (breedte, starthoogte + 90), self.WIT)
        self.hulp.toon_tekst("georgia", 30, 'Number of shots:    ' + str(self.finale_info[1][0]), (breedte, starthoogte + 140), self.WIT)
        self.hulp.toon_tekst("georgia", 30, 'Number of hits:     ' + str(self.finale_info[1][1]), (breedte, starthoogte + 170), self.WIT)

        self.hulp.toon_tekst("georgia", 40, 'Player', (breedte, starthoogte + 230), (250, 250, 250))
        self.hulp.toon_tekst("georgia", 30, 'Number of shots:    ' + str(self.finale_info[2][0]), (breedte, starthoogte + 280), self.WIT)
        self.hulp.toon_tekst("georgia", 30, 'Number of hits:     ' + str(self.finale_info[2][1]), (breedte, starthoogte + 310), self.WIT)

        rem_knop = Knop((20,20,20), None, None, False, None)
        rematchknop = pygame.draw.rect(self.gameDisplay, rem_knop.get_kleur(), (breedte + 10, starthoogte + 460, 200, 60))
        self.hulp.toon_tekst("georgia", 30, 'REMATCH', (breedte + 30, starthoogte + 470), self.WIT)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if rematchknop.collidepoint(pygame.mouse.get_pos()):
                    rem_knop.set_hover(True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rematchknop.collidepoint(pygame.mouse.get_pos()):
                    self.wis_eigenschappen()
                    self.game_main(4)
                if menuknop.collidepoint(pygame.mouse.get_pos()):
                    self.game_main(0)
                if close.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
        pygame.display.update()

    # Hier worden de acties afgehandeld in de optiemenu's (het hoveren over knoppen, klikken..)
    def keuzes_events(self, array_knoppen, array_eig, op, scherm=0):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                for x in range(len(array_knoppen)):
                    if array_knoppen[x].collidepoint(pygame.mouse.get_pos()) and not array_eig[x].get_selected():
                        array_eig[x].set_hover(True)
                    else:
                        array_eig[x].set_hover(False)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(len(array_knoppen)):
                    if array_knoppen[x].collidepoint(pygame.mouse.get_pos()):
                        self.alle_keuzes[op] = x
                        array_eig[x].set_selected(True)
                        if scherm == 2:
                            self.game_main(8)
                        else:
                            self.game_main(scherm)

                if self.goback.collidepoint(pygame.mouse.get_pos()):
                    self.wis_eigenschappen()
                    self.game_main(0)
            pygame.display.update()


# via deze twee lijntjes wordt het spel gestart en loopt alles hoe het moet
var = Menu()
var.game_main(0)