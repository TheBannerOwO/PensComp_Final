# -*- coding: utf-8 -*-

"""
Este script arranca el juego.
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
            if player.balance < 1:
                print(f'{name} no tiene suficiente plata para hacer una apuesta valida,')
                print('se le agregaran +50 chips para que pueda seguir jugando.', end='\n\n')
                player.balance = 50 # '=' en vez de '+=' solo por las dudas haya un caso en el que el jugador pueda tener balance negativo.
                waitContinue()
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

                match handleInput(
                    inputOptionsMenu, ['Hit', 'Stay'],
                    header=turnHeader+f"{players[name]}\n\n{crupier}"
                    ):
                    case 'hit':
                        newCard = players[name].takeCard()
                        newHandValue = players[name].handValue()
                        print(f'\nNueva carta: {newCard}, (Suma actual: {newHandValue})')
                    case 'stay':
                        print(f'\nPasando turno...')
                        waitContinue()
                        break

                waitContinue()
                clearConsole()
        
        enabled = [name for name in enabled if name not in losers]

        # Que el crupier agarre cartas hasta que sume 18 o mas,
        # y que empiece la comparacion de manos para decidir los payouts.
        while crupier.handValue() < 17:
            clearConsole()
            print(f'El crupier va a agarrar una carta...', end='\n\n')
            print(crupier, end='\n\n')
            for i in range(3):
                time.sleep(0.1)
                print('.', end='')
                time.sleep(0.1)
            c = crupier.takeCard()
            print(f'\n\nAgarró {c}, ahora tiene un total de: {crupier.handValue()}', end='\n\n')
            waitContinue()
        
        clearConsole()
        
        print(' Fase de comparación \n')

        for name, player in players.items():
            print(player, end='\n\n')
        print(crupier, end='\n\n')

        waitContinue()
        clearConsole()
        print('---- Resultados ----\n')

        crupierValue = crupier.handValue()

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

        # TODO: Añadir winrate en los jugadores para extraer estadisticas.

        # ? TODO: Al final de la ronda, dar a elegir a los jugadores si quieren retirarse o retirarlos si no tienen mas plata.

        round += 1


if __name__ == "__main__":
    main()