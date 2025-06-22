# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 16:30:13 2025

@author: t0rm3nt4
"""

import clases
import Blackjack_Clases

def mano(jugador):
    suma = 0 
    suma_crupier = 0
    balance = 0
    print("saldo: ", jugador.balance)
    bet = input("cuanto apuestas? ")
    while True:
        print("tus cartas son: ", jugador.mano)
        hand = jugador.hitOrStand()
        if isinstance(hand, int): #pregunta si es un numero por el valor que devuelve la función
            suma += hand
            print(suma)
            if suma == 21:
                print("ganaste")
                balance = jugador.balance + (int(bet) * 2)
                print("nuevo saldo: ", jugador.balance)
                return balance
            elif suma > 21:
                print("perdiste")
                balance = jugador.balance - int(bet)
                print("nuevo saldo: ", clases.player.balance)
                return jugador.balance
            print("tus cartas son de: ", suma)
            return balance
            #hay que hacer ifs para comparar con el crupier
        print(hand)
        if hand == "lose":
            balance = jugador.balance - int(bet)
            print("nuevo saldo: ", jugador.balance)
            return balance
            
        
jugadores = {}      
balances = {}
count = input("cuantos jugadores son?")
for i in range(0,int(count) + 1):
    jugador = f"jugador {i}"
    jugadores[jugador] = clases.Player(clases.mazo)
    balances[jugador] = 0

for nombre, jugador in jugadores.items():
    print("Turno de", nombre)
    saldo = mano(jugador)
    print(f"{nombre} ahora tiene ${saldo}")
    balances[nombre] = saldo

    