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


# Limpia la consola
def clearConsole():
    # 'cls' para Windows, 'clear' para Linux.
    os.system('cls' if os.name == 'nt' else 'clear')


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
    playerCount = int(input("¿Cuántos jugadores son? (Max. 7)\n >> "))

    if playerCount < 1 or playerCount > 7:
        raise Exception('Input invalido, intente de nuevo')

    return playerCount


# Pregunta y valida que el nombre no este en la lista dada.
def inputValidateName(i: int, players: list[str]):
    name = input(f"Nombre del jugador {i}:\n >> ")
    if name in players:
        raise Exception(f'Ya existe un jugador llamado {name}')
    return name


# Pregunta y devuelve la cantidad a apostar.
def inputBetAmnt(balance: int):
    bet = int(input("¿Cuánto apostás?\n >> "))

    if bet > balance:
        raise Exception(f'No podes apostar mas de lo que tenés.')
    elif bet < 1:
        raise Exception(f'La apuesta minima es de 1')
    
    return bet