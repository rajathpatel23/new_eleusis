
import new_eleusis
import random
import decisionTree

rule_predicted = 'equal(True,False)'
totalRules = []
dt = decisionTree.decisionTree()

def generate_random_card():
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    return values[random.randint(0, len(values) - 1)] + suits[random.randint(0, len(suits) - 1)]


def getValidCard(total_cards, rule_predicted, board):
    found_card = False
    selected_card = None
    temp = []
    for card in total_cards:
        tree = new_eleusis.parse(rule_predicted)
        if tree.evaluate((board[-2][0], board[-1][0], card)):
            found_card = True
            selected_card = card
            total_cards.remove(selected_card)
            total_cards.append(generate_random_card())
            break
    #remove the selected card from our hand
    if found_card == False:
        random.shuffle(total_cards)
        selected_card = total_cards[0]
        total_cards.remove(selected_card)
        total_cards.append(generate_random_card())
        return selected_card
    return selected_card


def boardList(board):
    cards = []
    for b in board:
        cards.append(b[0])
        if b[1] != []:
            cards.extend(b[1])
    return cards

def scientist(board, total_cards, game_ended):
    global totalRules
    global rule_predicted
    if game_ended == False:
        dt.populateCardSet(board)
        dt.build_decision_tree()
        totalRules = dt.getRules()
        rule_predicted = totalRules[0]
        card_played = getValidCard(total_cards, rule_predicted, board)
        return card_played
    else:
        rule_predicted = totalRules[0]
        print("Rule Predicted by our scientist:",rule_predicted)
        return rule_predicted


## function to return the accuracy of the players rule prediction
## god_rule: The rule given by god
## player_rule: The rule predicted by the player
def rule_equivalence(rule_predicted, god_rule):
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["S", "H", "D", "C"]
    cards = []
    count = 0
    total_count = 0
    for s in suits:
        for v in values:
            cards.append(v + s)

    for prev2 in range(0, 52):
        for prev in range(0, 52):
            for curr in range(0, 52):
                total_count += 1
                rule_tree_god = new_eleusis.parse(god_rule)
                rule_tree_player = new_eleusis.parse(rule_predicted)
                if (rule_tree_god.evaluate((cards[prev2],cards[prev],cards[curr]))) == (rule_tree_player.evaluate((cards[prev2],cards[prev],cards[curr]))):
                    count += 1

    return round((count/total_count)*100, 2)

def checkBoardDescription(board, rule):
    tree = new_eleusis.parse(rule)
    for i in range(2, len(board)):
        if not tree.evaluate((board[i-2][0], board[i-1][0], board[i][0])):
            return False
        if len(board[i][1]) != 0:
            for j in range(len(board[i][1])):
                if tree.evaluate((board[i-1][0], board[i][0], board[i][1][j])):
                    return False
    return True

def score(player, god_rule, ended_player):
    global rule_predicted
    score = 0
    cards_played = 0
    for i in range(len(player.board_state)):
        cards_played += 1
        if cards_played > 20:
            score += 1
        if player.board_state[i][1] != 0:
            cards_played += 1
            if cards_played > 20:
                score += 2
    accuracy = rule_equivalence(rule_predicted,god_rule)
    print("Confidence is",accuracy)
    if int(accuracy) != 100:
        score += 15
    else:
        score -= 75
    if ended_player:
        score -= 25
    if not checkBoardDescription(player.board_state, rule_predicted):
        score += 30
    print("Score of our player is:",score)
    return score