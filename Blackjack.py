# -*- coding: utf-8 -*-

"""
Este script arranca el juego.
"""

from GameClasses import Player, ConjoinedDeck, Crupier, Bot
from helpers import waitContinue, clearConsole, handleInput, inputPlayerAmnt, inputValidateName, inputBetAmnt, inputOptionsMenu, win, inputBotUmbral
import os, sys, time, random

def main():

    players: dict[str, Player | Bot] = {}
    bets: dict[str, int] = {}
    decks = ConjoinedDeck(newDecks = 8, shuffled = True)
    botsOnly = False
    playerAmnt = handleInput(inputPlayerAmnt)

    if playerAmnt == None or playerAmnt == 0:
        playerAmnt = 0
        botsOnly = True

    # Populamos el diccionario de jugadores y apuestas.
    for i in range(playerAmnt):
        name = handleInput(inputValidateName, i+1, [name for name in players.keys()])
        players[name] = Player(name, decks)
        bets[name] = 0
        

    # Rellenamos los puestos que faltan con bots
    while len(players) < 7:
        name = f'Bot {len(players) + 1}'
        umbral = 17
        if botsOnly:
            umbral = handleInput(inputBotUmbral, name)
        players[name] = Bot(name, decks, umbral=umbral)
        bets[name] = 0
    waitContinue()

    round = 1

    # Loop principal del juego
    while True:


        # Cada "====..." denota un "cambio de etapa" en el sistema del juego


        # Si es una partida "real", randomizar los umbrales de los bots.
        if not botsOnly:
            for name, player in players.items():
                if isinstance(player, Bot):
                    player.umbral = random.randint(14, 19)


        # Mostramos la lista de jugadores y su dinero actual al comienzo de la ronda.
        clearConsole()

        print(f'Ronda Nº{round}\n')

        print(f'Dinero actual:', 
            *[f'\n{name}: {player.balance}' for name, player in players.items()], 
            end='\n\n')
        
        if not botsOnly:
            waitContinue()

        # ============================================================

        # Pedimos una apuesta a cada jugador.
        for name, player in players.items():
            clearConsole()
            if player.balance < 1:
                print(f'{name} no tiene suficiente plata para hacer una apuesta valida,')
                print('se le agregaran +50 chips para que pueda seguir jugando.', end='\n\n')
                player.balance = 50 # '=' en vez de '+=' solo por las dudas haya un caso en el que el jugador pueda tener balance negativo.
                waitContinue()
            
            # Si es un bot, apuesta 10 automaticamente.
            if isinstance(player, Bot):
                bets[name] = player.extractBalance(10)
                continue

            bet = handleInput(inputBetAmnt, player.balance, header=f' Fase de apuestas || Turno de {name}\n\nSaldo actual: {player.balance}')
            bets[name] = player.extractBalance(bet)
            print(f"\nSe apostó {bet}, saldo restante: {player.balance}\n")
            waitContinue()

        # ============================================================

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

        if not botsOnly:
            waitContinue()

        # ============================================================

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

                    if not botsOnly and not isinstance(players[name], Bot):
                        waitContinue()
                    break

                # Si es un bot, y su umbral es mayor al valor de su mano, pide una carta.
                if isinstance(players[name], Bot):
                    if players[name].umbral > players[name].handValue():
                        players[name].takeCard()
                        continue
                    else:
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
        
        # ============================================================

        enabled = [name for name in enabled if name not in losers]

        # Que el crupier agarre cartas hasta que sume 18 o mas,
        # y que empiece la comparacion de manos para decidir los payouts.
        while crupier.handValue() < 17:
            clearConsole()

            print(f'El crupier va a agarrar una carta...', end='\n\n')
            print(crupier, end='\n\n')

            c = crupier.takeCard()

            if not botsOnly:
                for i in range(3):
                    time.sleep(0.1)
                    print('.', end='')
                    time.sleep(0.1)
                print(f'\n\nAgarró {c}, ahora tiene un total de: {crupier.handValue()}', end='\n\n')

                waitContinue()
        
        clearConsole()
        
        print(' Fase de comparación \n')

        for name, player in players.items():
            print(player, end='\n\n')
        print(crupier, end='\n\n')

        if not botsOnly:
            waitContinue()

        # ============================================================

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

        if not botsOnly:
            waitContinue()

        # ============================================================

        # Reseteamos el mazo y las manos para
        # poder empezar otra ronda.
        # Ademas, sumamos las estadisticas.
        # (lo hago aca para que este ligeramente ordenado)
        for name, player in players.items():

            if name in losers: player.stats["loses"] += 1
            else: player.stats["wins"] += 1

            player.hand.clear()

        decks.reset()
        decks.shuffle()

        round += 1

        clearConsole()

        # Mostramos una ultima pantalla con los winrates.

        print('--- Estadisticas ---', end='\n\n')

        for name, player in players.items():
            wins = player.stats["wins"]
            loses = player.stats["loses"]
            winrate = int((wins/(wins+loses))*100)
            finalString = f'{wins}w / {loses}l || %{winrate}wr'

            if isinstance(player, Bot):
                print(f'{name} (u={player.umbral}): {finalString}')
                continue

            print(f'{name}: {finalString}')

        print('\n--- Estadisticas ---\n')

        waitContinue()




if __name__ == "__main__":
    main()