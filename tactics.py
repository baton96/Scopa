from itertools import chain, combinations

denaro = "*"
settebello_symbol = "07"+denaro
lay_card_button_name = "Połóż kartę"
claim_cards_button_name = "Zbierz karty"
opponent_hand_frame_name = "Ręka przeciwnika"
actions_frame_name = "Akcje"
my_hand_frame_name = "Moja ręka"
table_frame_name = "Stolik"
this_was_scopa = "To była scopa!"

# factors
settebello_factor = 5
card_factor = 1
seven_factor = 5
denar_factor = 2
scopa_factor = 10
leaving_one_card_factor = -3
leaving_two_cards_factor = -1


def get_powerset(s):
    return chain.from_iterable(
        combinations(s, r) for r in range(len(s) + 1)
    )


# returns the list of all possible sums of table, along with cards that are part of this combinat
# but only if the sum is possible to be taken
def get_takes_with_sum(table):
    powerset = get_powerset(table)
    takes_with_sum = []

    for take_cards in powerset:
        take_sum = get_sum_of_cards(take_cards)
        # in scopa sums between 8 and 10 as well as anything over 13 is not a valid take
        if (1 <= take_sum <= 7) or (11 <= take_sum <= 13):
            takes_with_sum.append([take_sum, take_cards])
    return takes_with_sum


def get_sum_of_cards(cards):
    return sum(int(card[:2]) for card in cards)


def has_settebello(cards):
    return settebello_symbol in cards


def get_no_of_sevens(cards):
    return sum(card[1] == "7" for card in cards)


def get_no_of_denars(cards):
    return sum(card[2] == denaro for card in cards)


def get_score_for_take(take, table):
    card_from_hand, cards_from_table = take
    all_cards = list(cards_from_table) + [card_from_hand]
    score  = has_settebello(all_cards) * settebello_factor
    score += get_no_of_denars(all_cards) * denar_factor
    score += len(cards_from_table) * card_factor
    score += get_no_of_sevens(all_cards) * seven_factor

    no_cards_taken = len(cards_from_table)
    score_bonuses = {
        no_cards_taken + 0: scopa_factor,
        no_cards_taken + 1: leaving_one_card_factor,
        no_cards_taken + 2: leaving_two_cards_factor
    }
    score += score_bonuses.get(len(table), 0)

    return score