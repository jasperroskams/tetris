import pickle
import pyxel
from typeblok import Blok
import random
from tegel import Tegel


class Game():
    def __init__(self):
        self.hoogte = 256
        self.breedte = 168
        self.game_breedte = 128
        self.blokken = []
        self.tegels = []
        self.score = 0
        self.aan_het_spelen = False
        self.valsnelheid = 10
        self.score_nodig_voor_sneller_vallen = 1000
        self.topscores = [0]
        self.mag_ik_op_b_druken = True
        for i in range(34):
            self.tegels.append([None]*16)

        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        #     [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        # ]

    def newBlok(self):
        vorm = int(random.triangular(0, 6))
        print(vorm)
        kleur = int(random.triangular(1, 14))
        # vorm = 1
        # kleur = 9
        self.nieuwblok = Blok(vorm, kleur)
        # self.blokken.append(nieuwblok)
    def newTegel(self, x, y, c):
        nieuwtegel = Tegel(x, y, c)
        try:
            self.tegels[y][x] = nieuwtegel
        except IndexError:
            pass
    def wegTegel(self, tegel):
        self.tegels.remove(tegel)

    def update(self):
        if pyxel.btnp(pyxel.KEY_B) and self.mag_ik_op_b_druken:
            self.newBlok()
            self.newBlok()
            self.aan_het_spelen = True
            self.mag_ik_op_b_druken = False


        if pyxel.btnp(pyxel.KEY_P):
            if self.aan_het_spelen :
                self.aan_het_spelen = False
            else:
                self.aan_het_spelen = True
        if self.aan_het_spelen:
            if not self.blokken[0].is_geselecteert:
                self.blokken[0].is_geselecteert = True
                self.blokken[0].x = 8
                self.blokken[0].y = 2
            for blok in self.blokken:
                blok.update(self)
                blokLooptVast = False
                if blok.meest_onderse_y + blok.y >= 31: # raken de grond
                    blokLooptVast = True
                if blok == self.blokken[0]:
                    for tegel in blok.tegels:
                        if self.tegels[tegel[1] + 1][tegel[0]]: # raken blok onder deze tegel
                            blokLooptVast = True

                if blokLooptVast:
                    # kopieer tegels van blok naar tegelrooster
                    for tegel in blok.tegels:
                        self.newTegel(tegel[0], tegel[1], blok.kleur)
                    # nieuwe blok!
                    self.blokken.remove(blok)
                    self.vallende_blok = self.nieuwblok()
                    self.newBlok()

            for i, rij in enumerate(self.tegels):
                wegdoen = False
                for tegel in rij:
                    if tegel == None:
                        wegdoen = False
                        break
                    else:
                        wegdoen = True
                if wegdoen == True:
                    self.tegels.remove(rij)
                    self.tegels.insert(0, [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
                    for ii, rij in enumerate(self.tegels):
                        for tegel in rij:
                            if ii <= i:
                                if tegel != None:
                                    tegel.y += 8
                    self.score += 100
                    if self.score == self.score_nodig_voor_sneller_vallen:
                        self.valsnelheid -= 1
                        self.score_nodig_voor_sneller_vallen += 1000


            print(self.valsnelheid)
            for tegel in self.tegels[2]:
                if tegel != None:
                    for i, topscore in enumerate(self.topscores):
                        if self.score >= topscore:
                            self.topscores.insert(i, self.score)
                            if len(self.topscores) > 5:
                                self.topscores.pop()
                            break
                    self.aan_het_spelen = False
                    self.tegels = []
                    self.valsnelheid = 10
                    for i in range(34):
                        self.tegels.append([None] * 16)
                    self.score = 0
                    with open('data.pickle', 'wb') as f:
                        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
                    break



    def draw(self):
        pyxel.cls(0)
        pyxel.rect(128, 0, 1, 256, 7)
        for x in range(0, self.game_breedte - 112):
            for y in range(0, self.hoogte):
                pyxel.blt(x * 8, y * 8, 1, 0, 112, 8, 8)
        for blok in self.blokken:
            blok.draw()
        for rij in self.tegels:
            for tegel in rij:
                if tegel != None:
                    tegel.draw()
        pyxel.text(self.breedte - len(str(self.score) * 4), 2, str(self.score), 7)
        for i, topscore in enumerate(self.topscores):
            pyxel.text(self.breedte - len(str(self.topscores[i]) * 4), 10 + i * 6, str(self.topscores[i]), 7)
        pass

    def run(self):
        pyxel.init(self.breedte, self.hoogte)
        pyxel.load('tekeningen.pyxres')
        pyxel.run(self.update, self.draw)