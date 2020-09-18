class Knop():
    hover = None
    kleur = ()
    geklikt = None
    enabled = None
    achtergrond = None

    # verschillende kleuren
    GRIJS = (192, 192, 192)
    LICHTBLAUW = (105, 138, 253)
    BLAUW = (51, 136, 255)
    DONKERBLAUW = (85, 170, 221)
    ROOD = (255, 0, 0)
    GROEN = (0, 255, 0)
    ZWART = (0, 0, 0)
    WIT = (255, 255, 255)

    def __init__(self, kleur, hover, geklikt, enabled, fouteBoot, achtergrond=None):
        self.kleur = kleur
        self.hover = hover
        self.geklikt = geklikt
        self.enabled = enabled
        self.fouteBoot = fouteBoot
        self.achtergrond = achtergrond

    # via alle gegevens het juiste kleur teruggeven
    def get_kleur(self):
        if not self.hover and not self.geklikt and self.fouteBoot is None:
            self.kleur = self.GRIJS
        elif self.hover:
            self.kleur = self.LICHTBLAUW

        elif self.geklikt:
            self.kleur = self.BLAUW

        elif self.fouteBoot:
            self.kleur = self.ROOD
        elif self.fouteBoot is False:
            self.kleur = self.GROEN

        if self.enabled is False:
            self.kleur = self.ZWART
        elif self.enabled is True:
            self.kleur = self.GRIJS

        if self.achtergrond is False:
            self.kleur = self.WIT
        elif self.achtergrond is True:
            self.kleur = self.DONKERBLAUW

        return self.kleur

    # enkele getters en setters die de gegevens veranderen tijdens de acties
    def set_hover(self, waarde):
        self.hover = waarde

    def set_selected(self, waarde):
        self.geklikt = waarde

    def set_achtergrond(self, waarde):
        self.achtergrond = waarde

    def get_selected(self):
        return self.geklikt

    def set_enabled(self, waarde):
        self.enabled = waarde

    def get_enabled(self):
        return self.enabled

    def setFouteBoot(self, waarde):
        self.fouteBoot = waarde