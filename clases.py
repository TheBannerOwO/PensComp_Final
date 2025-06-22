"""

Este módulo implementa las clases necesarias para un juego básico de Blackjack:
- Card: representa una carta de la baraja
- Deck: representa un mazo de cartas, con reinicio, mezcla y extracción
- Player: representa un jugador con su mano y lógica para jugar una ronda
"""

import random

# Clase que representa una carta individual
class Card: 
    def __init__(self, valor, palo):
        self.palo = palo        # Ej: "diamonds", "hearts"
        self.valor = valor      # Número del 1 al 10 (los mayores a 10 también valen 10)
    
    def __str__(self):
        return f'valor: {self.valor} | palo: {self.palo}'
    
    def __repr__(self):
        return f'valor : {self.valor} | palo {self.palo}'
    
    def isAs(self):
        # Devuelve True si la carta es un As (valor 1)
        return self.valor == 1

# Clase que representa un mazo de cartas
class Deck:
    def __init__(self):
        self.cards: list = self.reset()  # Inicializa el mazo con 64 cartas
    
    def __str__(self):
        return f'cards: {len(self.cards)}'
    
    def __repr__(self):
        return f'cards: {len(self.cards)}'
    
    def __len__(self):
        return len(self.cards)

    def reset(self):
        """
        Crea un nuevo mazo de 64 cartas (16 valores por 4 palos),
        y asigna el valor 10 a las figuras (J, Q, K, A > 10)
        """
        res = []
        for i in range(1, 17):  # Valores del 1 al 16 (pero todo lo mayor a 10 se cuenta como 10)
            v = i
            if i > 10:
                v = 10
            res.append(Card(v, "diamonds"))
            res.append(Card(v, "spades"))
            res.append(Card(v, "clubs"))
            res.append(Card(v, "hearts"))
        return res

    def shuffle(self):
        # Mezcla las cartas del mazo
        random.shuffle(self.cards)

    def getCard(self):
        # Devuelve una carta aleatoria del mazo (sin removerla del mazo)
        return random.choice(self.cards)


# Clase que representa un jugador de Blackjack
class Player:
    def __init__(self, deck : Deck):
        self.mano = []          # Lista de cartas en la mano
        self.balance = 10000    # Saldo inicial del jugador
        self.deck = deck        # Referencia al mazo
        # Toma dos cartas iniciales
        for i in range(0, 2):
            self.mano.append(deck.getCard())
    
    def takeCard(self):
        # Toma una carta del mazo y la agrega a la mano
        self.mano.append(self.deck.getCard())
        return self.mano
    
    def hitOrStand(self):
        """
        Pregunta al jugador si quiere "hit" (pedir), "stand" (quedarse) o "split" (si es posible).
        Calcula el total de puntos y determina si se pasó o continúa.
        Devuelve:
        - un número entero si el jugador se quedó
        - "lose" si se pasó de 21
        - la mano si continúa
        """
        puntos = 0

        # Si las dos cartas iniciales son del mismo valor, se puede hacer split
        if self.mano[0].valor == self.mano[1].valor:
            desicion = input("split, hit, or stand ").lower()
            
            if desicion == "hit":
                self.takeCard()
                for carta in self.mano:
                    puntos += carta.valor
                    if puntos > 21:
                        print("Te pasaste con:", puntos)
                        return "lose"
            
            elif desicion == "stand":
                for carta in self.mano:
                    puntos += carta.valor
                return puntos
            
            elif desicion == "split":
                # Divide la mano en dos listas de una sola carta cada una
                lado1 = self.mano[0]
                lado2 = self.mano[1]
                self.mano.clear()
                self.mano.append([lado1])
                self.mano.append([lado2])
            
            else:
                print("No es una respuesta válida")

        else:
            # No puede hacer split, solo hit o stand
            desicion = input("hit, or stand ").lower()
            
            if desicion == "hit":
                self.takeCard()
                for carta in self.mano:
                    puntos += carta.valor
                    if puntos > 21:
                        print("Te pasaste con:", puntos)
                        return "lose"
            
            elif desicion == "stand":
                for carta in self.mano:
                    puntos += carta.valor
                    print("Puntos:", puntos)
                return puntos

        # Si no se tomó ninguna decisión final, devuelve la mano como está
        return self.mano


# Se crea una instancia del mazo para el juego
mazo = Deck()
