import random

class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f'Value: {self.value} | Suit: {self.suit} '
    
    def __repr__(self):
        return f'Value: {self.value} | Suit: {self.suit} '
    
    
    
class Deck:
    def __init__(self):
        self.cards: list = self.reset()
    
    def __str__(self):
        return f'cards: {len(self.cards)}'
    
    def __repr__(self):
        return f'cards: {len(self.cards)}'
    
    def __len__(self):
        return len(self.cards)

    def reset(self):
        res = []
        for i in range(1, 17):
            v = i
            if i > 10:
                v = 10
            res.append(Card(v, "diamonds"))
            res.append(Card(v, "spades"))
            res.append(Card(v, "clubs"))
            res.append(Card(v, "hearts"))
        return res

    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        return self.cards.pop()



class ConjoinedDeck:
    def __init__(self, *args: Deck):
        self.decks = []
        for deck in args:
            self.decks.append(deck)
        
    def __str__(self):
        res = ''
        for i, deck in enumerate(self.decks):
            res += f'Deck[{i}]: {str(deck)}, '
        return res
    
    def __len__(self):
        return len(self.decks)
        
    def shuffle(self):
        for deck in self.decks:
            deck.shuffle()
        return random.shuffle(self.decks)
    
    def printDecks(self):
        for i, deck in enumerate(self.decks):
            print(f'\n\nDeck[{i}]: ', end="")
            for card in deck.cards:
                print(card, end="")
    
    def getCard(self):
        return self.decks[len(self.decks)-1].getCard()



class Crupier:
    def __init__(self, deck: Deck):
        self.hand: list = []
        self.deck = deck
    
    def hit(self):
        return self.deck.getCard()

Deck.getCard()