import pygame


class Music:
    def __init__(self):
        self._songs = ['schiet.wav', 'blub.wav']
        self.status = None
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
        pygame.mixer.init()
        self.effect = None
    
    def intro(self):
        pygame.mixer.music.load("Sounds/intro.wav")
        pygame.mixer.music.play(-1)

    def play(self, naam):
        file = naam + ".wav"
        try:
            index = self._songs.index(file)
            if self.status != index:
                self.effect = pygame.mixer.Sound('Sounds/' + file)
                self.status = index
            self.effect.play()
        except:
            print("Kon het bestand niet vinden")
