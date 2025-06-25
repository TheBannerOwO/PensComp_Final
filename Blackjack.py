# -*- coding: utf-8 -*-

"""
Este script ejecuta una ronda de Blackjack para múltiples jugadores,
utilizando una clase Player (en clases.py) y un mazo de cartas.
Cada jugador realiza una jugada, apuesta, y se actualiza su saldo en base al resultado.
"""

from GameClasses import Player, ConjoinedDeck, Crupier, Card
from helpers import waitContinue, clearConsole, handleInput, inputPlayerAmnt, inputValidateName, inputBetAmnt, inputOptionsMenu, win
import os, sys, time

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
            print(player, end='\n\n')

        print(crupier, end='\n\n')

        waitContinue()

        # Los jugadores juegan turnos hasta que nadie quiera seguir,
        # o alguien gane.
        enabled: list[str] = [name for name in players.keys()]
        losers: list[str] = []

        for name in enabled:
            clearConsole()

            turnHeader = f' Fase de turnos || Turno de {name}\n\n'

            while True:

                if players[name].handValue() > 21:
                    print(turnHeader+str(players[name])+f'\n\n{name} se pasó, pasando turno...\n')
                    losers.append(name)
                    waitContinue()
                    break

                if players[name].handValue() == 21:
                    print(turnHeader+str(players[name])+f'\n\n{name} tiene blackjack, pasando turno...\n')
                    waitContinue()
                    break
                
                action: str = handleInput(inputOptionsMenu, ['Hit', 'Stay'], header=turnHeader+str(players[name]))

                match action:
                    case 'hit':
                        newCard = players[name].takeCard()
                        newHandValue = players[name].handValue()
                        print(f'Nueva carta: {newCard}, (Suma actual: {newHandValue})')
                    case 'stay':
                        print(f'Pasando turno...')
                        break

                waitContinue()
                clearConsole()
        
        enabled = [name for name in enabled if name not in losers]

        # Que el crupier agarre cartas hasta que sume 18 o mas,
        # y que empiece la comparacion de manos para decidir los payouts.
        while crupier.handValue() < 17:
            crupier.takeCard()
        
        clearConsole()
        
        print(' Fase de comparación \n\n')

        for name, player in players.items():
            print(player, end='\n\n')
        print(crupier, end='\n\n')

        waitContinue()
        clearConsole()
        print('---- Resultados ----\n')

        crupierValue = crupier.handValue()

        results: dict[str, str]

        # Si se pasa, ganan todos los que no perdieron.
        if crupierValue > 21:
            for name in enabled:
                win(players[name], bets[name])
        
        # Si no, se comparan todas las manos con las del crupier.
        else:
            for name in enabled:
                if players[name].handValue() > crupierValue:
                    win(players[name], bets[name])
                elif players[name].handValue() == crupierValue:
                    print(f'{name} recuperó su apuesta ({bets[name]})')
                    players[name].balance += bets[name]
                else:
                    losers.append(name)
        
        for name in losers:
            print(f'{name} perdió {bets[name]}')
        
        print('\n---- Resultados ----\n')

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

        # TODO: Añadir winrate en los jugadores para extraer estadisticas.

        round += 1


if __name__ == "__main__":
    main()