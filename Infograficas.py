import matplotlib.pyplot as plt
import numpy as np
import random

class Jugador:

    def __init__(self, apuestaDef: int, stop: int = 17, plata: int = 500):

        self.mano: list = []
        self.stop: int = stop # Default 17
        self.plata: int = plata # Dinero total
        self.balance: int = 0 # Cantidad apostada
        self.apuesta: int = apuestaDef # Cantidad a apostar

        self.historialPlata = [plata]
        self.historialWinrate = [0]

        self.partidasTotales = 0
        self.partidasGanadas = 0



def calcularMano(mano: list):
    total = 0
    ases = 0

    for carta in mano:
        if carta != 1:
            total += carta
        else:
            ases += 1

    for _ in range(ases):
        if total + 11 > 21:
            total += 1
        else:
            total += 11
    
    return total


# Decide si un jugador gano, devuelve True si gano o empato
# y False si perdio. Modifica al jugador proveido de la forma correspondiente.
def decidirResultado(jugador: Jugador, crupier: Jugador):
    valJug = calcularMano(jugador.mano)
    valCrup = calcularMano(crupier.mano)

    # Si el jugador se paso, pierde
    if valJug > 21:
        jugador.balance = 0
        return False
    
    # Si el crupier se pasa o el jugador tiene
    # una mano mejor, devuelve la apuesta duplicada
    elif valCrup > 21 or valJug > valCrup:
        jugador.plata += jugador.balance*2
        jugador.balance = 0
        return True

    # Si son iguales, recupera la apuesta
    elif valJug == valCrup:
        jugador.plata += jugador.balance
        jugador.balance = 0
        return True


# Genera un mazo.
def mazo():
    mazo = []
    for _ in range(0,4):
        for i in range(1,14):
            if i < 10: 
                mazo.append(i)
            else:
                mazo.append(10)
    return mazo


# Genera cuantos mazos se pidan
def variosMazos(num):
    mazo_juego = []
    for i in range(num):
        mazo_juego.extend(mazo())
    random.shuffle(mazo_juego)
    return mazo_juego


# Devuelve una carta de un mazo
def carta(jugador: Jugador, mazo):   
    carta = random.choice(mazo)
    jugador.mano.append(carta)


# Hace que un jugador agarre cartas hasta que no quiera mas
def jugar(jugador: Jugador, mazo):
    mano = calcularMano(jugador.mano)
    while mano < jugador.stop:
        carta(jugador, mazo)
        mano = calcularMano(jugador.mano)
    return mano


# Toma una lista de jugadores y grafica el wr
def graficarWinrate(jugadores: list[Jugador]):
    fig, ax = plt.subplots()
    
    for i, jugador in enumerate(jugadores):
        ax.plot(jugador.historialWinrate, label=f'Jugador {i+1}')
    
    ax.set_xlabel('Partidas')
    ax.set_ylabel('Wr')
    ax.set_title('Winrate a lo largo del tiempo')
    ax.legend()
    plt.show()


# Toma una lista de jugadores y grafica el historial de la palta
def graficarBalance(jugadores: list[Jugador]):
    fig, ax = plt.subplots()
    
    for i, jugador in enumerate(jugadores):
        ax.plot(jugador.historialPlata, label=f'Jugador {i+1}')
    
    ax.set_xlabel('Partidas')
    ax.set_ylabel('Plata')
    ax.set_title('Plata a lo largo del tiempo')
    ax.legend()
    plt.show()


def heatMap(datos: list[list[int]]):
    fig, ax = plt.subplots()

    ax.set_title("Test crupiers")
    ax.set_ylabel("Jugador")
    ax.set_xlabel("Crupier")
    ax.imshow(datos)
    plt.show()


# Toma una lista de jugadores, una cantidad de mazos, y el stop del crupier
# y simula una partida
def simularPartida(jugadores: list[Jugador], cantMazos, crupierStop = 17):

    mazo = variosMazos(cantMazos)
    crupier = Jugador(0, stop = crupierStop)

    # Cada jugador apuesta
    for jugador in jugadores:
        jugador.plata -= jugador.apuesta
        jugador.balance += jugador.apuesta

    # El crupier agarra sus primeras dos cartas
    for i in range(2):
        carta(crupier, mazo)

    # Cada jug agarra cartas hasta su stop
    for jugador in jugadores:
        jugar(jugador, mazo)
    jugar(crupier, mazo)

    res = []

    # Se deciden los ganadores y se limpian las apuestas
    for jugador in jugadores:
        jugador.partidasTotales += 1
        if decidirResultado(jugador, crupier):
            res.append(1)
            jugador.partidasGanadas += 1
        else:
            res.append(0)
        
        # Sumamos las estadisticas al historial para poder
        # graficarlo apropiadamente con pyplot
        jugador.historialPlata.append(jugador.plata)
        jugador.historialWinrate.append((jugador.partidasGanadas/jugador.partidasTotales)*100)
    
    for jugador in jugadores:
        jugador.mano = []
    crupier.mano = []
    
    return res


partidas = 1000


data = []
for i in range(15, 22):
    dataParcial = []
    for j in range(15, 22):
        jugador = Jugador(10, i)
        for _ in range(partidas):
            simularPartida([jugador], 7, j)
        dataParcial.append(jugador.historialWinrate[-1])
    data.append(dataParcial)

heatMap(data)