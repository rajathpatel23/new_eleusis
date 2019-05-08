New Eleusis Player Phase -2
Team: NASH BELEIVERS

Mohit Khatwani,
Priyank Agarwal,
Sarthak Mehta,
Rajat Patel

This files provides all the instruction for running the NewEleusis Player Phase -2
Following is the description of all the files for the working of NewEleusis Player
phase -2 code

## Game.py -
-This is the main file which would need to be run for getting following output
- Confidence of the player
- Rule prediction
- Score of prediction of new eleusis player

## NewEleusisPlayer.py -
This file contains following function:

generate_random_card()
- This function provides the random generation of card for the player after everyplay
getValidCard()
- This function helps in appending a random generated card to new eleusis players hand

boardlist() -
- This cards returnt the boardlist from the board state

scientist() -
- This is actual new eleusis player function which return the rule predicted

rule_equivalence() -
- This function is used in predicting equivalent god rule by the new eleusis player

checkBoardDescription()-
- This function evaluates the board state

score -
- Function returns the score of the new eleusis player


## populateDecisionTable.py -
- The file contains following function
populate_attribute() -
- This file deals with populating the decision table called when a new card is played

## decisionTree.py -
- The file contains following class and function

Class Node() --
- Node class initializes the attributes required for decision tree node

Class decisiontree() -
- decision tree class initializes the attributes required for decision tree

populateAttributes() -
- This  function get the inputs from the populate attribuet file for every new card played

build_decision_tree() -
- The function builds and returns a decision tree

getResult() -
- getResult function returns result from the decision tree

print_tree() -
- The function return the child nodes values of the decision tree

createDecisiontree() -
- The function creates the decision tree with all the input available from the populate attribute file

getSplitAttributesWithCombination() -
- The function returns output of all possible hypothesis with max information gain

getSplitAttributes() -
- The function returns output of all possible hypothesis with max information gain

getInformationGain()-
- Function the return the count of the information gain calculated.

getRules() -
- The function return final rule value evaluated from the decision tree.



