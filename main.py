import sys, time, random


class Card:
    def __init__(self, number, suit, trump):
        self.number = number
        self.suit = suit  # ч б п т
        self.location = 'deck'  # first of all, cards spawn in deck
        self.power = ['6', '7', '8', '9', '10', 'в', 'д', 'к', 'т'].index(self.number)
        if self.suit == trump:
            self.power += 9

    def __str__(self):
        readable_suit = '?'
        if self.suit == 'ч':
            readable_suit = '♥'
        if self.suit == 'б':
            readable_suit = '♦'
        if self.suit == 'п':
            readable_suit = '♠'
        if self.suit == 'т':
            readable_suit = '♣'
        return self.number + readable_suit


class Player:
    def __init__(self):
        self.unknown_cards = 0
        self.definite_cards = []
        self.is_walker = False
        self.overall_cards = 0

    def take_cards(self, cards):
        # some actions
        self.overall_cards = self.unknown_cards + len(self.definite_cards)
        return 0


def get_one_card_from_string(some_string):
    if 3 < len(some_string) < 2:
        return False
    elif len(some_string) == 2:
        return some_string[0], some_string[1]
    elif len(some_string) == 3:
        return some_string[0] + some_string[1], some_string[2]


def get_many_cards_from_string(some_string):
    structured_cards = []
    for texted_card in some_string.split():
        structured_cards.append(get_one_card_from_string(texted_card))
    return structured_cards


def check_players_cards():
    global POOL
    player0 = []
    for card in POOL:
        if card.location == 'player0':
            player0.append(card)
    if len(player0) < 6:
        player0s_cards = ''
        for i in POOL:
            if i.location == 'player0':
                player0s_cards += str(i) + ' '
        my_cards_struct_local = get_many_cards_from_string(input('Какие вам добавились карты '
                                                                 '(помимо ' + player0s_cards + '): '))
        for my_card_struct_local in my_cards_struct_local:
            for pool_card_local in POOL:
                if my_card_struct_local[0] == pool_card_local.number and my_card_struct_local[1] == pool_card_local.suit:
                    pool_card_local.location = 'player0'
    return 0


print('Вас приветствует Дураковыигрыватель-2000! Ознакомьтесь, как им пользоваться:\n'
      '1) Значения карт выглядят так: 6 7 8 9 10 в д к т\n'
      '2) Масти карт выглядят так: ч б п т\n'
      '3) Целиком карты выводятся примерно так: 6ч, 9п, тт, 10б(сначала значение, потом масть)\n'
      '4) Ввод нескольких карт осуществляется через пробел\n')
PLAYERS = int(input('Кол-во игроков: '))
TRUMP = input('Козырь: ')
SUITS = ['п', 'т', 'ч', 'б']  # выносим козырь в конец, чтоб в пуле карты отсортировались сразу от слабых к сильным
SUITS.remove(TRUMP)
SUITS.append(TRUMP)
NUMBERS = ['6', '7', '8', '9', '10', 'в', 'д', 'к', 'т']
POOL = []

# заполняем пул картами всех значений и мастей
for i in range(len(SUITS)):
    for j in range(len(NUMBERS)):
        POOL.append(Card(NUMBERS[j], SUITS[i], TRUMP))

# заполняем карты ГГ
my_cards_string = get_many_cards_from_string(input('Перечисли свои карты через пробел (значение и масть): '))
for my_card_string in my_cards_string:
    for pool_card in POOL:
        if my_card_string[0] == pool_card.number and my_card_string[1] == pool_card.suit:
            pool_card.location = 'player0'

game_in_progress = True
while game_in_progress:
    action = input('1 - кинули карты на поле \n2 - карты ушли игроку \n3 - карты ушли в бито\n4 - получить '
                   'статистику\n0 - game over\nТвой выбор: ')
    if action == '0':
        game_in_progress = False
    if action == '1':  # кинули карты на поле
        action = input('Карты через пробел:')
        action = get_many_cards_from_string(action)
        for written_card in action:
            for card in POOL:
                if written_card[0] == card.number and written_card[1] == card.suit:
                    card.location = 'field'

    if action == '2':  # карты ушли некому игроку
        action = input('Кому: ')
        for card in POOL:
            if card.location == 'field':
                card.location = 'player' + action
        check_players_cards()

    if action == '3':  # карты ушли в бито
        for card in POOL:
            if card.location == 'field':
                card.location = 'lost'
        check_players_cards()

    if action == '4':  # собираем статистику
        # какие козыри остались в пуле (колода + другие игроки)
        trump_cards_left = []
        for card in POOL:
            if card.location == 'deck' and card.suit == TRUMP:
                trump_cards_left.append(card)
        if len(trump_cards_left) > 0:
            trump_cards_left = sorted(trump_cards_left, reverse=True, key=lambda x: x.power)
            print('Козыри в пуле: ', end='')
            for i in trump_cards_left:
                print(i.number, end=' ')
            print()
        # у кого какие карты
        for i in range(1, PLAYERS):
            print('Игрок' + str(i) + ': ', end='')
            for card in POOL:
                if card.location == 'player' + str(i):
                    print(card, end=' ')
            print()
