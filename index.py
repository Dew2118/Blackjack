# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import curses
import random
from collections import deque

class Card:
  SCORE = {'A':1, 'J':10, 'Q':10,'K':10}
  SUIT_CHR = {'S':'\u2660', 'H':'\u2665', 'D':'\u2666', 'C':'\u2663'}
  def __init__(self,value,suit,stdscr):
    self.stdscr = stdscr
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

  def display(self,y,x):
    self.display_card_skeleton(y,x)
    self.display_card_symbol(y,x)

  def display_card_skeleton(self,y,x):
    for a in range(6):
      self.stdscr.addstr(y,x+a,'#')
      self.stdscr.addstr(y+6,x+a,'#')
    for b in range(7):
      self.stdscr.addstr(y+b,x,'#')
      self.stdscr.insstr(y+b,x+6,'#')
      self.stdscr.refresh()

  def display_card_symbol(self,y,x):
    self.stdscr.addstr(y+1,x+1,self.value)
    self.stdscr.addstr(y+1,x+1+len(str(self.value)),self.SUIT_CHR[self.suit])
    self.stdscr.addstr(y+5,x+4-len(str(self.value)),self.value)
    self.stdscr.addstr(y+5,x+4,self.SUIT_CHR[self.suit])
    self.stdscr.refresh()

class Deck:
  def __init__(self,stdscr):
    value = map(str,['A',2,3,4,5,6,7,8,9,10,'J','Q','K'])
    suit = ['C','H','S','D']
    self.cards = [Card('9','S',stdscr),Card('9','H',stdscr),Card('9','C',stdscr),Card('9','D',stdscr)]#Card(v,s,stdscr) for v in (value) for s in (suit)]

  def shuffle(self):
    random.shuffle(self.cards)

  def draw(self,number_of_cards):
    return [self.cards.pop(0) for i in range(number_of_cards)]


class Hand:
  def __init__(self,name,player,stdscr):
    self.cards = []
    self.name = name
    self.player = player
    self.card_count = 7
    self.stdscr = stdscr
    self.already_displayed = []

  def get_player(self):
    return self.player

  def get_name(self):
    return self.name

  def draw(self,deck,number_of_cards):
    self.cards.extend(deck.draw(number_of_cards))

  def is_blackjack(self,leght):
    if self.name == 'dealer':
      self.stdscr.addstr(2,0,'Black')
      self.stdscr.addstr(3,0,'jack')
    elif leght == 2:
      self.stdscr.addstr(15,0,'Black')
      self.stdscr.addstr(16,0,'jack')
    elif leght == 3:
      self.stdscr.addstr(22,0,'Black')
      self.stdscr.addstr(23,0,'jack')
    elif leght == 4:
      self.stdscr.addstr(29,0,'Black')
      self.stdscr.addstr(30,0,'jack')
    elif self.name == 'player1':
      self.stdscr.addstr(8,0,'Black')
      self.stdscr.addstr(9,0,'jack')
    if len(self.cards) != 2:
      return False
    scores = [c.get_score() for c in self.cards]
    if sorted(scores) == [1,10]:
      return True
    return False

  def get_score(self):
    return sum([c.get_score() for c in self.cards])

  def get_card_value(self,card_idx):
    try:
      return self.cards[card_idx].get_value()
    except Exception:
      pass

  def is_busted(self,leght):
    if (self.get_score() > 21) == True:
      if self.name == 'dealer':
        self.stdscr.addstr(5,0,'Black')
      elif leght == 2:
        self.stdscr.addstr(19,0,'Black')
      elif leght == 3:
        self.stdscr.addstr(26,0,'Black')
      elif leght == 4:
        self.stdscr.addstr(33,0,'Black')
      elif self.name == 'player1':
        self.stdscr.addstr(12,0,'Black')
    return (self.get_score() > 21)

  def get_card(self,index):
    return self.cards[index]

  def add_card(self,card):
    self.cards.append(card)

  def display_and_replace(self,x,y):
    self.already_displayed_set = set(self.already_displayed)
    self.card_count = 7
    self.already_displayed.append(self.cards[0])

    for a in range(8):
      self.stdscr.addstr(y,x+a,' ')
      self.stdscr.addstr(y+6,x+a,' ')
    for b in range(7):
      self.stdscr.addstr(y+b,x,' ')
      self.stdscr.addstr(y+b,x+6,' ')

    self.stdscr.addstr(y+1,x+1,' ')
    self.stdscr.addstr(y+1,x+2,' ')
    self.stdscr.addstr(y+1,x+3,' ')
    self.stdscr.addstr(y+5,x+2,' ')
    self.stdscr.addstr(y+5,x+3,' ')
    self.stdscr.addstr(y+5,x+4,' ')
    self.stdscr.refresh()
    return
  def arrow(self,y):
    for x in range(5):
      self.stdscr.addstr(y,x,'-')
    self.stdscr.addstr(y,6,'>')

  def display(self,leght):
    self.already_displayed_set = set(self.already_displayed)
    if self.name == 'dealer':
      self.display_formula(3)
    elif leght == 2:
      self.display_formula(17)
    elif leght == 3:
      self.display_formula(24)
    elif leght == 4:
      self.display_formula(31)
    elif self.name == 'player1':
      self.display_formula(10)

  def display_formula(self,a):
    self.arrow(a)
    for c in self.cards:
      if not c in self.already_displayed_set:
        c.display(7,self.card_count)
        self.card_count += 7
    for a in self.cards:
      self.already_displayed.append(a)
    return

  def clear_arrow(self):
    y_list = [3,17,24,31,10]
    for y in y_list:
      for x in range(6):
        self.stdscr.addstr(y,x,' ')

  def show_player(self):
      if self.name == 'dealer':
        self.stdscr.addstr(0,0,self.name)
      elif leght == 2:
        self.stdscr.addstr(7,0,self.name)
      elif leght == 3:
        self.stdscr.addstr(14,0,self.name)
      elif leght == 4:
        self.stdscr.addstr(21,0,self.name)
      elif self.name == 'player1':
        self.stdscr.addstr(28,0,self.name)

  def display_one_card(self):
    self.cards[0].display(0,7)
    self.card_count+=7
    self.already_displayed.append(self.cards[0])
    self.cards[0].display_card_skeleton(0,14)

  def play(self,deck,leght):
    while not(self.is_busted(leght)) and not(self.is_blackjack(leght)):
      self.display(leght)
      self.stdscr.addstr(35,0,'want to draw?')
      b = self.stdscr.getstr(35,14)
      draw_or_not = b.decode('utf-8')
      if draw_or_not == 'y':
        self.draw(deck,1)
        self.stdscr.refresh()
      if draw_or_not == 's':
        self.split()
      if draw_or_not == 'n':
        break
    self.clear_arrow()

    self.display(leght)
    return

  def make_card(self,card):
    self.cards = [card]

  def splittable(self):
    return (len(self.cards) == 2) and (self.get_card_value(0)==self.get_card_value(1))

  def split(self):
    if not self.splittable():
      return
    first_card, second_card = self.cards
    self.cards = [first_card]
    self.player.counter += 1
    new_hand = self.player.create_hand('splitted_hand'+str(self.player.counter),self.stdscr)
    new_hand.add_card(second_card)
    self.player.add_hand_to_play_queue(new_hand)
    self.display_and_replace(13,7*self.player.counter)
    new_hand.display(len(self.player.get_all_hands()))


