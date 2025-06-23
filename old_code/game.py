# -*- coding: utf-8 -*-
"""
Este script ejecuta una ronda de Blackjack para múltiples jugadores,
utilizando una clase Player (en clases.py) y un mazo de cartas.
Cada jugador realiza una jugada, apuesta, y se actualiza su saldo en base al resultado.
"""

import clases


def mano(jugador):
    """
    Ejecuta una mano para un jugador individual.
    El jugador apuesta y elige hit o stand. Se calcula su saldo según el resultado.
    
    Devuelve el nuevo balance del jugador.
    """
    suma = 0 
    balance = 0

    print("Saldo actual:", jugador.balance)
    bet = input("¿Cuánto apostás? ")

    while True:
        print("Tus cartas son:", jugador.mano)
        hand = jugador.hitOrStand()

        if isinstance(hand, int):  # Si devuelve un número, el jugador eligió 'stand'
            suma += hand
            print("Total de puntos:", suma)

            if suma == 21:
                print("¡Ganaste!")
                balance = jugador.balance + (int(bet) * 2)
                print("Nuevo saldo:", balance)
                return balance

            elif suma > 21:
                print("Perdiste")
                balance = jugador.balance - int(bet)
                print("Nuevo saldo:", balance)
                return balance

            # Si no ganó ni perdió, simplemente retorna el balance sin cambio
            print("Tus cartas suman:", suma)
            return balance

        print("Resultado:", hand)

        if hand == "lose":
            # El jugador se pasó y pierde la apuesta
            balance = jugador.balance - int(bet)
            print("Nuevo saldo:", balance)
            return balance

# Diccionarios para guardar instancias de jugadores y sus respectivos balances
jugadores = {}      
balances = {}

# Cantidad de jugadores ingresada por el usuario
count = input("¿Cuántos jugadores son? ")

for i in range(0, int(count) + 1):  # Crea un jugador por cada índice
    jugador = f"jugador {i}"
    jugadores[jugador] = clases.Player(clases.mazo)  # Instancia de la clase Player
    balances[jugador] = 0  # Inicializa el saldo en 0 (se actualizará luego)

# Ronda de juego para cada jugador
for nombre, jugador in jugadores.items():
    print("Turno de", nombre)
    saldo = mano(jugador)  # Ejecuta la mano del jugador
    balances[nombre] = saldo  # Actualiza el diccionario de balances
    print(f"{nombre} ahora tiene ${saldo}")

    