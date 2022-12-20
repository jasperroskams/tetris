
import pyxel


class Blok():
    types = [
        [
            [(-1,-1), (-1, 0), (0, 0), ( 1, 0)],
            [( 0,-1), ( 1,-1), (0, 0), ( 0, 1)],##
            [(-1, 0), ( 0, 0), (1, 0), ( 1, 1)],######
            [( 0,-2),  (0,-1), (0, 0), (-1, 0)]
        ],
        [
            [(-2, 0), (-1, 0), (0, 0), (1, 0)],
            [(0, -2), (0, -1), (0, 0), (0, 1)],
            [(-2, 0), (-1, 0), (0, 0), (1, 0)],  ########
            [(0, -2), (0, -1), (0, 0), (0, 1)]
        ],
        [
            [( 0, -1), (1, -1), (-1, 0), ( 0, 0)],
            [(-1, -1), (-1, 0), ( 0, 0), ( 0, 1)],####
            [(-1, -1), (0, -1), ( 0, 0), ( 1, 0)],  ####
            [( 0, -1), (-1, 0), ( 0, 0), (-1, 1)],
        ],
        [
            [( 0,-1), (-1, 0), (0, 0), (1, 0)],
            [( 0,-1), ( 0, 0), (1, 0), (0, 1)],  ##
            [(-1, 0), ( 0, 0), (1, 0), (0, 1)],######
            [( 0,-1), (-1, 0), (0, 0), (0, 1)]
        ],
        [
            [( 1,-1), (-1, 0), (0, 0), ( 1, 0)],
            [( 0,-2), ( 0,-1), (0, 0), ( 1, 0)],    ##
            [(-1, 1), ( 0, 0), (1, 0), (-1, 0)],######
            [(-1,-1),  (0,-1), (0, 0), ( 0, 1)]
        ],
        [
            [(-1, -1), (0, -1), (-1, 0), (0, 0)],
            [(-1, -1), (0, -1), (-1, 0), (0, 0)],####
            [(-1, -1), (0, -1), (-1, 0), (0, 0)],####
            [(-1, -1), (0, -1), (-1, 0), (0, 0)]
         ]
    ]

    def __init__(self, vorm, kleur):
        self.vorm = vorm
        self.kleur = kleur * 8
        self.x = 19
        self.y = 16
        self.richting = 0
        self.tijd_om_naar_onder_te_bewegen = 0
        self.nodig_om_naar_onder_te_bewegen = 1
        self.is_geselecteert = False
        self.moet_ik_naar_onder = True
        self.kan_ik_naar_rechts = True
        self.kan_ik_naar_links = True
        self.kan_ik_draaien = False

    def update(self, game):

        # DRAAIEN
        if pyxel.btnp(pyxel.KEY_UP) and self.is_geselecteert:
            self.richting = (self.richting + 1) % 4

        if self.tijd_om_naar_onder_te_bewegen % self.nodig_om_naar_onder_te_bewegen == 0 and self.is_geselecteert == True:
            self.y += 1

        self.tijd_om_naar_onder_te_bewegen += 1
        self.meest_linkse_x = 0
        self.meest_rechtse_x = 0
        self.meest_onderse_y = 0
        for x,y in self.types[self.vorm][self.richting]:
            if self.meest_linkse_x > x:
                self.meest_linkse_x = x
            if self.meest_rechtse_x < x:
                self.meest_rechtse_x = x
            if self.meest_onderse_y < y:
                self.meest_onderse_y = y
        while self.x + self.meest_rechtse_x >= game.game_breedte / 8 and self.is_geselecteert:
            self.x -= 1
        while self.x + self.meest_linkse_x < 0:
            self.x += 1

        # tegels van blok in grid
        self.kan_ik_draaien = False
        while not self.kan_ik_draaien:
            self.tegels = []
            for i, _ in enumerate(self.types[self.vorm][self.richting]):
                tegel = (self.types[self.vorm][self.richting][i][0] + self.x,
                         self.types[self.vorm][self.richting][i][1] + self.y)
                self.tegels.append(tegel)
            self.kan_ik_draaien = True
            if self.is_geselecteert:
                for i, tegel in enumerate(self.tegels):
                    if game.tegels[tegel[1]][tegel[0]]:  # raken blok onder deze tegel
                        self.x -= self.types[self.vorm][self.richting][i][0]
                        self.kan_ik_draaien = False
                        break
                    # self.richting = (self.richting - 1) % 4

        # self.tegels = []
        # for i, blok in enumerate(self.types[self.vorm][self.richting]):
        #     blok = (self.types[self.vorm][self.richting][i][0] + self.x,
        #             self.types[self.vorm][self.richting][i][1] + self.y)
        #     self.tegels.append(blok)
            # if self.richting <3:
            #     self.richting += 1
            # else:
            #     self.richting = 0
        self.nodig_om_naar_onder_te_bewegen = game.valsnelheid
        if pyxel.btn(pyxel.KEY_DOWN) and self.is_geselecteert:
            self.nodig_om_naar_onder_te_bewegen = 1




        # if self.y + self.meest_onderse_y > 32:
        #     # self.y -= 8
        #     # self.moet_ik_naar_onder = False
        #     # self.is_geselecteert = False
        #     game.newBlok()



        if pyxel.btnp(pyxel.KEY_RIGHT) and self.is_geselecteert and self.x + self.meest_rechtse_x < 15:
            for tegel in self.tegels:
                if game.tegels[tegel[1]][tegel[0] + 1]:  # raken blok rechts deze tegel
                    self.kan_ik_naar_rechts = False
            if self.kan_ik_naar_rechts:
                self.x += 1
        self.kan_ik_naar_rechts = True
        if pyxel.btnp(pyxel.KEY_LEFT) and self.is_geselecteert and self.x + self.meest_linkse_x > -1:
            for tegel in self.tegels:
                if game.tegels[tegel[1]][tegel[0] - 1]:  # raken links onder deze tegel
                    self.kan_ik_naar_links = False
            if self.kan_ik_naar_links:
                self.x -= 1
        self.kan_ik_naar_links = True

        meest_rechtse_x = 0
        for x,y in self.types[self.vorm][self.richting]:
            if meest_rechtse_x < x:
                meest_rechtse_x = x



    def draw(self):
        pyxel.blt(self.x * 8 + self.types[self.vorm][self.richting][0][0] * 8, self.y * 8 + self.types[self.vorm][self.richting][0][1] * 8, 1, 0, self.kleur, 8, 8, pyxel.COLOR_BLACK)
        pyxel.blt(self.x * 8 + self.types[self.vorm][self.richting][1][0] * 8, self.y * 8 + self.types[self.vorm][self.richting][1][1] * 8, 1, 0, self.kleur, 8, 8, pyxel.COLOR_BLACK)
        pyxel.blt(self.x * 8 + self.types[self.vorm][self.richting][2][0] * 8, self.y * 8 + self.types[self.vorm][self.richting][2][1] * 8, 1, 0, self.kleur, 8, 8, pyxel.COLOR_BLACK)
        pyxel.blt(self.x * 8 + self.types[self.vorm][self.richting][3][0] * 8, self.y * 8 + self.types[self.vorm][self.richting][3][1] * 8, 1, 0, self.kleur, 8, 8, pyxel.COLOR_BLACK)