class Player:

  def __init__(self,player_name,deck):
    self.name = player_name
    self.hands=[]
    self.deck = deck
    self.queue = None
    self.counter = 0

  def get_name(self):
    return self.name

  def get_value(self,index,card):
    self.hands[index].get_value(card)

  def create_hand(self,name,stdscr):
    self.a_hand = Hand(name, self, stdscr)
    self.hands.append(self.a_hand)
    return self.a_hand

  def get_hand(self,hand_name):
    for hand in self.hands:
      return hand

  def get_all_hands(self):
    return self.hands

  def add_hand_to_play_queue(self, hand):
    self.queue.appendleft(hand)

  def play(self,deck):
    self.queue = deque(self.hands)
    while len(self.queue) > 0:
      hand = self.queue.popleft()
      hand.play(deck,len(self.hands))


class Game:

  def __init__(self):
    self.stdscr = curses.initscr()
    self.deck = Deck(self.stdscr)
    self.deck.shuffle()
    self.players = []
    curses.echo()
    curses.cbreak()
    #urses.keypad(True)

  def create_player(self, player_name):
    a_player = Player(player_name,self.deck)
    self.players.append(a_player)

  def get_player(self, player_name):
    for player in self.players:
      if player.name == player_name:
        return player
    return None


  def play(self):

    # initialize dealer hand
    self.create_player('dealer')
    dealer = self.get_player('dealer')
    dealer_hand = dealer.create_hand('dealer',self.stdscr)
    dealer_hand.draw(self.deck,2)
    # initialize player1 hand
    self.create_player('player1')
    player1 = self.get_player('player1')
    player1_hand = player1.create_hand('player1',self.stdscr)
    #player1_hand.cards = [Card('A','C',self.stdscr),Card('A','D',self.stdscr)]
    player1_hand.draw(self.deck,2)

    #display dealer's hand
    dealer_hand.display_one_card()
    player1.play(self.deck)
    dealer.play(self.deck)
    # decide result by comparing dealer hand with each player's hand
    for self.number,hand in enumerate(player1.get_all_hands()):
        self.stdscr.addstr(36+self.number*2,0,f'Result for {hand.get_name()}')
        self.decide(dealer_hand, hand)
        self.stdscr.refresh()


  def decide(self, h1, h2):
    if h1.is_blackjack() == True and h2.is_blackjack() == False:
      self.stdscr.addstr(37+self.number*2,0,f'{h1.get_player().get_name()} won')
      self.stdscr.refresh()
      return
    if h1.is_blackjack() == False and h2.is_blackjack() == True:
      self.stdscr.addstr(37+self.number*2,0,f'{h2.get_player().get_name()} won')
      self.stdscr.refresh()
      return
    if h1.is_blackjack() == True and h2.is_blackjack() == True:
      self.stdscr.addstr(37+self.number*2,0,'tie')
      self.stdscr.refresh()
      return
    if h1.is_busted() == True:
      self.stdscr.addstr(37+self.number*2,0,f'{h2.get_player().get_name()} won')
      self.stdscr.refresh()
    elif h2.is_busted() == True:
      self.stdscr.addstr(37+self.number*2,0,f'{h1.get_player().get_name()} won')
      self.stdscr.refresh()
    elif h1.get_score() > h2.get_score():
      self.stdscr.addstr(37+self.number*2,0,f'{h1.get_player().get_name()} won')
      self.stdscr.refresh()
    elif h1.get_score() < h2.get_score():
      self.stdscr.addstr(37+self.number*2,0,f'{h2.get_player().get_name()} won')
      self.stdscr.refresh()
    else:
      self.stdscr.addstr(37+self.number*2,0,'tie')
      self.stdscr.refresh()


a = Game()
a.play()



