from enum import Enum
import random


class Suits(Enum):
    SPADE: str = "♠"
    HEART: str = "♥"
    CLUB: str = "♣"
    DIAMOND: str = "♦"

    def __str__(self):
        return self.value


# Clase que representa una carta individual
class Card: 
    def __init__(self, value: int, suit: str):
        self.suit: str = suit
        self._value: int = value
    
    @property
    def value(self):
        return 10 if self._value > 10 else self._value
    
    @value.setter
    def value(self, val: int ):
        if val > 13 or val < 1:
            raise Exception("Invalid card value")
        
        self._value: int = val

    def __str__(self):
        return f'value: {self.prettyValue()} | suit: {self.suit}'
    
    def __repr__(self):
        return f'value : {self.prettyValue()} | suit {self.suit}'
    
    def prettyValue(self):
        match self._value:
            case 1:
                return 'A'
            case 11:
                return 'J'
            case 12:
                return 'Q'
            case 13:
                return 'K'
        return self._value
    
    def isAs(self):
        # Devuelve True si la carta es un As (valor 1)
        return self._value == 1


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
        Crea un nuevo mazo de 64 cartas (14 cartas para cada palo)
        """
        res = []
        for value in range(1, 14):
            for suit in [Suits.CLUB, Suits.HEART, Suits.SPADE, Suits.DIAMOND]:
                res.append(Card(value, suit))
        return res

    def shuffle(self):
        # Mezcla las cartas del mazo
        random.shuffle(self.cards)

    def getCard(self):
        # ! Devuelve la carta en la cima del mazo.
        return self.cards.pop()



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
        if self.mano[0].value == self.mano[1].value:
            desicion = input("split, hit, or stand ").lower()
            
            if desicion == "hit":
                self.takeCard()
                for carta in self.mano:
                    puntos += carta.value
                    if puntos > 21:
                        print("Te pasaste con:", puntos)
                        return "lose"
            
            elif desicion == "stand":
                for carta in self.mano:
                    puntos += carta.value
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
                    puntos += carta.value
                    if puntos > 21:
                        print("Te pasaste con:", puntos)
                        return "lose"
            
            elif desicion == "stand":
                for carta in self.mano:
                    puntos += carta.value
                    print("Puntos:", puntos)
                return puntos

        # Si no se tomó ninguna decisión final, devuelve la mano como está
        return self.mano