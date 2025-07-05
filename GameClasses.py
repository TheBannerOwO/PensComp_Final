# -*- coding: utf-8 -*-

"""
Este script contiene las clases esenciales del juego.
"""

from enum import Enum
import random, os, sys


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


    # Devuelve el valor practico en vez del real.
    @property
    def value(self):
        return 10 if self._value > 10 else self._value


    @value.setter
    def value(self, val: int ):
        if val > 13 or val < 1:
            raise Exception("Invalid card value")
        
        self._value: int = val


    def __str__(self):
        string =  f' {self.prettyValue()} {self.suit} '
        if self.suit == Suits.DIAMOND or self.suit == Suits.HEART:
            return '\033[31;47m' + string + '\033[0m'
        return f'\033[7m' + string + '\033[0m'
    

    __repr__ = __str__

    # Usa el valor real para devolver la letra correspondiente.
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



# ! Parte principal de la consigna 1
# Clase que representa un mazo de cartas
class Deck:

    def __init__(self, shuffled=False):
        self.cards: list[Card] = self.newDeck()  # Inicializa el mazo con 64 cartas
        if shuffled:
            self.shuffle()


    def __str__(self):
        return f'cards: {len(self.cards)}'
    

    def __repr__(self):
        return f'cards: {len(self.cards)}'
    

    def __len__(self):
        return len(self.cards)


    def newDeck(self):
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
        try:
            return self.cards.pop()
        except:
            return None



# ! Parte principal de la consigna 2
# Clase que representa un conjunto de mazos,
# es la forma principal en la que se deberia interactuar con los mazos.
class ConjoinedDeck:

    # Se pueden pasar mazos existentes para referenciar,
    # o pedir que se creen X cantidad de mazos nuevos para usar.
    def __init__(self, *args: Deck, newDecks=0, shuffled=False):
        if len(args) == 0 and newDecks == 0:
            raise Exception('ConjoinedDeck needs at least one deck to initialize')
        
        if newDecks < 0:
            raise Exception('Invalid amount of new decks')
            
        self.decks: list[Deck] = []
    
        for deck in args:
            if not isinstance(deck, Deck):
                raise Exception('ConjoinedDeck only accepts Deck instances as *args')
            self.decks.append(deck)
        
        for i in range(newDecks):
            self.decks.append(Deck())
        
        if shuffled:
            self.shuffle()


    def __str__(self):
        res = ''
        for i, deck in enumerate(self.decks):
            res += f'Deck[{i}]: {str(deck)}, '
        return res
    

    def __repr__(self):
        res = ''
        for i, deck in enumerate(self.decks):
            res += f'Deck[{i}]: {str(deck)}, '
        return res


    def __len__(self):
        return len(self.decks)


    def reset(self):
        for i in range(len(self.decks)):
            self.decks[i].cards = self.decks[i].newDeck()


    def shuffle(self):
        for deck in self.decks:
            deck.shuffle()
        random.shuffle(self.decks)


    def printDecks(self):
        for i, deck in enumerate(self.decks):
            print(f'\nDeck[{i}]: ', end="")
            print(deck.cards)


    def getCard(self):
        deckAmt = len(self.decks)
        used = []

        while len(used) != deckAmt:

            while len(used) != deckAmt:
                n = random.randint(0, deckAmt-1)
                if n in used:
                    continue

                card = self.decks[n].getCard()

                if card != None:
                    return card
                
                used.append(n)
            
            self.reset()



# Esta clase representa al crupier,
# y se usa como base para crear un jugador
class Crupier:

    def __init__(self, deck: Deck | ConjoinedDeck):
        self.hand: list[Card] = []
        self.deck: ConjoinedDeck | Deck = deck
    

    def __str__(self):
        return f'Crupier: {' '.join([str(card) for card in self.hand])} ({self.handValue()})'

    __repr__ = __str__


    # ! Consigna 3
    # Agarra una carta del mazo y la agrega a la mano,
    # devuelve la carta que se agarró.
    def takeCard(self):
        card = self.deck.getCard()
        self.hand.append(card)
        return card

    
    # ! Consigna 4
    # Calcula el valor total de la mano.
    def handValue(self):
        total = 0
        aces = 0
        for card in self.hand:
            if card.value != 1:
                total += card.value
            else:
                aces += 1

        for _ in range(aces):
            if total + 11 > 21:
                total += 1
            else:
                total += 11
        
        return total



# Clase que representa un jugador.
class Player(Crupier):

    def __init__(self, name: str, deck: ConjoinedDeck | Deck, balance: int = 500):
        self.name: str = name
        self.hand: list[Card] = []    # Lista de cartas en la mano
        self.balance: int = balance    # Saldo inicial del jugador
        self.deck: ConjoinedDeck | Deck = deck    # Referencia a los mazos

        # Estadisticas. Las partidas donde
        # la apuesta se recupera no se cuentan.
        self.stats: dict = {
            "wins": 0,
            "loses": 0,
        }
    
    def __str__(self):
        return f'{self.name}: {' '.join([str(card) for card in self.hand])} ({self.handValue()})'

    __repr__ = __str__

    # Devuelve la cantidad de plata pedida,
    # si el jugador no tiene suficiente devuelve 0.
    def extractBalance(self, amount: int):
        if amount < 1 or not isinstance(amount, int):
            return 0

        if self.balance >= amount:
            self.balance -= amount
        else:
            return 0
        return amount



# ! Parte esencial de la consigna 9
# Esta clase representa un bot
class Bot(Player):

    def __init__(self, name: str, deck: ConjoinedDeck | Deck, umbral: int = 17, balance = 10000):
        # Esta variable representa el numero con el que va
        # a comparar su mano para saber si dejar de pedir cartas.
        self.umbral: int = umbral

        super().__init__(name, deck, balance)
    
    def __str__(self):
        return f'{self.name} (u={self.umbral}): {' '.join([str(card) for card in self.hand])} ({self.handValue()})'

    __repr__ = __str__



# Asegura que el codigo de testing no va a correr si el juego arranca
if __name__ == '__main__':
    mazo = Deck()

    print(mazo)
    print(mazo.cards)