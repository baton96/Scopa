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

    def check_sum_of_cards(self):
        cards_sum = len(self.table) + len(self.deck)
        for hand in self.hands:
            cards_sum += len(hand)
        for pile in self.piles:
            cards_sum += len(pile)
        if cards_sum != 40:
            print(f"Sum is {cards_sum} instead of 40")
            exit(1)

    def possible_takes(self, hand):
        takes_with_sum = tactics.all_takes_with_sum(self.table)
        filtered_takes = []
        for take_sum, take_cards in takes_with_sum:
            for card in hand:
                card_value = int(card[:2])
                if card_value == take_sum:
                    filtered_takes.append([card, take_cards])
        return filtered_takes

    # return sum of cards in hands and deck
    def sum_of_all_cards_in_game(self):
        cards_sum = len(self.deck)
        for hand in self.hands:
            cards_sum += len(hand)
        return cards_sum

    # draw hand if necessary, return True is game should be ended
    def draw_hand_if_necessary(self, hand_no):
        if len(self.hands[hand_no]) == 0:
            more_cards = self.draw_hand(self.hands[hand_no])
            return not more_cards
        return False

    # this function plays single hand with hand number
    def play_hand(self, hand_number):
        # draw hand if hand is empty
        if len(self.hands[hand_number]) == 0:
            self.draw_hand(self.hands[hand_number])

        potential_takes = self.possible_takes(self.hands[hand_number])
        # find best possible take
        best_take_score = -1
        best_take_index = -1
        for i, potential_take in enumerate(potential_takes):
            # remember the last hand played
            self.last_hand_played = hand_number
            current_take_score = tactics.get_score_for_take(potential_take, self.table)
            if current_take_score > best_take_score:
                best_take_index = i
                best_take_score = current_take_score

        # if best possible take found
        if best_take_index != -1:
            # remove card from hand and add it to the pile
            card_from_hand, cards_from_table = potential_takes[best_take_index]
            self.hands[hand_number].remove(card_from_hand)
            self.piles[hand_number].append(card_from_hand)
            # remove cards from the table and add them to the pile
            for card in cards_from_table:
                self.table.remove(card)
                self.piles[hand_number].append(card)

            # if no cards left on the table, increase scopa count
            if len(self.table) == 0 and not len(self.deck) == 0:
                self.scopa_count[hand_number] += 1

            return potential_takes[best_take_index]

        else:
            # no cards can be taken, drop a card
            card_to_be_dropped = tactics.select_card_to_be_dropped(self.hands[hand_number], self.table)
            self.hands[hand_number].remove(card_to_be_dropped)
            self.table.append(card_to_be_dropped)
            return [card_to_be_dropped, []]

    # this function calculates results of a pile with given number
    def calculate_score(self, pile_number):
        score = 0
        # one point for settebello
        if tactics.settebello(self.piles[pile_number]):
            score += 1

        # check if any other hand has more or the same number of sevens, cards and denars
        no_of_sevens = tactics.sevens(self.piles[pile_number])
        more_sevens = True
        no_of_cards = len(self.piles[pile_number])
        more_cards = True
        no_of_denars = tactics.denars(self.piles[pile_number])
        more_denars = True
        for i in range(len(self.piles)):
            if i != pile_number:
                if tactics.sevens(self.piles[i]) >= no_of_sevens:
                    more_sevens = False
                if len(self.piles[i]) >= no_of_cards:
                    more_cards = False
                if tactics.denars(self.piles[i]) >= no_of_denars:
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
