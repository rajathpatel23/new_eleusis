'''
This file deals with populating the decision table
called when a new card is played
'''
#structure would be a dict with key as string value of function and value as tuple of
# function and arguments

import new_eleusis


def populate_attribute(attributes, curr, prev, prev2, result, decision):

    cards = [curr, prev, prev2]
    cards_names = ["current", 'previous', 'previous2']
    function_names = [ "even", "is_royal"]
    functions = [new_eleusis.even, new_eleusis.is_royal, new_eleusis.odd]

    for card,card_name in zip(cards,cards_names):
        for func_names,func in zip(function_names,functions):
            attributes[func_names + "("+str(card_name)+")"].append(func(card))

    function_names_two = ['equal', 'less', 'greater']
    functions_two = [new_eleusis.equal, new_eleusis.less, new_eleusis.greater]

    suit = ['C','D','H','S']
    color = ['B','R']
    for i in range(len(cards)):
        for func_two, func_name_two in zip(functions_two, function_names_two):
            #for suit
            for s in suit:
                if func_name_two == 'equal':
                    attributes[func_name_two + "(suit(" + cards_names[i] + ")," + s+")"].append(func_two(new_eleusis.suit(cards[i]),s))
                elif func_name_two == 'less':
                    if s != 'C':
                        attributes[func_name_two + "(suit(" + cards_names[i] + ")," + s + ")"].append(func_two(new_eleusis.suit(cards[i]),s))
                elif func_name_two == 'greater':
                    if s != 'S':
                        attributes[func_name_two + "(suit(" + cards_names[i] + ")," + s + ")"].append(func_two(new_eleusis.suit(cards[i]), s))

            for c in color:
                if func_name_two == 'equal':
                    attributes[func_name_two + "(color(" + cards_names[i] + ")," + c + ")"].append(func_two(new_eleusis.color(cards[i]),c))


    '''
    Attributes with both arguments as functions
    '''

    for i in range(len(cards)-1):
        for j in range(i+1, len(cards)):
            for func_two,func_name_two in zip(functions_two, function_names_two):
                attributes[func_name_two + "(color(" + cards_names[i] + "),color(" + cards_names[j] + "))"].append(func_two(new_eleusis.color(cards[i]), new_eleusis.color(cards[j])))
                attributes[func_name_two + "(suit(" + cards_names[i] + "),suit(" + cards_names[j] + "))"].append(func_two(new_eleusis.suit(cards[i]),new_eleusis.suit(cards[j])))
                attributes[func_name_two + "(value(" + cards_names[i] + "),value(" + cards_names[j] + "))"].append(func_two(str(new_eleusis.value(cards[i])), str(new_eleusis.value(cards[j]))))

    result.append(decision)
    return attributes, result