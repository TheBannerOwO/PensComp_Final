# -*- coding: utf-8 -*-

"""
Este script ejecuta una ronda de Blackjack para múltiples jugadores,
utilizando una clase Player (en clases.py) y un mazo de cartas.
Cada jugador realiza una jugada, apuesta, y se actualiza su saldo en base al resultado.
"""

from GameClasses import Player, ConjoinedDeck, Crupier
from helpers import waitContinue, clearConsole, handleInput, inputPlayerAmnt, inputValidateName, inputBetAmnt
import os, sys, time


# Falta implementar en el loop del juego
def mano(self):
        suma = 0 
        balance = 0

        

        while True:
            print("Tus cartas son:", self.mano)
            hand = self.hitOrStand()

            if isinstance(hand, int):  # Si devuelve un número, el jugador eligió 'stand'
                suma += hand
                print("Total de puntos:", suma)

                if suma == 21:
                    print("¡Ganaste!")
                    balance = self.balance + (int(bet) * 2)
                    print("Nuevo saldo:", balance)
                    return balance

                elif suma > 21:
                    print("Perdiste")
                    balance = self.balance - int(bet)
                    print("Nuevo saldo:", balance)
                    return balance

                # Si no ganó ni perdió, simplemente retorna el balance sin cambio
                print("Tus cartas suman:", suma)
                return balance

            print("Resultado:", hand)

            if hand == "lose":
                # El jugador se pasó y pierde la apuesta
                balance = self.balance - int(bet)
                print("Nuevo saldo:", balance)
                return balance

def main():

    players: dict[str, Player] = {}
    bets: dict[str, int] = {}
    decks = ConjoinedDeck(newDecks = 8, shuffled = True)

    # Populamos el diccionario de jugadores y apuestas.
    playerCount = handleInput(inputPlayerAmnt)

    for i in range(playerCount):
        name = handleInput(inputValidateName, i+1, [name for name in players.keys()])
        players[name] = Player(name, decks)
        bets[name] = 0
    round = 1

    # Loop principal del juego
    while True:

        # Mostramos la lista de jugadores y su dinero actual al comienzo de la ronda.
        clearConsole()
        print(f'Ronda Nº{round}\n')

        print(f'Dinero actual:', 
              *[f'\n{name}: {player.balance}' for name, player in players.items()], 
              end='\n\n')
        waitContinue()

        # Pedimos una apuesta a cada jugador.
        for name, player in players.items():
            clearConsole()
            bet = handleInput(inputBetAmnt, player.balance, header=f' Fase de apuestas || Turno de {name}\n\nSaldo actual: {player.balance}')
            player.extractBalance(bet)
            bets[name] = bet
            print(f"\nSe apostó {bet}, saldo restante: {player.balance}\n")
            waitContinue()

        clearConsole()

        # Inicializamos al crupier y repartimos las cartas.
        crupier: Crupier = Crupier(decks)
        
        crupier.takeCard()
        crupier.takeCard()

        print(' Manos ', end='\n\n')
        for name, player in players.items():
            player.takeCard()
            player.takeCard()
            print(f'{name}:', *[f'{card}' for card in player.hand], end='\n\n')

        waitContinue()

        # Los jugadores juegan turnos hasta que nadie quiera seguir,
        # o alguien gane.
        enabled = [name for name in players.keys()]
        winners = []
        bestHand = 0

        while True:
            passes = 0
            for name in enabled:
                turn = players[name].playTurn()
                
                if  turn == 21: winners.append(name)
                elif turn == 0: passes += 1
                elif turn < 21: continue
                elif turn > 21: enabled.remove(name)    

            if len(winners) != 0:
                break
            
            # Si nadie tiene blackjack, reutilizamos la lista de winners
            # para guardar a los jugadores que tengan las mejores manos.
            elif passes == len(enabled):
                for name in enabled:
                    if len(winners) == 0:
                        winners.append(name)
                        bestHand = players[name].handValue()

                    elif players[name].handValue() > bestHand:
                        winners.clear()
                        winners.append(name)
                        bestHand = players[name].handValue()

                    elif players[name].handValue() == bestHand:
                        winners.append(name)
                break


        # Que el crupier agarre cartas hasta que sume 18 o mas,
        # y que empiece la comparacion de manos para decidir los payouts.
        while crupier.handValue() < 17:
            crupier.takeCard()

        crupierValue = crupier.handValue()
        
        # Si se pasa, ganan todos los que no perdieron.
        if crupierValue > 21:
            for name in enabled:
                print(f'Ganó {name}')
                players[name].balance += bets[name]*2

        # Si tiene blackjack, ganan los demas que tengan blackjack
        elif crupierValue == 21:
            if bestHand == 21:
                for name in winners:
                    print(f'Ganó {name}')
                    players[name].balance = bets[name]*2
        
        # Si no tiene la mejor mano, ganan los que la tengan
        elif bestHand > crupierValue:
            for name in winners:
                print(f'Ganó {name}')
                players[name].balance = bets[name]*2

        else:
            print('Nadie ganó :(')

        waitContinue()

        # Reseteamos el mazo y las manos para
        # poder empezar otra ronda.
        for name, player in players.items():
            player.hand.clear()
        decks.reset()
        decks.shuffle()

        # TODO: FALTA TESTING

        # ! Hay que testear a ver que pasa si un jugador se queda sin plata. (Creo que se rompe el juego)

        # ? TODO: Al final de la ronda, dar a elegir a los jugadores si quieren retirarse o retirarlos si no tienen mas plata.

        # TODO: Falta hacer "pantallas" para algunas partes. (eg: cuando el dealer agarra cartas, final de la partida, etc...)

        # TODO: Arreglar bugs en los que se a veces skipean algunas pantallas (??)

        round += 1


if __name__ == "__main__":
    main()