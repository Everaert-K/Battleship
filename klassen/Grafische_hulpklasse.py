import pygame
from pygame.locals import *


# deze klasse bevat de methodes die zowel het speelveld als het menu nodig hebben
class Hulpklasse:

    ZWART = (0, 0, 0)
    GRIJS = (199, 199, 199)

    def __init__(self, display,width,height):
        pygame.init()
        self.display = display
        self.arrayRegels = [pygame.image.load('img/stand1.png'), pygame.image.load('img/stand2.png'),
                       pygame.image.load('img/stand3.png')]
        self.regelsscherm = pygame.image.load('img/regelss.jpg')
        self.regelsText = pygame.image.load('img/rulesText.png')
        self.width = width
        self.height = height

    # tekst weergeven op de opgegeven plaats (standaard is het kleur zwart)
    def toon_tekst(self, font, grootte, tekst, locatie, tekst_kleur=ZWART):
        fontTitel = pygame.font.SysFont(font, grootte)
        next = fontTitel.render(tekst, True, tekst_kleur)
        self.display.blit(next, locatie)

    # zo kan er tekst geprint en gecentreerd worden waar dit nodig is
    def printGecentreerdeTekst(self, lettertype, grootte, tekst, kleur, centrum):
        font = pygame.font.SysFont(lettertype, grootte)
        tekst = font.render(tekst, False, kleur)
        text_rect = tekst.get_rect(center=centrum)
        self.display.blit(tekst, text_rect)

    # zorgt voor wat delay in het spel bijvoorbeeld bij het oplichten van de grids of vooraleer de computer schiet
    def vertraging(self, tijd):
        start_ticks = pygame.time.get_ticks()
        while 1:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds >= tijd:
                break

    def next_knop(self):
        nextKnop = pygame.draw.rect(self.display, self.GRIJS, (self.width - 170, self.height - 70, 160, 60))
        self.toon_tekst("georgia", 40, "Next ->", (self.width - 155, self.height - 65))
        return nextKnop

    def go_back_knop(self):
        goback = pygame.draw.rect(self.display, self.GRIJS, (10, 10, 180, 60))
        self.toon_tekst("georgia", 45, "Go back", (20, 15))
        return goback

    # bij de keuze van rules wordt hier je keuze afgehandeld
    def regels(self, waarde=0):
        schaling = (self.arrayRegels[0].get_width()) / self.width
        if (schaling > 1):
            schaling = schaling-0.5
        # de achtergrond, en extra foto's worden gepositioneerd
        self.display.blit(pygame.transform.scale(self.regelsscherm, (self.width, self.height)), (0, 0))
        self.display.blit(pygame.transform.scale(self.regelsText, ((self.regelsText.get_width()*2),
                                                                   (self.regelsText.get_height())*2)),
                          (((self.width)/2-self.regelsText.get_width()), 15))
        self.display.blit(pygame.transform.scale(self.arrayRegels[waarde],
                                                 (int(self.arrayRegels[waarde].get_width()*(schaling*9/10)),
                                                  int(self.arrayRegels[0].get_height()*(schaling*9/10)))),
                          (0, self.regelsText.get_height()+50))
