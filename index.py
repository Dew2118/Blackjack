import curses
import random
from collections import deque
from time import sleep


class Display:
    SUIT_CHR = {'S': '\u2660', 'H': '\u2665', 'D': '\u2666', 'C': '\u2663'}

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.value = None
        self.suit = None

    def display(self, y, x, value, suit):
        self.value = value
        self.suit = suit
        self.display_card_skeleton(y * 7, x * 7)
        self.display_card_symbol(y * 7, x * 7)
        self.refresh()

    def display_card_skeleton(self, y, x, symbol='#'):
        for a in range(6):
            self.stdscr.addstr(y, x + a, symbol)
            self.stdscr.addstr(y + 6, x + a, symbol)
        for b in range(7):
            self.stdscr.addstr(y + b, x, symbol)
            self.stdscr.addstr(y + b, x + 6, symbol)
        self.refresh()

    def display_card_symbol(self, y, x):
        self.stdscr.addstr(y + 1, x + 1, self.value)
        self.stdscr.addstr(y + 1, x + 1 + len(str(self.value)), self.SUIT_CHR[self.suit])
        self.stdscr.addstr(y + 5, x + 5 - len(str(self.value)), self.value)
        self.stdscr.addstr(y + 5, x + 5, self.SUIT_CHR[self.suit])
        self.refresh()

    def clear_card_symbol(self, y, x):
        self.stdscr.addstr(y + 1, x + 1, ' ')
        self.stdscr.addstr(y + 1, x + 1 + len(str(self.value)), ' ')
        self.stdscr.addstr(y + 5, x + 5 - len(str(self.value)), ' ')
        self.stdscr.addstr(y + 5, x + 5, ' ')
        self.refresh()

    def display_decide(self, number, text, plus=0):
        self.stdscr.addstr(36 + plus, number * 18, text)
        self.refresh()

    def display_text_with_y(self, y, text):
        self.stdscr.addstr(y, 0, text)
        self.refresh()

    def display_text_times_seven(self, y, text):
        self.stdscr.addstr(y * 7, 0, text)
        self.refresh()

    def display_text(self, y, x, text, plusy=0, plusx=0):
        self.stdscr.addstr(y + plusy, x + plusx, text)
        self.refresh()

    def getstr(self, y, x):
        return self.stdscr.getstr(y, x)

    def refresh(self):
        self.stdscr.refresh()


class Card:
    SCORE = {'A': 11, 'J': 10, 'Q': 10, 'K': 10}

    def __init__(self, value, suit, display):
        self.Display = display
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

    def display(self, y, x):
        self.Display.display(y, x, self.value, self.suit)


class Deck:
    def __init__(self, display):
        value = map(str, ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
        suit = ['C', 'H', 'S', 'D']
        self.cards = [Card(v, s, display) for v in value for s in suit]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, number_of_cards):
        return [self.cards.pop(0) for c in range(number_of_cards)]


