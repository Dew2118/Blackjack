import curses
import random
from collections import deque
from time import sleep


class Display:
    SUIT_CHR = {'S': '\u2660', 'H': '\u2665', 'D': '\u2666', 'C': '\u2663'}

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def display(self, y, x, value, suit):
        self.value = value
        self.suit = suit
        self.display_card_skeleton(y * 7, x * 7)
        self.display_card_symbol(y * 7, x * 7)

    def display_card_skeleton(self, y, x):
        for a in range(6):
            self.stdscr.addstr(y, x + a, '#')
            self.stdscr.addstr(y + 6, x + a, '#')
        for b in range(7):
            self.stdscr.addstr(y + b, x, '#')
            self.stdscr.insstr(y + b, x + 6, '#')
            self.refresh()

    def display_card_symbol(self, y, x):
        self.stdscr.addstr(y + 1, x + 1, self.value)
        self.stdscr.addstr(y + 1, x + 1 + len(str(self.value)), self.SUIT_CHR[self.suit])
        self.stdscr.addstr(y + 5, x + 4 - len(str(self.value)), self.value)
        self.stdscr.addstr(y + 5, x + 4, self.SUIT_CHR[self.suit])
        self.refresh()

    def display_decide(self, number, text):
        self.stdscr.addstr(37 + number * 2, 0, text)

    def display_blackjack(self, y):
        self.stdscr.addstr(y, 0, 'Black')
        self.stdscr.addstr(y + 1, 0, 'jack')

    def display_general_text(self, y, text):
        self.stdscr.addstr(y, 0, text)

    def display_text_times_seven(self, y, text):
        self.stdscr.addstr(y * 7, 0, text)

    def display_text(self, y, x, text):
        self.stdscr.addstr(y, x, text)

    def refresh(self):
        self.stdscr.refresh()

    def getstr(self, y, x):
        return self.stdscr.getstr(y, x)


class Card:
    SCORE = {'A': 1, 'J': 10, 'Q': 10, 'K': 10}

    def __init__(self, value, suit, display):
        self.display = display
        curses.echo()
        self.value = value
        self.suit = suit
        if value in 'AJQK':
            self.score = Card.SCORE[value]
        else:
            self.score = int(value)

    def get_score(self):
        return self.score

    def get_value(self):
        return self.value

    def _display(self, y, x):
        self.display.display(y, x, self.value, self.suit)


class Deck:
    def __init__(self, display):
        value = map(str, ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
        suit = ['C', 'H', 'S', 'D']
        self.cards = [Card(v, s, display) for v in (value) for s in (suit)]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, number_of_cards):
        return [self.cards.pop(0) for i in range(number_of_cards)]


class Hand:
    def __init__(self, name, player, display):
        self.cards = []
        self.name = name
        self.player = player
        self.card_count = 1
        self.display = display
        self.already_displayed = []

    def get_player(self):
        return self.player

    def get_name(self):
        return self.name

    def draw(self, deck, number_of_cards):
        self.cards.extend(deck.draw(number_of_cards))

    def is_blackjack(self, length=0):
        if len(self.cards) != 2:
            return False
        scores = [c.get_score() for c in self.cards]
        if sorted(scores) == [1, 10]:
            if self.name == 'dealer':
                self.display.display_general_text(2, 'Black')
                self.display.display_general_text(3, 'jack')
            elif length == 2:
                self.display.display_general_text(15, 'Black')
                self.display.display_general_text(16, 'jack')
            elif length == 3:
                self.display.display_general_text(22, 'Black')
                self.display.display_general_text(23, 'jack')
            elif length == 4:
                self.display.display_general_text(29, 'Black')
                self.display.display_general_text(30, 'jack')
            elif self.name == 'player1':
                self.display.display_blackjack(8)
            return True
        return False

    def get_score(self):
        return sum([c.get_score() for c in self.cards])

    def get_card_value(self, card_idx):
        try:
            return self.cards[card_idx].get_value()
        except Exception:
            pass

    def is_busted(self, length=0):
        if (self.get_score() > 21) == True:
            if self.name == 'dealer':
                self.display.display_general_text(5, 'Busted')
            elif length == 2:
                self.display.display_general_text(19, 'Busted')
            elif length == 3:
                self.display.display_general_text(26, 'Busted')
            elif length == 4:
                self.display.display_general_text(33, 'Busted')
            elif self.name == 'player1':
                self.display.display_general_text(12, 'Busted')
        return (self.get_score() > 21)

    def get_card(self, index):
        return self.cards[index]

    def add_card(self, card):
        self.cards.append(card)

    def display_and_replace(self, x, y):
        self.already_displayed_set = set(self.already_displayed)
        self.card_count = 1
        self.already_displayed.append(self.cards[0])
        for a in range(8):
            self.display.display_text(y, x + a, ' ')
            self.display.display_text(y + 6, x + a, ' ')
        for b in range(7):
            self.display.display_text(y + b, x, ' ')
            self.display.display_text(y + b, x + 6, ' ')
        for c in range(1, 4):
            self.display.display_text(y + 1, x + c, ' ')
        for d in range(2, 5):
            self.display.display_text(y + 5, x + d, ' ')
        self.display.refresh()
        return

    def arrow(self, y):
        for x in range(6):
            self.display.display_text(y, x, '-')
        self.display.display_text(y, 6, '>')
        self.display.refresh()
        return

    def _display(self, length):
        self.already_displayed_set = set(self.already_displayed)
        if self.name == 'dealer':
            self.display_formula(0)
        elif length == 2:
            self.display_formula(2)
        elif length == 3:
            self.display_formula(3)
        elif length == 4:
            self.display_formula(4)
        elif self.name == 'player1':
            self.display_formula(1)

    def display_formula(self, a):
        for c in self.cards:
            if not c in self.already_displayed_set:
                c._display(a, self.card_count)
                self.card_count += 1
        for b in self.cards:
            self.already_displayed.append(b)
        return

    def clear_arrow(self):
        y_list = [3, 10, 17, 24, 32]
        for y in y_list:
            for x in range(7):
                self.display.display_text(y, x, ' ')
        self.display.refresh()

    def show_player(self, length):
        if self.name == 'dealer':
            self.display.display_text_times_seven(0, self.name)
        elif length == 2:
            self.display.display_text_times_seven(2, self.name)
        elif length == 3:
            self.display.display_text_times_seven(3, self.name)
        elif length == 4:
            self.display.display_text_times_seven(4, self.name)
        elif self.name == 'player1':
            self.display.display_text_times_seven(1, self.name)

    def display_one_card(self):
        self.cards[0]._display(0, 1)
        self.card_count = 2
        self.already_displayed.append(self.cards[0])
        self.display.display_card_skeleton(0, 14)

    def play(self, deck, length):
        self.show_player(length)
        if self.name == 'dealer':
            self.arrow(3)
        elif length == 2:
            self.arrow(17)
        elif length == 3:
            self.arrow(24)
        elif length == 4:
            self.arrow(31)
        elif self.name == 'player1':
            self.arrow(10)
        while not (self.is_busted(length)) and not (self.is_blackjack(length)):
            self._display(length)
            self.display.display_text_times_seven(5, 'want to draw?')
            b = self.display.getstr(35, 14)
            draw_or_not = b.decode('utf-8')
            if draw_or_not == 'y':
                self.draw(deck, 1)
                self.display.refresh()
            if draw_or_not == 's' and self.name != 'dealer':
                self.split()
            if draw_or_not == 'n':
                break
        self.clear_arrow()
        self._display(length)
        return

    def make_card(self, card):
        self.cards = [card]

    def splittable(self):
        return (len(self.cards) == 2) and (self.get_card_value(0) == self.get_card_value(1))

    def split(self):
        if not self.splittable():
            return
        first_card, second_card = self.cards
        self.cards = [first_card]
        self.player.counter += 1
        new_hand = self.player.create_hand('splitted_hand' + str(self.player.counter), self.stdscr)
        new_hand.add_card(second_card)
        self.player.add_hand_to_play_queue(new_hand)
        self.display_and_replace(13, 7 * self.player.counter)
        new_hand.display(len(self.player.get_all_hands()))


