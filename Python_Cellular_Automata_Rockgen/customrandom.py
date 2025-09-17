import numpy as np
import random
import math
import os.path
import parse

class CustomRandom:

    def __init__(self, filename):

        self.rules = []

        if os.path.exists("cust/" + filename):
            ruleFile = open("cust/" + filename, "r")
        else:
            print("Specified ruleset: " + filename + " was not found.")
        
        self.weights = []

        for line in ruleFile:
            if parse.skip_comments(line):
                continue
            temp_rule = []
            weight = 1
            temp_line = line.split()
            temp_line = " ".join(temp_line[0:-1])
            mode, extraParam = parse.parse_input(temp_line)
            temp_rule.append(mode)
            temp_rule.append(extraParam)
            if line.split()[-1].split("-")[0] == "weight":
                weight = int(line.split()[-1].replace("weight-", ""))
            self.weights.append(weight)
            self.rules.append(temp_rule.copy())
           

    def get_rule(self):
        choice = random.choices(self.rules, weights=self.weights)[0]
        mode = choice[0]
        extraParam = choice[1]
        return mode, extraParam

            
            