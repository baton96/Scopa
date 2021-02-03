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
leaving_single_card_factor = -3
leaving_two_cards_factor = -1


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# returns the list of all possible sums of table, along with cards that are part of this combinat
# but only if the sum is possible to be taken
def all_takes_with_sum(s):
    # store all the sublists
    ps = powerset(s)
    takes_with_sum = []

    for cset in ps:
        take_sum = sum_of_cards(cset)
        # if the sum is equal or smaller than threshold, append it -
        # in scopa sums between 8 and 10 as well as anything over 13 is not a valid take
        if (1 <= take_sum <= 7) or (11 <= take_sum <= 13):
            takes_with_sum.append([take_sum, cset])

    return takes_with_sum


# returns the sum of cards in a list
def sum_of_cards(cards):
    return sum(int(card[:2]) for card in cards)


# return true if settebello
def settebello(cards):
    return settebello_symbol in cards


# returns count of sevens
def sevens(cards):
    return sum(card[1] == "7" for card in cards)


# returns count of denars
def denars(cards):
    return sum(card[2] == denaro for card in cards)


# get the score for take
def get_score_for_take(take, table):
    score = len(take[1]*card_factor)
    if take[0] == "07D" or settebello(take[1]):
        score += settebello_factor
    if take[0][2] == denaro:
        score += denar_factor
    score += (denars(take[1]) * denar_factor)
    if take[0][1] == "7":
        score += seven_factor
    score += (sevens(take[1]) * seven_factor)
    if len(take[1]) == len(table):
        score += scopa_factor
    if len(take[1])+2 == len(table):
        score += leaving_two_cards_factor
    if len(take[1])+1 == len(table):
        score += leaving_single_card_factor

    return score