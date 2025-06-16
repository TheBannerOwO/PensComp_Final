# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 16:30:13 2025

@author: t0rm3nt4
"""

import clases

def game():
    suma = 0 
    while True:
        print("tus cartas son: ", clases.player.mano)
        hand = clases.player.hitOrStand()
        if isinstance(hand, int): #pregunta si es un numero por el valor que devuelve la función
            for i in range(len(clases.player.mano)):
                suma = suma + hand
            print(suma)
            if suma == 21:
                print("ganaste")
            elif suma > 21:
                print("perdiste")
            #hay que hacer ifs para comparar con el crupier
        print(hand)
        for i in range(len(clases.player.mano)):
            suma = suma + hand[i].valor
        if suma > 21:
            print("te pasaste, tus cartas suman: ", suma)
            break
game()