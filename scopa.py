from random import shuffle

import tactics

colors = [tactics.denaro, " ", " ", " "]
hand_size = 3
initial_table_size = 4
no_of_players = 2


class Scopa:
    # card deck
    deck = []
    # all hands
    hands = []
    # all piles
    piles = []
    # current table
    table = []
    # how many scopas
    scopa_count = []
    # how many points
    points = []
    # what was the last hand played
    last_hand_played = -1

    def __init__(self):
        self.generate_deck()
        # self.deck = ['03 ', '06 ', '05 ', '12 ', '01 ', '12*', '05*', '03 ', '02 ', '03 ', '11*', '05 ', '04 ', '03*',
        # '01 ', '04*', '06*', '04 ', '02 ', '07 ', '13 ', '13*', '01*', '01 ', '07 ', '07*', '11 ', '07 ',
        # '02 ', '12 ', '13 ', '06 ', '12 ', '11 ', '06 ', '04 ', '13 ', '02*', '05 ', '11 ']
        self.initiate_play()

    def generate_deck(self):
        self.deck = []
        for color in colors:
            self.deck += [f'0{i}{color}' for i in range(1, 8)]
            self.deck += [f'{i}{color}' for i in range(11, 14)]
        shuffle(self.deck)

    # create table, hands, piles and scopa count
    def initiate_play(self):
        for _ in range(initial_table_size):
            self.table.append(self.deck.pop())
        for _ in range(no_of_players):
            hand = []
            self.draw_hand(hand)
            self.hands.append(hand)
            self.scopa_count.append(0)
            self.piles.append([])

    # draw cards from deck to hand, return False if hand is empty
    def draw_hand(self, hand):
        if len(self.deck) == 0:
            return False
        for _ in range(hand_size):
            hand.append(self.deck.pop())
        return True

    def print_game_results(self):
        print(f"Scopas: {self.scopa_count}")
        for s in range(no_of_players):
            pile_score = self.calculate_score(s)
            print(f"Score for hand {s}, cards {len(self.piles[s])} ({self.piles[s]}) is {pile_score}")

    def print_short_status(self):
        print("===========")
        print("Table:", self.table)
        print("Hands", self.hands)
        for pile in self.piles:
            print(f"Pile size: {len(pile)}, content: {pile}")

    def print_status(self):
        print("===========")
        print("Table:")
        print(self.table)
        print("Hands")
        print(self.hands)
        print("Deck")
        print(self.deck)
        print("Scopas")
        print(self.scopa_count)
        for pile in self.piles:
            print(f"Pile size: {len(pile)}, content: {pile}")
        print("===========\n")

    def get_no_of_cards(self):
        no_of_cards = len(self.table) + len(self.deck)
        for hand in self.hands:
            no_of_cards += len(hand)
        for pile in self.piles:
            no_of_cards += len(pile)
        if no_of_cards != 40:
            print(f"Sum is {no_of_cards} instead of 40")
            exit(1)

    def possible_takes(self, hand):
        takes_with_sum = tactics.get_takes_with_sum(self.table)
        filtered_takes = []
        for take_sum, take_cards in takes_with_sum:
            for card in hand:
                card_value = int(card[:2])
                if card_value == take_sum:
                    filtered_takes.append([card, take_cards])
        return filtered_takes

    # return sum of cards in hands and deck
    def get_no_of_cards_in_game(self):
        no_of_cards = len(self.deck)
        for hand in self.hands:
            no_of_cards += len(hand)
        return no_of_cards

    # draw hand if necessary, return True is game should be ended
    def draw_hand_if_necessary(self, hand_no):
        if len(self.hands[hand_no]) == 0:
            more_cards = self.draw_hand(self.hands[hand_no])
            return not more_cards
        return False

    # this function plays single hand with hand number
    def play_hand(self, hand_number):
        # remember the last hand played
        self.last_hand_played = hand_number
        hand = self.hands[hand_number]
        # draw hand if empty
        if len(hand) == 0:
            self.draw_hand(hand)

        best_take = self.get_best_take(hand)
        # if best possible take found
        if best_take:
            self.move_cards_from_take_to_pile(best_take, hand_number)
            # if no cards left on the table, increase scopa count
            if len(self.table) == 0 and not len(self.deck) == 0:
                self.scopa_count[hand_number] += 1
            return best_take

        else:
            # no cards can be taken, drop lowest card
            lowest_card = min(hand, key=lambda card: int(card[:2]))
            hand.remove(lowest_card)
            self.table.append(lowest_card)
            return [lowest_card, []]

    def get_best_take(self, hand):
        potential_takes = self.possible_takes(hand)
        best_take_score = -1
        best_take_index = -1
        for i, potential_take in enumerate(potential_takes):
            current_take_score = tactics.get_score_for_take(potential_take, self.table)
            if current_take_score > best_take_score:
                best_take_index = i
                best_take_score = current_take_score

        best_take = None
        # if best possible take found
        if best_take_index != -1:
            best_take = potential_takes[best_take_index]
        return best_take

    def move_cards_from_take_to_pile(self, take, hand_number):
        card_from_hand, cards_from_table = take
        pile = self.piles[hand_number]

        hand = self.hands[hand_number]
        hand.remove(card_from_hand)
        pile.append(card_from_hand)

        for card_from_table in cards_from_table:
            self.table.remove(card_from_table)
            pile.append(card_from_table)

    # this function calculates results of a pile with given number
    def calculate_score(self, pile_number):
        pile = self.piles[pile_number]
        score = 0
        # one point for settebello
        if tactics.settebello(pile):
            score += 1

        # check if any other hand has more or the same number of sevens, cards and denars
        no_of_sevens = tactics.sevens(pile)
        more_sevens = True
        no_of_cards = len(pile)
        more_cards = True
        no_of_denars = tactics.denars(pile)
        more_denars = True
        for other_pile in self.piles:
            if other_pile != pile:
                if tactics.sevens(other_pile) >= no_of_sevens:
                    more_sevens = False
                if len(other_pile) >= no_of_cards:
                    more_cards = False
                if tactics.denars(other_pile) >= no_of_denars:
                    more_denars = False

        # add one point for each
        if more_sevens:
            score += 1
        if more_cards:
            score += 1
        if more_denars:
            score += 1

        # finally add scopa points
        score += self.scopa_count[pile_number]

        return score
