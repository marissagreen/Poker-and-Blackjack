#  File: Poker.py

#  Description: Using objects-oriented programming, simulate the game of poker. Have Card, Deck, and Poker classes. Prints out hands, the types of hand, and who won/tied.

#  Student Name: Marissa Green

#  Student UT EID: mdg3554

#  Course Name: CS 313E

#  Unique Number: 50725

#  Date Created: 2/17/19 

#  Date Last Modified: 2/18/19

import random

class Card(object):
    # global variables
    RANKS = (2,3,4,5,6,7,8,9,10,11,12,13,14)
    SUITS = ("C","H","S","D")

    def __init__(self, rank = 12, suit = "S"):
        # default is Queen of spades
        if (rank in Card.RANKS):
            self.rank = rank
        else:
            self.rank = 12

        if (suit in Card.SUITS):
            self.suit = suit
        else:
            self.suit = "S"

    # string representation of a Card object
    def __str__(self):
        if self.rank == 14:
            rank = "A"
        elif self.rank == 13:
            rank = "K"
        elif self.rank == 12:
            rank = "Q"
        elif self.rank == 11:
            rank = "J"
        else:
            rank = str(self.rank)
        return rank + self.suit

    # override equal function because card equality is object, not just a #
    # all suits are equal value, so only rank matters
    def __eq__(self,other):
        return self.rank == other.rank
    def __ne__(self,other):
        return self.rank != other.rank
    def __gt__(self,other):
        return self.rank > other.rank
    def __ge__(self,other):
        return self.rank >= other.rank
    def __lt__(self,other):
        return self.rank < other.rank
    def __le__(self,other):
        return self.rank <= other.rank

