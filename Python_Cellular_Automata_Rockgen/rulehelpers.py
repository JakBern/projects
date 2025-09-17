import numpy as np
from customrandom import CustomRandom
import rulesets
import random
import rulehelpers


def grow(array, mode):
    if mode == "rand":
        mode = random.randint(1, 3)
    if mode == 1:
        return rulesets.growth_mode1(array)
    elif mode == 2:
        return rulesets.growth_mode2(array)
    elif mode == 3:
        return rulesets.growth_mode3(array)

def decay(array, mode):
    if mode == "rand":
        mode = random.randint(1, 3)
    if mode == 1:
        return rulesets.decay_mode1(array)
    elif mode == 2:
        return rulesets.decay_mode2(array)
    elif mode == 3:
        return rulesets.decay_mode3(array)

def custom(array, born, sustain):
    return rulesets.custom_moore(array, born, sustain)

def random_rule(array):
    mode = random.randint(1, 7)
    if mode == 1:
        return rulesets.growth_mode1(array)
    elif mode == 2:
        return rulesets.growth_mode2(array)
    elif mode == 3:
        return rulesets.growth_mode3(array)
    elif mode == 4:
        return rulesets.decay_mode1(array)
    elif mode == 5:
        return rulesets.decay_mode2(array)
    elif mode == 6:
        return rulesets.decay_mode3(array)
    elif mode == 7:
        return do_rule(array, "skip", [])


def do_rule(array, rule, born, sustain, custom_random) -> np.array:
    match rule:
        case "grow rand" | "growrand" | "grow random":
            return grow(array, "rand")
        case "decay rand" | "decayrand" | "decay random":
            return decay(array, "rand")
        case "rand" | "random":
            return random_rule(array)
        case "custom":
            return custom(array, born, sustain)
        case "grow1":
            return grow(array, 1)
        case "grow2":
            return grow(array, 2)
        case "grow3":
            return grow(array, 3)
        case "decay1":
            return decay(array, 1)
        case "decay2":
            return decay(array, 2)
        case "grow3":
            return decay(array, 3)
        case "skip":
            return array[1:-1, 1:-1]
        case "cleanup":
            return custom(array, {}, {2, 3, 4, 5, 6, 7, 8})
        case "fill holes":
             return custom(array, {8}, set(range(9)))
        case "fill":
             return np.ones(np.shape(array[1:-1, 1:-1]))
        case "clear":
             return np.zeros(np.shape(array[1:-1, 1:-1]))
        case "boulder":
            return custom(array, {3, 4}, set(range(9)))
        case "box2":
            return custom(array, {1, 2, 3}, set(range(9)))
        case "custrand" | "custom random" | "custom rand" | "customrandom":
            rule, born, sustain, custom_random = CustomRandom(rule.split("_")[1]).get_rule()
            return do_rule(array, rule, born, sustain, custom_random)
        case _:
            print("Something went wrong with attempting to do a rule:", rule)
            return array[1:-1, 1:-1]