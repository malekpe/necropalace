import pygame
import os
from pygame.locals import *
from random import randint
from pygame.sprite import RenderPlain

pygame.init()

def main():
    print("########################################\n")
    print("by Malekpe#1681")
    print("https://github.com/malekpe/necropalace\n")
    print("########################################\n")
    nbx,nby = 8,12
    pygame.display.set_caption('Necropalace')
    e_largeur = 64*nbx
    e_hauteur = 64*nby
    font=pygame.font.SysFont("arial", 40)
    fenetre = pygame.display.set_mode((e_largeur, e_hauteur))
    fenetre.fill((221,166,83))
    for i in range(0, e_largeur, 64):
        colonnes=pygame.Rect(i,0,1,e_hauteur)
        pygame.draw.rect(fenetre,(0,0,0),colonnes)
    for i in range(0, e_hauteur, 64):
        lignes=pygame.Rect(0,i,e_largeur,1)
        pygame.draw.rect(fenetre,(0,0,0),lignes)

    class Case:
        def __init__(self, x, y):
            self.co = (x, y)
            self.libre = True

        def __repr__(self):
            data = {"co":self.co, "libre":self.libre}
            return str(data)

        def refresh(self, blue, red):
            x,y = self.co
            color=pygame.Rect(x,y,64,64)
            if self.co != blue.case.co and self.co != red.case.co:
                if self.libre:
                    pygame.draw.rect(fenetre,(221,166,83),color)
                else:
                    pygame.draw.rect(fenetre,(0,0,0),color)
            for i in range(0, e_largeur, 64):
                colonnes=pygame.Rect(i,0,1,e_hauteur)
                pygame.draw.rect(fenetre,(0,0,0),colonnes)
            for i in range(0, e_hauteur, 64):
                lignes=pygame.Rect(0,i,e_largeur,1)
                pygame.draw.rect(fenetre,(0,0,0),lignes)

            return

        def coGrille(self):
            x,y = self.co
            x,y = int(x/64),int(y/64)
            return x,y

    class Perso:
        def __init__(self,case,color):
            self.case = case
            self.color = color
            self.iconObjet = pygame.image.load(f"{color}.png")


        def __repr__(self):
            data = {"couleur":self.color, "co":self.case.co, "libre":self.case.libre}
            return str(data)

        def refresh(self):
            fenetre.blit(self.iconObjet,self.case.co)
            self.case.libre = False

        def scanNearby(self, grille, block):
            nearby = []
            x,y = self.case.coGrille()
            for diff_x in range(-1,2):
                for diff_y in range(-1,2):
                    if diff_x == 0 and diff_y == 0:
                        continue
                    for n in range(1,3):
                        cell_x = x + diff_x * n
                        cell_y = y + diff_y * n
                        if cell_x < 0 or cell_y < 0 or cell_x >= nbx or cell_y >= nby:
                            continue
                        if grille[y+diff_y*n][x+diff_x*n].libre:
                            nearby.append(grille[y+diff_y*n][x+diff_x*n])
                        elif block:
                            break
            return nearby

    def caseFinder(grille, x, y):
        x = x//64
        y = y//64
        return grille[y][x]

    def coup1(player, grille):
        purple = player.scanNearby(grille, True)
        for case in purple:
            x,y = case.co
            #draw=pygame.Rect(x,y,64,64)
            #pygame.draw.rect(fenetre,(148,0,211),draw)
            pygame.draw.circle(fenetre, (148,0,211), (x+32, y+32), 30)
        return purple

    def coup2(player, grille):
        cible = player.scanNearby(grille, False)
        for case in cible:
            x,y = case.co
            pygame.draw.circle(fenetre, (220,10,30), (x+32, y+32), 30)
        return cible

    def move(statue, player, case, purple, grille, blue, red):
        if len(purple) == 0:
                if player.color == "blue":
                    texte=font.render("Le joueur Rouge a gagné !", True, (255,0,0))
                else:
                    texte=font.render("Le joueur Bleu a gagné !", True, (0,0,255))
                fenetre.blit(texte, (64, 64*5))
        if case in purple:
            statue["move"] = False
            purple = list()
            player.case = case
            player.refresh()
            refresh(grille, blue, red)
        return statue

    def fire(statue, player, case, cible, grille, blue, red):
        if case in cible:
            statue["fire"] = False
            cible = list()
            case.libre = False
            case.refresh
            refresh(grille, blue, red)
        else:
            refresh(grille, blue, red)
        return statue

    def refresh(grille, blue, red):
        for ligne in grille:
            for case in ligne:
                case.refresh(blue, red)

    def gameUpdate(statue, player, blue, red, grille, purple, cible):
        if statue["fire"] and not statue["move"]:
            cible = coup2(player, grille)

        if not statue["move"] and not statue["fire"]:
            statue["move"], statue["fire"] = True, True
            if statue["player"] == "blue":
                player = red
                statue["player"] = "red"
            else:
                player = blue
                statue["player"] = "blue"
            purple = coup1(player, grille)
            if len(purple) == 0:
                if player.color == "blue":
                    texte=font.render("Le joueur Rouge a gagné !", True, (255,0,0))
                else:
                    texte=font.render("Le joueur Bleu a gagné !", True, (0,0,255))
                fenetre.blit(texte, (64, 64*5))
        return statue, player, purple, cible

    grille = []
    for y in range(0, e_hauteur, 64):
        ligne = []
        for x in range(0, e_largeur, 64):
            ligne.append(Case(x, y))
        grille.append(ligne)

    blue = Perso(grille[9][2], "blue")
    red = Perso(grille[2][5], "red")

    blue.refresh()
    red.refresh()

    for i in range(0):
        y,x = randint(0,11),randint(0,7)
        if grille[y][x].libre:
            grille[y][x].libre=False

    for ligne in grille:
        for case in ligne:
            case.refresh(blue,red)

    player = red
    statue = {"player":"red", "move":False, "fire":False}
    purple = list()
    cible = list()
    dbclock = pygame.time.Clock()
    DOUBLECLICKTIME = 300

    while True:
        statue, player, purple, cible = gameUpdate(statue, player, blue, red, grille, purple, cible)
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            quit()
        if event.type == MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            mouse = caseFinder(grille, x, y)
            if mouse == player.case and statue["fire"]:
                cible = coup2(player, grille)

        if event.type == MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            case = caseFinder(grille, x, y)
            if mouse == case and statue["move"]:
                cible = list()
                refresh(grille,blue,red)
                purple = coup1(player, grille)
                statue = move(statue, player, case, purple, grille, blue, red)
            if mouse == player.case and case != mouse and statue["fire"]:
                statue = fire(statue, player, case, cible, grille, blue, red)
                if statue["move"]:
                    purple = coup1(player, grille)
            if dbclock.tick() < DOUBLECLICKTIME:
                if mouse == player.case and case == mouse and not statue["move"]:
                    statue["fire"] = False
                    cible = list()
                    refresh(grille,blue,red)

main()
