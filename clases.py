#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 14:24:12 2025

@author: Estudiante
"""

import random

class Card: 
    def __init__(self, valor, palo):
        self.palo = palo
        self.valor = valor
    
    def __str__(self):
        return f'valor: {self.valor} | palo: {self.palo}'
    
    def __repr__(self):
        return f'valor : {self.valor} | palo {self.palo}'
    
    def isAs(self):
        if self.valor == 1:
            return True 
        
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
        return random.choice(self.cards)


class Player:
    
    def __init__(self, deck : Deck):
        self.mano = []
        self.balance = 10000
        self.deck = deck
        for i in range(0,2):
            self.mano.append(deck.getCard())
    
    def win(self):
        self.balance = self.balance * 2
    
    def lose(self):
        self.balance = self.balance - apuesta#se hará después
    
    def draw(self):
        self.balance = self.balance 
    
    def takeCard(self):
        self.mano.append(self.deck.getCard())
        return self.mano
    
        
    def hitOrStand(self):
        puntos = 0
        if self.mano[0].valor == self.mano[1].valor:
            desicion = input("split, hit, or stand ")
            if desicion == "hit":
                self.takeCard()
                for i in range(len(self.mano)):
                    puntos = puntos + self.mano[i].valor
                    if puntos > 21:
                        print("te pasaste con : ", puntos)
                        return "lose"
            elif desicion == "stand":
                for i in range(len(self.mano)):
                    puntos = puntos + self.mano[i].valor
                return puntos
            elif desicion == "split":
                lado1 = self.mano[0]
                lado2 = self.mano[1]
                self.mano.clear()
                self.mano.append([lado1])
                self.mano.append([lado2])
            else:
                print("No es una respuesta")
        else:
            desicion = input("hit, or stand ")
            if desicion == "hit":
                self.takeCard()
                for i in range(len(self.mano)):
                    puntos = puntos + self.mano[i].valor
                    if puntos > 21:
                        print("te pasaste con : ", puntos)
                        return "lose"
            elif desicion == "stand":
                for i in range(len(self.mano)):
                    puntos = puntos + self.mano[i].valor
                    print(puntos)
                return puntos
        return self.mano
#def bet(player : Player):
    

mazo = Deck()