class Player:

    def __init__(self, player_name, deck):
        self.name = player_name
        self.hands = []
        self.deck = deck
        self.queue = None
        self.counter = 0

    def get_name(self):
        return self.name

    def get_value(self, index, card):
        self.hands[index].get_value(card)

    def create_hand(self, name, stdscr):
        self.a_hand = Hand(name, self, stdscr)
        self.hands.append(self.a_hand)
        return self.a_hand

    def get_hand(self, hand_name):
        for hand in self.hands:
            return hand

    def get_all_hands(self):
        return self.hands

    def add_hand_to_play_queue(self, hand):
        self.queue.appendleft(hand)

    def play(self, deck):
        self.queue = deque(self.hands)
        while len(self.queue) > 0:
            hand = self.queue.popleft()
            hand.play(deck, len(self.hands))


class Game:

    def __init__(self, stdscr):
        self.display = Display(stdscr)
        self.deck = Deck(self.display)
        self.deck.shuffle()
        self.players = []

    def create_player(self, player_name):
        a_player = Player(player_name, self.deck)
        self.players.append(a_player)
        return a_player

    def get_player(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def initialize_player(self, player_name):
        a_player = self.create_player(player_name)
        a_player_hand = a_player.create_hand(player_name, self.display)
        a_player_hand.draw(self.deck, 2)
        return a_player, a_player_hand

    def play(self):
        dealer, dealer_hand = self.initialize_player('dealer')
        player1, player1_hand = self.initialize_player('player1')

        # display dealer's hand
        dealer_hand.display_one_card()
        player1.play(self.deck)
        dealer.play(self.deck)
        # decide result by comparing dealer hand with each player's hand
        for self.number, hand in enumerate(player1.get_all_hands()):
            self.display.display_general_text(36 + self.number * 2, f'Result for {hand.get_name()}')
            self.decide(dealer_hand, hand)
            self.display.refresh()

    def decide(self, h1, h2):
        if h1.is_blackjack() == True and h2.is_blackjack() == False:
            self.display.display_decide(self.number, f'{h1.get_player().get_name()} won')
            self.display.refresh()
            return
        if h1.is_blackjack() == False and h2.is_blackjack() == True:
            self.display.display_decide(self.number, f'{h2.get_player().get_name()} won')
            self.display.refresh()
            return
        if h1.is_blackjack() == True and h2.is_blackjack() == True:
            self.display.display_decide(self.number, 'tie')
            self.display.refresh()
            return
        if h1.is_busted() == True:
            self.display.display_decide(self.number, f'{h2.get_player().get_name()} won')
            self.display.refresh()
        elif h2.is_busted() == True:
            self.display.display_decide(self.number, f'{h1.get_player().get_name()} won')
            self.display.refresh()
        elif h1.get_score() > h2.get_score():
            self.display.display_decide(self.number, f'{h1.get_player().get_name()} won')
            self.display.refresh()
        elif h1.get_score() < h2.get_score():
            self.display.display_decide(self.number, f'{h2.get_player().get_name()} won')
            self.display.refresh()
        else:
            self.display.display_decide(self.number, 'tie')
            self.display.refresh()

def main(stdscr):
    a = Game(stdscr)
    a.play()
    sleep(5)

curses.wrapper(main)