class Deck(object):

    def __init__(self, num_decks = 1):
        self.deck = [ ]
        for i in range(num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    card = Card(rank,suit)
                    self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    # deal one card at a time
    def deal(self):
        if len(self.deck) == 0: # if deck is empty, can't deal
            return None
        else:
            return self.deck.pop(0) # removes and returns first card


# how game is played - people, 2D list of 5 cards, players (>2, <5)
class Poker(object):

    def __init__(self, num_players = 2, num_cards = 5):
        self.deck = Deck() # default 1 deck
        self.deck.shuffle()
        self.all_hands = [ ]
        self.num_cards_in_hand = num_cards

        # deal cards one to each person, 5 times
        for i in range(num_players):
            hand = [ ]
            for j in range(self.num_cards_in_hand):
                hand.append(j)
            self.all_hands.append(hand)
        for k in range(self.num_cards_in_hand):
            for l in range(num_players):
                self.all_hands[l][k] = self.deck.deal()

    # simulate the play of poker
    def play(self):
        # need to sort each person's hand
        for i in range(len(self.all_hands)): # going through one hand at a time
            sorted_hand = sorted(self.all_hands[i], reverse = True) # reverse = True sorts in descending order, can sort because of 6 equality tests

            # replace unsorted hand with sorted hand
            self.all_hands[i] = sorted_hand

            # create string of all cards in hand
            hand_str = " "
            for card in sorted_hand:
                hand_str = hand_str + str(card) + " "
            print("Player "+str(i+1)+":"+hand_str)

        # need to determine the type of hand, points for that hand, and print
        hand_type = [ ] 
        hand_points = [ ]
        for i in range(len(self.all_hands)):

            royal_points, royal_type = Poker.is_royal(self,self.all_hands[i])
            straight_flush_points, straight_flush_type = Poker.is_straight_flush(self,self.all_hands[i])
            four_kind_points, four_kind_type = Poker.is_four_kind(self,self.all_hands[i])
            full_house_points, full_house_type = Poker.is_full_house(self,self.all_hands[i])
            flush_points, flush_type = Poker.is_flush(self,self.all_hands[i])
            straight_points, straight_type = Poker.is_straight(self,self.all_hands[i])
            three_kind_points, three_kind_type = Poker.is_three_kind(self,self.all_hands[i])
            two_pair_points, two_pair_type = Poker.is_two_pair(self,self.all_hands[i])
            one_pair_points, one_pair_type = Poker.is_one_pair(self,self.all_hands[i])
            high_card_points, high_card_type = Poker.is_high_card(self,self.all_hands[i])

            # determine type and add type to list
            if royal_points > 0:
                hand_type.append(royal_type)
                hand_points.append(royal_points)
            elif straight_flush_points > 0:
                hand_type.append(straight_flush_type)
                hand_points.append(straight_flush_points)
            elif four_kind_points > 0:
                hand_type.append(four_kind_type)
                hand_points.append(four_kind_points)
            elif full_house_points > 0:
                hand_type.append(full_house_type)
                hand_points.append(full_house_points)
            elif flush_points > 0:
                hand_type.append(flush_type)
                hand_points.append(flush_points)
            elif straight_points > 0:
                hand_type.append(straight_type)
                hand_points.append(straight_points)
            elif three_kind_points > 0:
                hand_type.append(three_kind_type)
                hand_points.append(three_kind_points)
            elif two_pair_points > 0:
                hand_type.append(two_pair_type)
                hand_points.append(two_pair_points)
            elif one_pair_points > 0:
                hand_type.append(one_pair_type)
                hand_points.append(one_pair_points)
            elif high_card_points > 0:
                hand_type.append(high_card_type)
                hand_points.append(high_card_points)
            else:
                print("ERROR, NO TYPE OF HAND FOUND")

        # print type of hand
        print()
        for i in range(len(self.all_hands)):
            print("Player "+str(i+1)+": "+hand_type[i])
        print()

        # determine winning hand type and how many hands won
        winner_points = max(hand_points)
        winner_index = hand_points.index(winner_points)
        winner_type = hand_type[winner_index]
        count = hand_type.count(winner_type)

        # make dictionary for player : points
        dictionary = { }
        for j in range(len(hand_type)):
            if hand_type[j] == winner_type:
                dictionary[j+1] = hand_points[j]

        # print winner/ties
        if count == 1:
            print("Player",winner_index + 1,"wins.")
        elif count > 1:
            while count >= 1:
                max_value = max(dictionary, key=dictionary.get)
                del dictionary[max_value]
                print("Player",max_value, "ties.")
                count -= 1        
            
    # 10 types of hands
    def is_royal(self,hand):
        # must be all same suit
        same_suit = True
        for i in range(len(hand) - 1):
            same_suit = same_suit and (hand[i].suit == hand[i+1].suit)
        if (not same_suit):
            return 0, " "

        # must be numerically straight
        rank_order = True
        for i in range(len(hand)):
            rank_order = rank_order and (hand[i].rank == 14-i)
        if (not rank_order):
            return 0, " "

        points = (10 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        return points, "Royal Flush"

    def is_straight_flush(self,hand):
        rank_order = True
        for i in range(len(hand)):
            rank_order = rank_order and (hand[i].rank == 14-i)

        same_suit = False
        if hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit == hand[4].suit:
            same_suit = True

        if same_suit and rank_order:
            points = (9 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
            return points, "Straight Flush"
        else:
            return 0, " "

    def is_four_kind(self,hand):
        four_kind = False

        # lower 4 are four of a kind
        if hand[0].rank == hand[1].rank == hand[2].rank == hand[3].rank:
            four_kind = True
            points = (8 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        # higher four are four of a kind
        elif hand[1].rank == hand[2].rank == hand[3].rank == hand[4].rank:
            four_kind = True
            points = (8 * 15**5) + (hand[1].rank * 15**4) + (hand[2].rank * 15**3) + (hand[3].rank * 15**2) + (hand[4].rank * 15) + (hand[0].rank)

        if four_kind:
            return points, "Four of a Kind"
        else:
            return 0, " "

    def is_full_house(self,hand):
        full_house = False

        # same rank in pair, then triplet
        if hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank == hand[4].rank:
            full_house = True
            points = (7 * 15**5) + (hand[2].rank * 15**4) + (hand[3].rank * 15**3) + (hand[4].rank * 15**2) + (hand[0].rank * 15) + (hand[1].rank)

        # same rank in triplet, then pair
        elif hand[0].rank == hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
            full_house = True
            points = (7 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)

        if full_house:
            return points, "Full House"
        else:
            return 0, " "
        
    def is_flush(self,hand):

        if hand[0].suit == hand[1].suit == hand[2].suit == hand[3].suit == hand[4].suit:
            points = (6 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
            return points, "Flush"

        return 0, " "

    def is_straight(self,hand):
        rank_order = True
        for i in range(len(hand)):
            rank_order = rank_order and (hand[i].rank == 14-i)
        if (not rank_order):
            return 0, " "

        points = (5 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        return points, "Straight"

    def is_three_kind(self,hand):
        three_kind = False

        # first three are same
        if hand[0].rank == hand[1].rank == hand[2].rank:
            three_kind = True
            points = (4 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        
        # middle three are same
        elif hand[1].rank == hand[2].rank == hand[3].rank:
            three_kind = True
            points = (4 * 15**5) + (hand[1].rank * 15**4) + (hand[2].rank * 15**3) + (hand[3].rank * 15**2) + (hand[0].rank * 15) + (hand[4].rank)

        # last three are same
        elif hand[2].rank == hand[3].rank == hand[4].rank:
            three_kind = True
            points = (4 * 15**5) + (hand[2].rank * 15**4) + (hand[3].rank * 15**3) + (hand[4].rank * 15**2) + (hand[0].rank * 15) + (hand[1].rank)                                                                                                                             

        if three_kind:
            return points, "Three of a Kind"
        else:
            return 0, " "

    def is_two_pair(self,hand):
        two_pair = False

        # unmatched card is first
        if hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
            two_pair = True
            points = (3 * 15**5) + (hand[1].rank * 15**4) + (hand[2].rank * 15**3) + (hand[3].rank * 15**2) + (hand[4].rank * 15) + (hand[0].rank)

        # unmatched card is middle
        if hand[0].rank == hand[1].rank and hand[3].rank == hand[4].rank:
            two_pair = True
            points = (3 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[3].rank * 15**2) + (hand[4].rank * 15) + (hand[2].rank)

        # unmatched card is last
        if hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank:
            two_pair = True
            points = (3 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)

        if two_pair:
            return points, "Two Pair"
        else:
            return 0, " "

    def is_one_pair(self,hand):
        one_pair = False
        if hand[0].rank == hand[1].rank:
            one_pair = True
            points = (2 * 15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        elif hand[1].rank == hand[2].rank:
            one_pair = True
            points = (2 * 15**5) + (hand[1].rank * 15**4) + (hand[2].rank * 15**3) + (hand[0].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        elif hand[2].rank == hand[3].rank:
            one_pair = True
            points = (2 * 15**5) + (hand[2].rank * 15**4) + (hand[3].rank * 15**3) + (hand[0].rank * 15**2) + (hand[1].rank * 15) + (hand[4].rank)
        elif hand[3].rank == hand[4].rank:
            one_pair = True
            points = (2 * 15**5) + (hand[3].rank * 15**4) + (hand[4].rank * 15**3) + (hand[0].rank * 15**2) + (hand[1].rank * 15) + (hand[2].rank)
        
        if one_pair:
            return points, "One Pair"
        else:
            return 0, " "

    def is_high_card(self,hand):
        points = (15**5) + (hand[0].rank * 15**4) + (hand[1].rank * 15**3) + (hand[2].rank * 15**2) + (hand[3].rank * 15) + (hand[4].rank)
        return points, "High Card"

def main ():

    num_players = int(input("Enter number of players: "))
    while ((num_players < 2) or (num_players > 6)):
        num_players = int(input("Enter number of players: "))

    print()
    
    # create poker object
    game = Poker(num_players)

    game.play()

main ()
