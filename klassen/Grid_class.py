from Cel_class import Cel


class Grid:

    def __init__(self):
        self.cellen = []
        for i in range(100):
            c = Cel(i)
            self.cellen.append(c)

    def initBuren(self):
        for i in range(100):
            self.cellen[i].initBuren(self)

    def getCellen(self):
        return self.cellen

    def __str__(self):
        y = ""
        for i in range(10):
            s = ""
            for x in range(10):
                s += str(self.getCel(i, x).getStatus()) + " "
            y += s + "\n"
        return y

    def toString(self, densiteit=None):
        s = ""
        if densiteit is None:
            for i in range(100):
                s += str(self.cellen[i]) + "\n"
            return s
        else:
            s = ""
            for i in range(10):
                y = ""
                for x in range(10):
                    y += str(self.getCel(i, x).getDensiteit()) + " "
                s += y + "\n"
            return s

    def getCel(self, rij, kolom=None):  # als kolom niet wordt meegegeven, werkt het als getCel(nummer)
        if kolom is not None:
            s = str(rij) + str(kolom)
            return self.cellen[int(s)]
        else:
            return self.cellen[rij]