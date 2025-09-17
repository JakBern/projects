import numpy as np
import random
import math
from abc import ABC, abstractmethod

class Rule(ABC):

    def __init__(self, array):
        self.original = array
        self.processed = np.zeros(np.shape(array))
        self.tempArray = np.zeros((3, 3))
        self.rows = np.shape(array)[0]
        self.cols = np.shape(array)[1]
        self.padded = np.pad(array, ((1, ), (1, )), constant_values=0)

    @abstractmethod
    def run(self, rules):
        pass

class Moore(Rule):


    def run(self, rules):
        born = rules[1]
        stay = rules[3]
        for index, cell in np.ndenumerate(self.padded):
            if 0 < index[0] < (self.rows + 1) and 0 < index[1] < (self.cols + 1):
                adjRow = index[0] - 1
                adjCol = index[1] - 1
                self.tempArray = self.padded[index[0]-1:index[0]+2, index[1]-1:index[1]+2]
                nearbySum = np.sum(self.tempArray) - self.tempArray[1][1]
                selfcell = self.tempArray[1][1]
                if selfcell == 1 and nearbySum in stay:
                    self.processed[adjRow][adjCol] = 1
                elif selfcell == 0 and nearbySum in born: 
                    self.processed[adjRow][adjCol] = 1
                else:
                    self.processed[adjRow][adjCol] = 0
        return self.processed[1:-1, 1:-1]
            
def custom_moore(array, rules):
    return Moore(array).run(rules)

def growth_mode1(array):
    return Moore(array).run(("b", {2, 4, 7}, "s", set(range(9))))

def growth_mode2(array):
    return Moore(array).run(("b", {3}, "s", set(range(9))))

def growth_mode3(array):
    return Moore(array).run(("b", {1, 3, 5, 8}, "s", set(range(8))))

def decay_mode1(array):
    return Moore(array).run(("b", {}, "s", set(range(2, 6))))

def decay_mode2(array):
    return Moore(array).run(("b", {3}, "s", {2, 3}))

def decay_mode3(array):
    return Moore(array).run(("b", {}, "s", {1, 2, 3, 5, 6, 7}))