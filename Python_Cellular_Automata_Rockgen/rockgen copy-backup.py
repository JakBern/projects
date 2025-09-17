"""
Test started 10-5-22
Attemption to make cell automata-based (& other methods) procedural rock generation
needs functions:

make_tup
parse_input
grow
decay
custom

need to pad array by 1
go over all of padded array, but only return smaller subsection
min(16, )
=====================
step size through axis is min(stepsize, nd.shape(array)[0] - lastIndex)
should make that a while loop
return only the array subarray of the right size

ok make a separate function 

need to figure out how to send back a right sized subarray to the right area of the original array
======================
(this will be nested in a function that iterates through the array)
iterating function:

def next_frame(array, rule, extraParam):

    newArray = np.zeros(np.shape(array))

    if radius <= 0:
        
        radius = 8

    if offset > radius or offset < -radius:
        offset = 0

    if radius*2 > np.shape(array)[0]:
        newArray = do_rule(array, rule)

    else:
        for rowIndex in range(np.shape(array)[0]::radius-offset):
            if np.shape(array)[0] - rowIndex > radius and rowIndex != 0:
                for colIndex in range(np.shape(array)[0]::radius-offset):
                    if np.shape(array)[1] - colIndex > radius and colIndex != 0:
                        subarray = array[rowIndex-radius:rowIndex+radius, colIndex-radius:colIndex+radius]
                        subarray = do_rule(subarray, rule)
                        newArray[rowIndex-radius:rowIndex+radius, colIndex-radius:colIndex+radius] = subarray

                    elif colIndex != 0:
                        colDiff = np.shape(array)[1] - colIndex
                        subarray = array[rowIndex-radius:rowIndex+radius, colIndex-radius:colIndex+colDiff]
                        subarray = do_rule(subarray, rule)
                        newArray[rowIndex-radius:rowIndex+radius, colIndex-radius:colIndex+colDiff] = subarray

            elif rowIndex != 0:
                rowDiff = np.shape(array)[0] - rowIndex
                for colIndex in range(np.shape(array)[0]::radius-offset):
                    if np.shape(array)[1] - colIndex > radius and colIndex != 0:
                        subarray = array[rowIndex-radius:rowIndex+rowDiff, colIndex-radius:colIndex+radius]
                        subarray = do_rule(subarray, rule)
                        newArray[rowIndex-radius:rowIndex+rowDiff, colIndex-radius:colIndex+radius] = subarray

                    elif colIndex != 0:
                        colDiff = np.shape(array)[1] - colIndex
                        subarray = array[rowIndex-radius:rowIndex+rowDiff, colIndex-radius:colIndex+colDiff]
                        subarray = do_rule(subarray, rule)
                        newArray[rowIndex-radius:rowIndex+rowDiff, colIndex-radius:colIndex+colDiff] = subarray

    return (newArray, rule)


so, the function for subarrays should go:
if radius*2 > array.len:
    subarray = 


=======================
ok, so how this should go:

ask for size of array (just keep it symmetric for now)

ask for noise percentage (.5 - (percentage * 0.005))

->loop here:

ask for neighboorhood size for regions of rulesets

ask if growth, decay, custom, or finished

run ->

sends array to function that calculates next frame
that sends a subset of the array to growth/decay/custom functions

if growth/decay, change color corresponding to the type of growth per region
each region only gets one step, but this gets repeated for the desired number of steps
have some offset between steps of region size? would be handled in the general function

g 6 o 4
grow 6 steps offset regions by up to 4

neighborhood should be odd
step size can be dissociated from neighborhood
if stepsize + last step > len

3 growth rulesets
3 decay rulesets
custom takes in different arguments

each step is output to a list holding the arrays in tuple form with a variable telling what color it should be
3 colors for growth and decay different stages

if finish is called, outputs an image with grey rocks on a green background, pulling the last frame from the frame list and giving it specific colors and saving as a png

be sure to save to the tests folder

so next on agenda is:
loop until program told to exit:
get input on size and sparsity ->
make frame from input - >
(make it 2 larger on each axis but only return the middle when appending to frames list
loop:
    get input on steps and mode ->
    loop for amount of steps:
        send input to general handler for array ->
            - need to create function for slicing array
        have that send to mode handlers ->
            - custom moore neighborhoods done
            - growth methods
            - decay methods
        return worked over subarray ->
        stitch subarray back in, next subarray ->
        finish frame, export to frame list along with mode used in tuple format, if the last mode was the same mode used change color->
    if finished:
        create gif using frame list + mode used for coloration ->
            - use frame list
        create png with natural colors




)

"""

import numpy as np
from PIL import Image
import os.path
import random
import math
import render
import rulesets
import parse


def grow(array, mode):
    if mode == "rand":
        mode = random.randint(0, 3)
    if mode == 1:
        return rulesets.growth_mode1(array)
    elif mode == 2:
        return rulesets.growth_mode2(array)
    elif mode == 3:
        return rulesets.growth_mode3(array)

def decay(array, mode):
    if mode == "rand":
        mode = random.randint(0, 3)
    if mode == 1:
        return rulesets.decay_mode1(array)
    elif mode == 2:
        return rulesets.decay_mode2(array)
    elif mode == 3:
        return rulesets.decay_mode3(array)

