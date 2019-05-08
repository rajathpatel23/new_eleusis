from collections import defaultdict
import populateDecisionTable

class Node():
    def __init__(self, child = None):
        if child == None:
            self.child = []
        else:
            self.child = child
        self.path = None
        self.id = None
    def setID(self, id):
        self.id = id
    def setChildren(self, children):
        self.child = children
    def getChildren(self):
        return self.child
    def setPath(self, path):
        self.path = path


class decisionTree():
    def __init__(self):
        self.attributes = defaultdict(list)
        self.result = []
        self.root = Node()
        self.rules_list = []
        self.cardSet = []

    def populateCardSet(self, boards):
        self.cardSet = []
        for i in range(2,len(boards)):
            self.cardSet.append((boards[i-2][0], boards[i-1][0], boards[i][0]))
            self.attributes, self.result = populateDecisionTable.populate_attribute(self.attributes, boards[i][0], boards[i-1][0], boards[i-2][0],
                                                                                    self.result, True)

            if boards[i][1] != []:
                for j in range(len(boards[i][1])):
                    self.cardSet.append((boards[i-1][0], boards[i][0], boards[i][1][j]))
                    self.attributes, self.result = populateDecisionTable.populate_attribute(self.attributes,
                                                                                            boards[i][1][j],
                                                                                            boards[i][0],
                                                                                            boards[i - 1][0],
                                                                                            self.result, False)

    def populateAttributes(self, curr, prev, prev2, decision):
        self.attributes, self.result = populateDecisionTable.populate_attribute(self.attributes, curr, prev, prev2,self.result, decision)

    def build_decision_tree(self):
        self.rules_list = []
        self.createDecisiontree(self.attributes,[], self.result)


    def getResult(self):
        return self.result

    def print_tree(self,root):
        print(root.id)
        if root.id != True and root.id != False:
            children = root.getChildren()
            for child in children:
                self.print_tree(child)


    def createDecisiontree(self, attributes, node, result):
        split_attributes, minimum_information_gain = self.getSplitAttributes(attributes, result)
        if split_attributes != []:
            for split_attr in split_attributes:
                temp = []
                if node != []:
                    temp.extend(node)
                temp.append(split_attr)
                self.rules_list.append(temp)

        new_attributes = defaultdict(list)
        attributes_if = defaultdict(list)
        attr_keys = list(attributes.keys())
        for left_attr in range(0,len(attr_keys)-1):
            #for AND rule
            for right_attr in range(left_attr+1,len(attr_keys)):
                temp_result = []
                for k in range(len(attributes[attr_keys[left_attr]])):
                    if attributes[attr_keys[left_attr]][k] == True and attributes[attr_keys[right_attr]][k] == True:
                        temp_result.append(True)
                    else:
                        temp_result.append(False)
                new_attributes["andf("+str(attr_keys[left_attr]) + "," + str(attr_keys[right_attr]) + ")"].extend(temp_result)

                #Combination of OR Rule
                temp_result = []
                for k in range(len(attributes[attr_keys[left_attr]])):
                    if attributes[attr_keys[left_attr]][k] == True or attributes[attr_keys[right_attr]][k] == True:
                        temp_result.append(True)
                    else:
                        temp_result.append(False)
                new_attributes["orf(" + str(attr_keys[left_attr]) + "," + str(attr_keys[right_attr]) + ")"].extend(
                    temp_result)

                temp_result = []
                for k in range(len(attributes[attr_keys[left_attr]])):
                    if attributes[attr_keys[left_attr]][k] == True:
                        temp_result.append(attributes[attr_keys[right_attr]][k])
                    else:
                        temp_result.append(False)
                attributes_if["iff(" + str(attr_keys[left_attr]) + "," + str(attr_keys[right_attr]) + ",False)"].extend(temp_result)

                temp_result = []
                for k in range(len(attributes[attr_keys[right_attr]])):
                    if attributes[attr_keys[right_attr]][k] == True:
                        temp_result.append(attributes[attr_keys[left_attr]][k])
                    else:
                        temp_result.append(False)
                attributes_if[
                    "iff(" + str(attr_keys[right_attr]) + "," + str(attr_keys[left_attr]) + ",False)"].extend(
                    temp_result)

                temp_result = []
                for k in range(len(attributes[attr_keys[left_attr]])):
                    if attributes[attr_keys[left_attr]][k] == True:
                        temp_result.append(attributes[attr_keys[right_attr]][k])
                    else:
                        temp_result.append(True)
                attributes_if[
                    "iff(" + str(attr_keys[left_attr] + "," + str(attr_keys[right_attr]) + ",True)")].extend(
                    temp_result)

                temp_result = []
                for k in range(len(attributes[attr_keys[right_attr]])):
                    if attributes[attr_keys[right_attr]][k] == True:
                        temp_result.append(attributes[attr_keys[left_attr]][k])
                    else:
                        temp_result.append(True)
                attributes_if[
                    "iff(" + str(attr_keys[right_attr]) + "," + str(attr_keys[left_attr]) + ",True)"].extend(
                    temp_result)

        split_attributes, minimum_information_gain = self.getSplitAttributes(new_attributes, self.result)
        if split_attributes != []:
            for split_attr in split_attributes:
                temp = []
                if node != []:
                    temp.extend(node)
                temp.append(split_attr)
                self.rules_list.append(temp)

        split_attributes, minimum_information_gain = self.getSplitAttributesWithCombination(attributes_if, self.result)
        if minimum_information_gain == 0:
            for split_attr in split_attributes:
                temp = []
                if node != []:
                    temp.extend(node)
                temp.append(split_attr)
                self.rules_list.append(temp)



    def getSplitAttributesWithCombination(self, attributes, result):
        mini = 9999
        split_attrs = []
        for attr in attributes:
            information_gain = self.getInformationGain(attributes, attr, result)
            if information_gain < mini:
                mini = information_gain
        for attr in attributes:
            information_gain = self.getInformationGain(attributes, attr, result)
            if information_gain == 0:
                split_attrs.append(attr)
        return split_attrs, mini

    def getSplitAttributes(self, attributes, result):
        mini = 9999
        split_attrs = []
        for attr in attributes:
            #print("attr",attr)
            information_gain = self.getInformationGain(attributes, attr, result)
            if information_gain < mini:
                mini = information_gain
        for attr in attributes:
            information_gain = self.getInformationGain(attributes, attr, result)
            if information_gain == 0:
                if attributes[attr][0] == result[0]:
                    split_attrs.append(attr)
                else:
                    split_attrs.append("notf("+attr+")")
        #print("here in getSplit mini", mini)
        return split_attrs, mini

    def getInformationGain(self, attributes, attr, result):
        count = 0
        for i in range(len(attributes[attr])):
            if attributes[attr][i] != self.result[i]:
                count += 1
        if count == len(result):
            return 0
        return abs(count)


    def getRules(self):
        final_rules = []
        for rule in self.rules_list:
            if len(rule) == 1:
                final_rule = ""
                final_rule +=   str(rule[0])
                final_rules.append(final_rule)
            else:
                for i in range(len(rule)):
                    if len(rule[i]) != 1:
                        temp_rule = "andf("
                        for i in range(len(rule[i])):
                            temp_rule += str(rule[i])
                            if i != len(rule[i]) - 1:
                                temp_rule += ','
                            else:
                                temp_rule += ")"
                    else:
                        temp_rule = rule[i][0]
                    final_rules.append(temp_rule)
        #print(final_rules)
        return final_rules


