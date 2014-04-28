""" Deck class - to be used for any card game.
This current version does not incorporate Ace Low rules.

Key for reading the card values:

card = [facevalue, suit]

Suits
1 = Spade
2 = Club
3 = Heart
4 = Diamond
5 = Joker

Face Values
1 = 2
2 = 3
3 = 4
4 = 5
5 = 6
6 = 7
7 = 8
8 = 9
9 = 10
10 = Jack
11 = Queen
12 = King
13 = Ace
"""
from random import shuffle


class Deck:
    
    def __init__(self, decks = 1, jokers = 0, shuf = True):

        self.drawpile = []
        self.discardpile = []
        self.cardvalues = {1:'Two',
              2:'Three',
              3:'Four',
              4:'Five',
              5:'Six',
              6:'Seven',
              7:'Eight',
              8:'Nine',
              9:'Ten',
              10:'Jack',
              11:'Queen',
              12:'King',
              13:'Ace'
              }

        for i in range(decks):

            for s in [1,2,3,4]:

                for f in range(13):

                    self.drawpile.append([f + 1,s])


        if jokers > 0:

            for i in range(jokers):

                self.drawpile.append([0,5])

        if shuf == True:

            shuffle(self.drawpile)

    

    #place variable allows pulling from different locations in the pile.  Must be < len(self.drawpile) or an exception will be raised.
    def drawcard(self, place = 0):

        card = self.drawpile[place]

        self.discardpile.append(self.drawpile.pop(place))

        return card

    def shuffledeck(self):

        shuffle(self.drawpile)

    def deal(self):

        return self.drawpile.pop(0)

    def discard(self, card):

        self.discardpile.append(card)
                
    def check_cards(self):

        cardlist = []

        for i in self.drawpile:

            card = ''

            card += (self.cardvalues[i[0]] + ' of ')

            if i[1] == 1:

                card += 'Spades'

            elif i[1] == 2:

                card += 'Clubs'

            elif i[1] == 3:

                card += 'Hearts'

            elif i[1] == 4:

                card += 'Diamonds'

            cardlist.append(card)

        for i in cardlist:

            print i