def custom(array, extraParam):
    if extraParam[0] == "b":
        return rulesets.custom_moore(array, extraParam[1], extraParam[3])
    else:
        return array

def do_rule(array, rule, extraParam):
    if len(rule) == 1:
        if rule == "g":
            return grow(array, "rand")
        elif rule == "d":
            return decay(array, "rand")
        elif rule == "c":
            return custom(array, extraParam)
    if rule[0] == "g" and rule[1] != "r":
        return grow(array, int(rule[1]))
    elif rule[0] == "g" and rule[1] == "r":
        return grow(array, "rand")
    elif rule[0] == "d" and rule[1] != "r":
        return decay(array, int(rule[1]))
    elif rule[0] == "d" and rule[1] == "r":
        return decay(array, "rand")
    else:
        return array


def next_frame(array, rule, extraParam, radius, offset):

    padded = np.pad(array, (1, 1,))
    newArray = np.zeros(np.shape(padded))

    if radius <= 0:
        radius = 8

    if type(offset) == str:
        offset = 1
    else:
        offset = int(offset)


    if radius*2 > np.shape(array)[0]:
        newArray = do_rule(array, rule, extraParam)

# fuck i need to rewrite this to take in a padded array one bigger on each side but only return regular size
# and i need to make sure the step size along the grid is correct

    else:
        for rowIndex in range(1+offset+radius, np.shape(padded)[0], radius+offset):
            if np.shape(padded)[0] - rowIndex > radius and rowIndex != 0:
                for colIndex in range(0, np.shape(padded)[0], radius):
                    if np.shape(padded)[1] - colIndex > radius and colIndex != 0:
                        subarray = padded[(rowIndex-radius):(rowIndex+radius+1), (colIndex-radius):(colIndex+radius+1)]
                        subarray = do_rule(subarray, rule, extraParam)
                        newArray[rowIndex-radius:rowIndex+radius+1, colIndex-radius:colIndex+radius+1] = subarray

                    elif colIndex != 1:
                        colDiff = np.shape(padded)[1] - colIndex
                        subarray = padded[rowIndex-radius:rowIndex+radius+1, colIndex-radius:colIndex+colDiff+1]
                        subarray = do_rule(subarray, rule, extraParam)
                        newArray[rowIndex-radius:rowIndex+radius+1, colIndex-radius:colIndex+colDiff+1] = subarray

            elif rowIndex != 1:
                rowDiff = np.shape(padded)[0] - rowIndex
                for colIndex in range(0, np.shape(array)[0], radius):
                    if np.shape(padded)[1] - colIndex > radius and colIndex != 0:
                        subarray = padded[rowIndex-radius:rowIndex+rowDiff+1, colIndex-radius:colIndex+radius+1]
                        subarray = do_rule(subarray, rule, extraParam)
                        newArray[rowIndex-radius:rowIndex+rowDiff+1, colIndex-radius:colIndex+radius+1] = subarray

                    elif colIndex != 1:
                        colDiff = np.shape(padded)[1] - colIndex
                        subarray = padded[rowIndex-radius:rowIndex+rowDiff+1, colIndex-radius:colIndex+colDiff+1]
                        subarray = do_rule(subarray, rule, extraParam)
                        newArray[rowIndex-radius:rowIndex+rowDiff+1, colIndex-radius:colIndex+colDiff+1] = subarray

    return (newArray[1:-1, 1:-1], rule, extraParam, radius, offset)
    
def main():
    keepGoing = True
    while keepGoing:
        fileMade = False
        sequence = []
        v = 10000
        while fileMade == False:
            if os.path.exists("tests/anim" + str(v)[1:5] + ".gif"):
                v += 1
            else:
                fileMade = True
        size = int(input("Size? "))
        percent = int(input("What percentage initial noise? "))
        currentFrame = np.maximum(np.rint(np.random.rand(size, size)-0.005*(100-percent)), np.zeros((size, size)))
        sequence.append(currentFrame)
        currentGen = True
        while currentGen:
            radius = int(input("Radius? "))
            offset = input("Offset? d for default: ")
            parsed = False
            while not parsed:
                unparsed = input("Enter ruleset. Say \"help\" for help. ")
                if unparsed.lower() == "help":
                    print("Grow, decay, or custom moore. \"g\", \"d\", or \"c\".")
                    print("Grow and decay can be \"g1-3\" or \"dr\" for random.")
                    print("Custom moore takes birth and sustain arguments like so:")
                    print("b 1 2 3 6 s 2 4")
                else:
                    rule, extraParam = parse.parse_input(unparsed)
                    parsed = True
            steps = int(input("Steps? "))
            print("Working", end ="")
            for _ in range(steps):
                sequence.append(next_frame(currentFrame, rule, extraParam, radius, offset))
                currentFrame = sequence[-1][0]
                print(".", end="")
            print("\nDone!")
            goAgain = input("Stop here? y/n: ")
            if goAgain.lower() == "y":
                currentGen = False
        print("Creating image...")
        render.make_anim(sequence, v)
        render.make_png(sequence, v)
        print("Done!")
        another = input("Another? y/n: ")
        if another == "n":
            keepGoing = False
            print("Be seeing you.")
                



            
main()
    
    
