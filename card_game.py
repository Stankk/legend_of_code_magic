import sys
import math
import copy

turn = -1
LIMIT_COST = 12
LIMIT_HAND = 8
LIMIT_BOARD = 6


class Card(object):
    """
    Classe de gestion des cartes
    """
    def __init__(self, c_id, c_instance_id, c_type, c_cost, c_attack, c_defense, c_abilities):
        self.id = c_id
        self.instance_id = c_instance_id
        self.type = c_type
        self.cost = c_cost
        self.attack = c_attack
        self.defense = c_defense
        self.abilities = c_abilities

    def __repr__(self):
        return("Card number : %s\n"
               "Attack : %s\n"
               "Defense : %s\n"
               "Cost : %s\n"
               % (self.get_id(), self.get_attack(), self.get_defense(), self.get_cost()))

    def get_cost(self):
        return self.cost

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_instance_id(self):
        return self.instance_id

    def is_guard(self):
        return "G" in self.abilities

    def is_breaktrhough(self):
        return "B" in self.abilities

    def is_charge(self):
        return "C" in self.abilities


class Deck(object):
    """
    Classe de gestion de deck
    """
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def nb_of_cards_cost(self, c_cost):
        nb = 0
        for card in self.cards:
            if card.get_cost() == c_cost:
                nb += 1
        return nb

    def print_curve(self):
        msg = ""
        for i_cost in range(LIMIT_COST):
            nb_cards = sum(c.cost == i_cost + 1 for c in self.cards)
            msg += "%s : %s\n" % (i_cost+1, nb_cards)
        print_console("Curve deck :\n%s" % msg)


# ###### Utils ######
def print_console(msg):
    print(msg, file=sys.stderr)


def action_pick_card(number):
    return "PICK %s" % number


def action_attack(id1, id2=None):
    target = "%s" % id1
    if id2:
        target = "%s %s" % (id1, id2)
    return "ATTACK %s" % target


def action_summon(card_id):
    return "SUMMON %s" % card_id


def action_pass():
    return "PASS"


def board_full(board):
    return len(board) == LIMIT_BOARD


def board_empty(board):
    return len(board) == 0


# ####### DRAFT PHASE ########
def pick_card(cards, deck):
    costs = []
    tmp_costs = []
    for card in cards:
        # print_console(card)
        tmp_costs.append(card.get_cost())
        costs.append(deck.nb_of_cards_cost(card.get_cost()))

    idx = costs.index(min(costs))
    deck.add_card(cards[idx])
    print(action_pick_card(idx))


# ####### BATTLE PHASE ######
def play_my_turn(p_info, p_deck, p_board, p_hand, a_board):
    actions = ""
    if p_info["mana"] == 0 and board_empty(p_board):
        print(action_pass())
        return

    if not board_full(p_board):
        len_board = len(p_board)
        for p_card in p_hand:
            if p_info["mana"] - p_card.get_cost() >= 0 and len_board <= LIMIT_BOARD:
                p_info["mana"] -= p_card.get_cost()
                len_board += 1
                actions += action_summon(p_card.get_instance_id()) + ";"

    if len(p_board) >= 1:
        for b_card in p_board:
            target = -1
            for o_card in a_board:
                if o_card.is_guard():
                    target = o_card.get_instance_id()
                    o_card.defense -= b_card.attack
                    if o_card.get_defense() <= 0:
                        a_board.remove(o_card)
            actions += action_attack(b_card.get_instance_id(), target) + ";"

    print(actions)

# ######


# game loop
my_deck = Deck()
while True:
    # initialisation du nombre de tours
    turn += 1
    my_info = None
    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
        if i == 0:
            my_info = {"health": player_health,
                       "mana": player_mana,
                       "deck": player_deck,
                       "rune": player_rune,
                       "draw": player_draw
                       }
        else:
            o_info = {"health": player_health,
                      "mana": player_mana,
                      "deck": player_deck,
                      "rune": player_rune,
                      "draw": player_draw
                      }
    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())
    draft_cards = []
    my_board = []
    my_hand = []
    opponent_board = []
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, m_health_change, \
            o_health_change, in_card_draw = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        my_health_change = int(m_health_change)
        opponent_health_change = int(o_health_change)
        card_draw = int(in_card_draw)
        current_card = Card(card_number, instance_id, card_type, cost, attack, defense, abilities)
        # phase de draft:
        if turn < 30:
            draft_cards.append(current_card)
        if turn >= 30:
            if location == 0:
                my_hand.append(current_card)
            if location == 1:
                my_board.append(current_card)
            if location == -1:
                opponent_board.append(current_card)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    if turn < 30:
        pick_card(draft_cards, my_deck)

    if turn >= 30:
        play_my_turn(my_info, my_deck, my_board, my_hand, opponent_board)
