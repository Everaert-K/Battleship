import pickle
import os, fnmatch


class SaveLoad:
    def __init__(self):
        self.data = []
        self.listOfSaves = []

    def saving(self, naam, grid_speler, grid_computer, eig_grid_speler, sp, cm, boot_keuze, final_shot, safeFoto, safeBoten):
        self.data = [grid_speler, grid_computer, eig_grid_speler, sp, cm, boot_keuze, final_shot, safeFoto, safeBoten]
        with open('Saves/' + naam + '.p', 'wb') as file:
            pickle.dump(self.data, file)

    def loading(self, naam):
        try:
            with open('Saves/' + naam + '.p', 'rb') as file:
                self.data = pickle.load(file)
                return True
        except:
            print("Kon het bestand niet vinden")
            return False

    def getData(self):
        return self.data

    def getSaves(self):
        listOfFiles = os.listdir('Saves/.')
        pattern = '*.p'
        count = 0
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern) and count < 10:
                file, extention = os.path.splitext(entry)
                self.listOfSaves.append(file)
                count += 1
        return self.listOfSaves

