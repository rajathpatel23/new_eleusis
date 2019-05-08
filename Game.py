# Put your program name in place of program_name

from newEleusisPlayer import *
from random import randint
from new_eleusis import *

game_ended = False
ended_player = False

def generate_random_card():
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    return values[randint(0, len(values) - 1)] + suits[randint(0, len(suits) - 1)]


class Player(object):
    """
    'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
    """
    def __init__(self,cards):
        self.board_state = []
        self.board_state.extend(cards)
        self.hand = [generate_random_card() for _ in range(14)]

    def play(self):
        """
        Your scientist should play a card out of its given hand OR return a rule, not both.
        'game_ended' parameter is a flag that is set to True once the game ends. It is False by default
        """
        return scientist(self.board_state, self.hand, game_ended)

       #update board state
    def update_card_to_boardstate(self,card,result):

        '''
         update your board state with card based on the result
        '''
        if result == True:
            self.board_state.append((card,[]))
            return True
        else:
            self.board_state[-1][1].append(card)
            return False


class Adversary(object):
    def __init__(self):
        self.hand = [generate_random_card() for i in range(14)]

    def play(self):
        """
        'cards' is a list of three valid cards to be given by the dealer at the beginning of the game.
        Your scientist should play a card out of its given hand.
        """
        # Return a rule with a probability of 1/14
        prob_list = [i for i in range(14)]
        prob = prob_list[randint(0, 13)]
        if prob == 5:
            # Generate a random rule
            rule = ""
            conditions = ["equal", "greater"]
            properties = ["suit", "value"]
            cond = conditions[randint(0, len(properties) - 1)]
            if cond == "greater":
                prop = "value"
            else:
                prop = properties[randint(0, len(properties) - 1)]

            rule += cond + "(" + prop + "(current), " + prop + "(previous)), "
            return rule[:-2] + ")"
        else:
            return self.hand[randint(0, len(self.hand) - 1)]


# The players in the game


#rule = "iff(equal(color(previous), B), equal(color(current), R), True))"
#rule = "notf(andf(even(current),equal(suit(current),H)))"
rule = "notf(is_royal(current))"
#rule = 'iff(is_royal(current),even(current),True)'
#rule = "iff(equal(suit(current),suit(previous)),greater(value(current),value(previous)),True)"
#rule = 'iff(orf(equal(color(current),B),orf(is_royal(current),even(current))))'
cards = [("3H",[]), ("4C",[]), ("6C",[])]
tree = parse(rule)


# player and adversary

player = Player(cards)
adversary1 = Adversary()
adversary2 = Adversary()
adversary3 = Adversary()

# The three cards that adhere to the rule
"""
In each round scientist is called and you need to return a card or rule.
The cards passed to scientist are the last 3 cards played.
Use these to update your board state.
"""
print("!!Our scientist is thinking!!")
for round_num in range(0,14):
    # Each player plays a card or guesses a rule
    # Player 1 plays
    print("Playing Round:",round_num)
    player_card_rule = player.play()
    if is_card(player_card_rule):
        # checking whether card played is correct or wrong
        temp_cards= [cards[-2][0],cards[-1][0], player_card_rule]
        result = tree.evaluate(tuple(temp_cards)) #(card1,card2,card3)
        if result:
             del cards[0]
             cards.append((player_card_rule,[]))
        # player updating board state based on card played and result
        player.update_card_to_boardstate(player_card_rule, result)

    else:
        game_ended = True
        ended_player = True
        break

    # Adversary 1 plays
    ad1_card_rule = adversary1.play()
    if is_card(ad1_card_rule):
        temp_cards = [cards[-2][0], cards[-1][0], ad1_card_rule]
        result = tree.evaluate(tuple(temp_cards)) # (card1,card2,card3)
        if result:
            del cards[0]
            cards.append((ad1_card_rule,[]))
        player.update_card_to_boardstate(ad1_card_rule, result)

    else:
        game_ended = True
        ended_player = False
        break

    # Adversary 2 plays
    ad2_card_rule = adversary2.play()
    if is_card(ad2_card_rule):
        temp_cards = [cards[-2][0], cards[-1][0], ad2_card_rule]
        result = tree.evaluate(tuple(temp_cards))  # (card1,card2,card3)
        if result:
            del cards[0]
            cards.append((ad2_card_rule,[]))
        player.update_card_to_boardstate(ad2_card_rule, result)
    else:
        game_ended = True
        ended_player = False
        break

    # Adversary 3 plays
    ad3_card_rule = adversary3.play()
    if is_card(ad3_card_rule):
        temp_cards = [cards[-2][0], cards[-1][0], ad3_card_rule]
        result = tree.evaluate(tuple(temp_cards)) # (card1,card2,card3)
        if result:
            del cards[0]
            cards.append((ad3_card_rule,[]))
        player.update_card_to_boardstate(ad3_card_rule, result)
    else:
        game_ended = True
        ended_player = False
        break
game_ended = True


# Everyone has to guess a rule
rule_player = player.play()

# Check if the guessed rule is correct and print the score
score(player, rule, ended_player)