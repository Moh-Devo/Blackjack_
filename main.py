import random
import sys


class Card:
    def __init__(self, name, value, suit, symbol):
        self.name = name
        self.value = value
        self.suit = suit
        self.symbol = symbol

    def print_all(self):
        print(f"{self.name} of {self.suit} {self.symbol}")


class Suit:
    suits = []

    def __init__(self, name, symbol, color):
        self.__class__.suits.append(self)
        self.name = name
        self.symbol = symbol
        self.color = color


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in [spades, hearts, diamonds, clubs]:
            for v in card_value:
                self.cards.append(Card(v, card_value[v], s.name, s.symbol))


class Dealer:
    def __init__(self, name,):
        self.name = name
        self.hand = []
        self.highest_value = 0
        self.blackjack = False
        self.bust = False

    def show(self):
        self.adjust_highest_value()
        # print(f"{self.name}'s hand is...\n")
        if self.name == dealer.name:

            print("~~~~~~~~~~~~~~~")
            #print(self.name, "'s hand:\n")
            # print(f"{self.name}'s hand is...\n")
            for c in self.hand:
                c.print_all()
            #print("")
            print("~~~~~~~~~~~~~~~")
            print(f"{self.name}'s hand's value is: {self.highest_value}\n")
        else:
            # print(f"{self.name}'s hand is...\n")
            print("===============")
            # print(self.name, "'s hand:\n")
            # print(f"{self.name}'s hand is...\n")
            for c in self.hand:
                c.print_all()
            # print("")
            print("===============")
            print(f"{self.name}'s hand's value is: {self.highest_value}\n")

    def draw_card(self):
        draw = deck.cards.pop()
        self.hand.append(draw)
        self.adjust_highest_value()

    def adjust_highest_value(self):
        highest_value_list = []
        for x in self.hand:
            highest_value_list.append(x.value)

        for y in self.hand:
            if 'Ace' in y.name and sum(highest_value_list) > 21:
                highest_value_list.append(-10)
        self.highest_value = sum(highest_value_list)


class Player(Dealer):
    def __init__(self, name, chips):
        super().__init__(name)
        self.chips = chips
        self.bet = 0
        self.round_over = False

        self.split = False
        self.split_bet = 0
        self.split_hand = []
        self.split_bust = False


def choice_select(choice):
    while True:
        if choice in ['1', '2']:
            if choice == '1':
                return
            elif choice == '2':
                sys.exit()
        else:
            invalid_input()
            choice = input("Please input 1 for yes or 2 for no.\n")


def invalid_input():
    print("Invalid input. Please try again.\n")


def start_game():
    while True:
        try:
            bob.bet = int(input(f"Please place your bet. Minimum bet is 10 chips.\n"
                                f"Current chips: {bob.chips}\nBet: "))
            if bob.bet < 10:
                print("Please enter a bet with a minimum of 10 chips\n")
                continue
            elif bob.bet > bob.chips:
                print("You cannot bet more chips than you have.\n")
                continue
            print(f"-{bob.bet} Chips\n")
            bob.chips = bob.chips - bob.bet
        except ValueError:
            invalid_input()
            continue
        dealer.draw_card()
        dealer.show()

        while bob.round_over is False:
            player_turn()
            if bob.round_over is True:
                break
            dealer_turn()
            if bob.round_over is True:
                break
        check_win()
        end_round()


def player_turn():
    bob.draw_card()
    bob.draw_card()
    bob.show()

    if bob.highest_value == 21 and len(bob.hand) == 2:
        print("Blackjack!\n")
        bob.blackjack = True
        if dealer.highest_value == 10 or dealer.highest_value == 11:
            return
        else:
            bob.round_over = True
            return

    while True:
        choice = input("Do you wish to draw another card?"
                       "\n1: Hit me!\n2: Stay\n3: Double up!\n4: Split\n")
        if choice in ['1', '2', '3', '4']:

            if choice == '1':
                bob.draw_card()
                bob.show()
                show_hand_value(dealer)
                if bob.highest_value > 21:
                    print("You Busted!")
                    bob.bust = True
                    bob.round_over = True
                    return
                elif bob.highest_value == 21:
                    print("21 reached! You are unable to hit further.")
                    return

            elif choice == '2':
                return

            elif choice == '3' and len(bob.hand) == 2 or bob.split is True:
                bob.chips = bob.chips - bob.bet
                bob.bet = bob.bet * 2
                if bob.chips < 0:
                    invalid_input()
                    print("Not enough chips to double up!\n")
                    bob.bet = bob.bet // 2
                    bob.chips = bob.chips + bob.bet
                    continue
                print(f"- {bob.bet} Chips")
                bob.draw_card()
                bob.show()
                if bob.highest_value > 21:
                    print("You Busted!")
                    bob.bust = True
                    bob.round_over = True
                return

            elif choice == '4' and bob.hand[0].value == bob.hand[1].value and bob.split is False:
                bob.chips = bob.chips - bob.bet
                bob.split_bet = bob.bet
                if bob.chips < 0:
                    invalid_input()
                    print("Not enough chips to split!\n")
                    bob.bet = bob.bet // 2
                    bob.chips = bob.chips + bob.bet
                    continue
                print(f"- {bob.bet} Chips")
                print(f'You split your hand on a {bob.hand[0].name}\n')
                bob.split = True
                split_card = bob.hand.pop()
                bob.split_hand.append(split_card)
                bob.show()
                split()
                bob.split_hand = bob.hand.copy()
                bob.hand.clear()
                bob.hand.append(split_card)
                bob.show()

            else:
                invalid_input()
        else:
            invalid_input()


