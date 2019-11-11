#  File: Blackjack.py

#  Description: Simulated a game of blackjack using OOP - Card, Deck, Player, Dealer, and Blackjack classes. 

#  Student Name: Marissa Green

#  Student UT EID: mdg3554

#  Course Name: CS 313E

#  Unique Number: 50725

#  Date Created: 2/23/19

#  Date Last Modified: 2/23/19

import random

class Card (object):
    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

    SUITS = ('C', 'D', 'H', 'S')

    def __init__ (self, rank = 12, suit = 'S'):
        if (rank in Card.RANKS):
            self.rank = rank
        else:
            self.rank = 12

        if (suit in Card.SUITS):
            self.suit = suit
        else:
            self.suit = 'S'

    # string representation of a Card object
    def __str__ (self):
        if (self.rank == 1):
            rank = 'A'
        elif (self.rank == 13):
            rank = 'K'
        elif (self.rank == 12):
            rank = 'Q'
        elif (self.rank == 11):
            rank = 'J'
        else:
            rank = str (self.rank)
        return rank + self.suit

    # equality tests
    def __eq__ (self, other):
        return self.rank == other.rank

    def __ne__ (self, other):
        return self.rank != other.rank

    def __lt__ (self, other):
        return self.rank < other.rank

    def __le__ (self, other):
        return self.rank <= other.rank

    def __gt__ (self, other):
        return self.rank > other.rank

    def __ge__ (self, other):
        return self.rank >= other.rank

class Deck (object):
    
    def __init__ (self, num_decks = 1):
        self.deck = [ ]
        for i in range (num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    card = Card (rank, suit)
                    self.deck.append (card)

    # shuffle the deck
    def shuffle (self):
        random.shuffle (self.deck)

    # deal a card
    def deal (self):
        if (len(self.deck) == 0):
            return None
        else:
            return self.deck.pop(0)

class Player (object):
    
    # cards is a list of Card objects
    def __init__ (self, cards):
        self.cards = cards

    # when a player hits append a card
    def hit (self, card):
        self.cards.append (card)

    # count the points in the Player's hand
    def get_points (self):
        count = 0
        for card in self.cards:
            if (card.rank > 9):
                count += 10
            elif (card.rank == 1):
                count += 11
            else:
                count += card.rank

        # deduct 10 if Ace is there and needed as 1
        for card in self.cards:
            if (count <= 21):
                break
            elif (card.rank == 1):
                count = count - 10

        return count

    # does the player have blackjack
    def has_blackjack (self):
        return (len(self.cards) == 2) and (self.get_points() == 21)

    # string representation of the cards and points in the hand
    def __str__ (self):
        hand_str = " "
        for card in self.cards:
            hand_str = hand_str + str(card) + " "
        return hand_str+"- "+str(self.get_points())+" points"

class Dealer (Player):
    def __init__ (self, cards):
        Player.__init__ (self, cards)
        self.show_one_card = True

    # over-ride the hit() function in the parent class
    def hit (self, deck):
        self.show_one_card = False
        while (self.get_points() < 17):
            self.cards.append (deck.deal())

    # return a string showing just one card if not hit yet
    def __str__ (self):
        if (self.show_one_card):
            return str(self.cards[0])
        else:
            return Player.__str__(self)

class Blackjack (object):
    def __init__ (self, num_players = 1):
        self.deck = Deck ()
        self.deck.shuffle()

        # create the number of Player objects
        self.num_players = num_players
        self.player_list = []

        for i in range (self.num_players):
            player = Player ([self.deck.deal(), self.deck.deal()])
            self.player_list.append (player)

        # create the Dealer object
        # dealer also get two cards
        self.dealer = Dealer ([self.deck.deal(), self.deck.deal()])

    def play (self):
        # print the cards that each player has
        print()
        for i in range (self.num_players):
            print ('Player ' + str(i + 1) + ':' + str(self.player_list[i]))

        # print the cards that the dealer has
        print ('Dealer: ' + str(self.dealer))
        print()

        # each player hits until he says no
        player_points = [ ]
        for i in range (self.num_players):
            while True:
                print("Player " + str(i+1)+", ",end = "")
                choice = input ("do you want to hit? [y / n]: ")
                if choice in ('y', 'Y'):
                    (self.player_list[i]).hit (self.deck.deal())
                    points = (self.player_list[i]).get_points()
                    print ('Player ' + str(i + 1) + ': ' + str(self.player_list[i]))
                    if (points >= 21):
                        break
                else:
                    break
            print()
            player_points.append ((self.player_list[i]).get_points())

        # dealer's turn now
        self.dealer.hit (self.deck)
        dealer_points = self.dealer.get_points()
        print ('Dealer:' + str(self.dealer))
        print()
        
        # determine the outcome
        for i in range(self.num_players):
            if (Player.has_blackjack(self.player_list[i])):
                print ("Player", i+1, "wins")
            elif (player_points[i] > 21):
                print ("Player", i+1, "loses")
            elif (dealer_points <= 21) and (dealer_points > player_points[i]):
                print ("Player", i+1, "loses")
            elif (dealer_points < player_points[i]):
                print ("Player", i+1, "wins")
            elif (dealer_points == player_points[i]):
                print ("Player", i+1, "ties")
            else:
                print ("Player", i+1, "wins")
                
def main():
    # prompt the user to enter the number of players
    num_players = int (input ('Enter number of players: '))
    while ((num_players < 1) or (num_players > 6)):
        num_players = int (input ('Enter number of players: '))
    
    # create the Blackjack object
    game = Blackjack (num_players)

    # play the game
    game.play()

main()