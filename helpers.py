# -*- coding: utf-8 -*-

"""
Este archivo contiene algunas funciones auxiliares
para que el script principal quede mas limpio.
"""

from GameClasses import Player
import os, sys


# Espera a que el usuario presione enter para continuar.
def waitContinue(msg="Presione enter para continuar..."):
    input(msg)


# Wrapper de input() para hacer mas simple pedir inputs lindos.
def prettyInput(msg="Input", sym=" >> "):
    return input(f'{msg}\n{sym}')


# Limpia la consola
def clearConsole():
    # 'cls' para Windows, 'clear' para Linux.
    os.system('cls' if os.name == 'nt' else 'clear')


# Genera el mensaje de que el jugador dado ganó y le agrega
# su apuesta multiplicada por un factor dado (def=2) a su balance.
def win(player: Player, bet: int, factor:int = 2):
    print(f'{player.name} ganó {bet*factor} (apuesta original {bet})')
    player.balance += bet*factor


"""
handleInput funciona de la siguiente forma; se le pasa la funcion que se quiere ejecutar
de forma segura como primer parametro, y luego los parametros para la funcion
que se quiere asegurar.
Importante: Idealmente la funcion que se le pasa deberia estar implementada
de forma tal, que cuando el usuario de un input inesperado "raisee" un error
con el mensaje deseado. Estan como ejemplo las que ya hice :).
"""
# Wrapper para manejar el input de forma segura.
def handleInput(func, *args, header: str = ''):
    clearConsole()
    while True:
        try:
            print(header) if header != '' else ...
            result = func(*args)
            if result:
                return result
            break
        except Exception as e:
            clearConsole()
            if isinstance(e, KeyboardInterrupt):
                sys.exit()
            print(f'\033[41mError: {e}\033[0m', end="\n\n")


# Pregunta y devuelve la cantida de jugadores.
def inputPlayerAmnt():
    playerCount = int(prettyInput("¿Cuántos jugadores son? (Max. 7) (0 para winrate testing)"))

    if playerCount < 0 or playerCount > 7:
        raise Exception('Input invalido, intente de nuevo')

    return playerCount


# Pregunta y valida que el nombre no este en la lista dada.
def inputValidateName(i: int, players: list[str]):
    name = prettyInput(f"Nombre del jugador {i}:")
    if name in players:
        raise Exception(f'Ya existe un jugador llamado {name}')
    if len(name) > 16 or len(name) < 3:
        raise Exception('El nombre debe estar entre 3 y 16 caracteres')
    return name


# Pregunta y devuelve la cantidad a apostar.
def inputBetAmnt(balance: int):
    bet = int(prettyInput("¿Cuánto apostás?"))

    if bet > balance:
        raise Exception(f'No podes apostar mas de lo que tenés')
    elif bet < 1:
        raise Exception(f'La apuesta minima es de 1')
    
    return bet


# Da a elegir entre una lista de opciones.
def inputOptionsMenu(options: list[str]):
    print('\nOpciones:\n')
    for i in range(len(options)):
        print(f'{i+1}. {options[i]}')

    opt = int(prettyInput("\nNº de la opcion")) - 1
    if opt not in range(len(options)):
        raise Exception('El numero debe estar entre las opciones proveidas')
    return options[opt].lower()


# Deja elegir el umbral de los bots.
def inputBotUmbral(botName: str):
    umbral = int(prettyInput(f"Umbral para {botName} (1 <= umbral <= 21)"))

    if umbral < 1 or umbral > 21:
        raise Exception('El numero debe estar entre 1 y 21 incluidos')
    return umbral