class Hand:
    def __init__(self, name, player, display):
        self.cards = []
        self.name = name
        self.player = player
        self.card_count = 1
        self.Display = display
        self.already_displayed = []
        self.already_displayed_set = None

    def test_for_player(self, text1, text2, plus):
        if self.name == 'dealer':
            self.Display.display_text_with_y(plus, text1)
            self.Display.display_text_with_y(plus + 1, text2)
        elif self.name == 'sp1':
            self.Display.display_text_with_y(plus + 14, text1)
            self.Display.display_text_with_y(plus + 14 + 1, text2)
        elif self.name == 'sp2':
            self.Display.display_text_with_y(plus + 21, text1)
            self.Display.display_text_with_y(plus + 21 + 1, text2)
        elif self.name == 'sp3':
            self.Display.display_text_with_y(plus + 28, text1)
            self.Display.display_text_with_y(plus + 28 + 1, text2)
        elif self.name == 'player1':
            self.Display.display_text_with_y(plus + 7, text1)
            self.Display.display_text_with_y(plus + 8, text2)
            self.Display.refresh()

    def get_player(self):
        return self.player

    def get_name(self):
        return self.name

    def draw(self, deck, number_of_cards):
        self.cards.extend(deck.draw(number_of_cards))

    def is_blackjack(self):
        if len(self.cards) != 2:
            return False
        scores = [c.get_score() for c in self.cards]
        if sorted(scores) == [10, 11]:
            self.test_for_player('Black', 'jack', 2)
            return True
        return False

    def get_score(self):
        """ return sum of cards' score but return -999 if busted"""
        sum_score = sum([c.get_score() for c in self.cards])
        for c in self.cards:
            if c.get_value() == 'A' and sum_score > 21:
                sum_score -= 10
        self.test_for_player(str(sum_score), '', 4)
        return sum_score if sum_score <= 21 else -999

    def get_card_value(self, card_idx):
        return self.cards[card_idx].get_value()

    def is_busted(self):
        if self.get_score() < 0:
            self.test_for_player('Busted', '', 5)
        return self.get_score() < 0

    def get_card(self, index):
        return self.cards[index]

    def add_card(self, card):
        self.cards.append(card)

    def display_and_replace(self, y):
        self.already_displayed_set = set(self.already_displayed)
        self.card_count = 2
        self.already_displayed.append(self.cards[0])
        self.Display.display_card_skeleton(y, 14, ' ')
        self.Display.clear_card_symbol(y, 14)

    def arrow(self, y):
        for x in range(6):
            self.Display.display_text(y, x, '-')
        self.Display.display_text(y, 6, '>')
        return

    def display(self):
        self.already_displayed_set = set(self.already_displayed)
        if self.name == 'dealer':
            self.display_formula(0)
        elif self.name == 'sp1':
            self.display_formula(2)
        elif self.name == 'sp2':
            self.display_formula(3)
        elif self.name == 'sp3':
            self.display_formula(4)
        elif self.name == 'player1':
            self.display_formula(1)

    def display_formula(self, a):
        for c in self.cards:
            if c not in self.already_displayed_set:
                c.display(a, self.card_count)
                self.card_count += 1
        for b in self.cards:
            self.already_displayed.append(b)
        return

    def clear_arrow(self):
        y_list = [3, 10, 17, 24, 32]
        for y in y_list:
            for x in range(7):
                self.Display.display_text(y, x, ' ')

    def show_player(self):
        self.test_for_player(self.name, '', 0)

    def display_one_card(self):
        self.cards[0].display(0, 1)
        self.card_count = 2
        self.already_displayed.append(self.cards[0])
        self.Display.display_card_skeleton(0, 14)

    def play(self, deck):
        self.player.show_all_players()
        if self.name == 'dealer':
            self.arrow(3)
        elif self.name == 'sp1':
            self.arrow(17)
        elif self.name == 'sp2':
            self.arrow(24)
        elif self.name == 'sp3':
            self.arrow(31)
        elif self.name == 'player1':
            self.arrow(10)
        while not (self.is_busted()) and not (self.is_blackjack()):
            self.display()
            self.Display.display_text_times_seven(5, 'want to draw?')
            self.get_score()
            b = self.Display.getstr(35, 14)
            draw_or_not = b.decode('utf-8')
            self.Display.display_text(35, 14, ' ')
            if draw_or_not == 'y':
                self.draw(deck, 1)
            if draw_or_not == 'd':
                self.draw(deck, 1)
                break
            if draw_or_not == 's' and self.name != 'dealer':
                self.split()
            if draw_or_not == 'n':
                break
        self.get_score()
        self.display()
        self.clear_arrow()
        self.is_blackjack()

    def make_card(self, card):
        self.cards = [card]

    def splittable(self):
        return (len(self.cards) == 2) and (self.get_card_value(0) == self.get_card_value(1))

    def split(self):
        if not self.splittable():
            return
        first_card, second_card = self.cards
        self.cards = [first_card]
        self.already_displayed.remove(second_card)
        new_hand = self.player.create_hand('sp' + str(self.player.counter), self.Display)
        self.player.counter += 1
        if self.name == 'dealer':
            self.display_and_replace(7 * 0)
        elif self.name == 'sp1':
            self.display_and_replace(7 * 2)
        elif self.name == 'sp2':
            self.display_and_replace(7 * 3)
        elif self.name == 'sp3':
            self.display_and_replace(7 * 4)
        elif self.name == 'player1':
            self.display_and_replace(7 * 1)
        new_hand.add_card(second_card)
        self.player.add_hand_to_play_queue(new_hand)
        new_hand.display()
        new_hand.show_player()

    def decide(self, other_hand):
        """return name of winner or tie if scores are equal"""
        # check blackjack cases
        if (self.is_blackjack() is True) and (other_hand.is_blackjack() is True):
            return 'Tie'
        if (self.is_blackjack() is True) and (other_hand.is_blackjack() is False):
            return f'{self.player.get_name()} won'
        if (self.is_blackjack() is False) and (other_hand.is_blackjack() is True):
            return f'{other_hand.player.get_name()} won'
        # check score cases
        if self.get_score() > other_hand.get_score():
            return f'{self.player.get_name()} won'
        elif self.get_score() < other_hand.get_score():
            return f'{other_hand.player.get_name()} won'
        else:
            return 'Tie'


class Player:
    def __init__(self, player_name, deck, game):
        self.name = player_name
        self.hands = []
        self.deck = deck
        self.queue = None
        self.game = game
        self.counter = 1
        self.a_hand = None

    def get_name(self):
        return self.name

    def get_value(self, index, card):
        self.hands[index].get_value(card)

    def create_hand(self, name, display):
        self.a_hand = Hand(name, self, display)
        self.hands.append(self.a_hand)
        return self.a_hand

    def get_hand(self):
        for hand in self.hands:
            return hand

    def get_all_hands(self):
        return self.hands

    def add_hand_to_play_queue(self, hand):
        self.queue.appendleft(hand)

    def play(self):
        self.queue = deque(self.hands)
        while len(self.queue) > 0:
            hand = self.queue.popleft()
            hand.play(self.deck)

    def show_all_players(self):
        for player in self.game.players:
            for hand in player.hands:
                hand.show_player()


class Game:
    def __init__(self, stdscr):
        self.Display = Display(stdscr)
        self.deck = Deck(self.Display)
        self.deck.shuffle()
        self.players = []

    def create_player(self, player_name):
        a_player = Player(player_name, self.deck, self)
        self.players.append(a_player)
        return a_player

    def get_player(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def initialize_player(self, player_name):
        a_player = self.create_player(player_name)
        a_player_hand = a_player.create_hand(player_name, self.Display)
        a_player_hand.draw(self.deck, 2)
        return a_player, a_player_hand

    def play(self):
        # initialize both players
        player1, player1_hand = self.initialize_player('player1')
        dealer, dealer_hand = self.initialize_player('dealer')
        dealer_hand.display_one_card()
        # play both players
        player1.play()
        dealer.play()
        # decide result by comparing dealer hand with each player's hand
        for self.number, hand in enumerate(player1.get_all_hands()):
            self.Display.display_decide(self.number, f'Result for {hand.get_name()}')
            self.decide(dealer_hand, hand)

    def decide(self, h1, h2):
        self.Display.display_decide(self.number, f'{h1.decide(h2)}', 1)


def main(stdscr):
    a = Game(stdscr)
    a.play()
    sleep(3)


curses.wrapper(main)