def split():
    while True:
        choice = input("Do you wish to draw another card?"
                       "\n1: Hit me!\n2: Stay\n3: Double up!\n")
        if choice in ['1', '2', '3']:

            if choice == '1':
                bob.draw_card()
                bob.show()
                show_hand_value(dealer)
                if bob.highest_value > 21:
                    print("You Busted on your first Split!")
                    bob.split_bust = True
                    return
                elif bob.highest_value == 21:
                    print("21 reached! You are unable to hit further on your first Split.")
                    return

            elif choice == '2':
                print(f"You stand on {bob.highest_value} on your first Split")
                return

            elif choice == '3' and len(bob.hand) == 1:
                bob.chips = bob.chips - bob.split_bet
                if bob.chips < 0:
                    invalid_input()
                    print("Not enough chips to double up!\n")
                    bob.chips = bob.chips + bob.split_bet
                    continue
                bob.split_bet = bob.split_bet * 2
                print(f"- {bob.split_bet} Chips")
                bob.draw_card()
                bob.show()
                if bob.highest_value > 21:
                    print("You Busted on your first Split!")
                    bob.bust = True
                return

            else:
                invalid_input()
        else:
            invalid_input()


def dealer_turn():
    while True:
        dealer.draw_card()
        dealer.show()
        if len(dealer.hand) == 2 and dealer.highest_value == 21:
            dealer.blackjack = True
            bob.round_over = True
            return
        if dealer.highest_value < 17:
            input("Press enter to see the dealers next card...")
        elif dealer.highest_value in range(17, 22):
            bob.round_over = True
            return
        elif dealer.highest_value > 21:
            dealer.bust = True
            bob.round_over = True
            return


def check_win():
    while True:
        if dealer.bust is True:
            bob.chips = bob.chips + (bob.bet * 2)
            print(f"You win! +{bob.bet * 2} Chips\nYou now have a total of {bob.chips} chips!\n")
            break
        elif bob.bust is True:
            print(f"Busted! You lose! -{bob.bet} Chips\nYou now have a total of {bob.chips} chips!\n")
            break
        elif bob.blackjack is True and dealer.blackjack is False:
            bob.chips = int(bob.chips + (bob.bet * 2.5))
            print(f"You win! +{int(bob.bet * 2.5)} Chips\nYou now have a total of {bob.chips} chips!")
            break
        elif dealer.blackjack is True and bob.blackjack is False:
            print(f"You lose! -{bob.bet} Chips\nYou now have a total of {bob.chips} chips!")
            break
        elif bob.blackjack is True and dealer.blackjack is True:
            print("Unfortunate! The dealer also had a blackjack.\n")
            bob.chips = bob.chips + bob.bet
            print("Draw!\nYou don't win, nor lose, anything.")
            break
        elif dealer.highest_value > bob.highest_value:
            print(f"You lose! -{bob.bet} Chips\nYou now have a total of {bob.chips} chips!")
            break
        elif bob.highest_value > dealer.highest_value:
            bob.chips = bob.chips + (bob.bet * 2)
            print(f"You win! +{bob.bet * 2}\nYou now have a total of {bob.chips} chips!")
            break
        else:
            bob.chips = bob.chips + bob.bet
            print("Draw!\nYou don't win, nor lose, anything.")
            break
    if bob.split is True:
        bob.hand = bob.split_hand.copy()
        bob.bust = bob.split_bust
        bob.bet = bob.split_bet
        bob.split = False
        bob.adjust_highest_value()
        check_win()


def end_round():
    deck.__init__()
    random.shuffle(deck.cards)
    dealer.hand.clear()
    dealer.highest_value = 0
    dealer.bust = False
    dealer.blackjack = False
    bob.hand.clear()
    bob.highest_value = 0
    bob.bust = False
    bob.blackjack = False
    bob.round_over = False
    bob.split = False
    bob.split_hand.clear()
    bob.split_bust = False
    bob.split_bet = 0

    if bob.chips < 10:
        print("You do not have the required chips to play at this table anymore.")
        sys.exit()
    choice = input("Do you wish to play another round?\n1: Yes\n2: Quit\n")
    choice_select(choice)
    print("")


def show_hand_value(self):
    print(f"{self.name}'s hand's value is: {self.highest_value}\n")


spades = Suit("Spades", '♠', 'Black')
hearts = Suit("Hearts", '♥', 'Red')
diamonds = Suit("Diamonds", '♦', 'Red')
clubs = Suit("Clubs", '♣', 'Black')

card_value = {'Ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
              '8': 8, '9': 9, '10': 10, 'Joker': 10, 'Queen': 10, 'King': 10}

deck = Deck()
random.shuffle(deck.cards)
bob = Player("Bob", 10000)
dealer = Dealer("Dealer")
with open("Introduction") as f:
    print(f.read())
    print("")

print("This is a game of Blackjack. Do you wish to play?")
game_start = input("1: Begin\n2: Quit\n")
choice_select(game_start)

start_game()
