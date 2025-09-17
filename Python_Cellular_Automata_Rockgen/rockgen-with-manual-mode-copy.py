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

def custom(array, extraParam):
    if extraParam[0] == "b":
        return rulesets.custom_moore(array, extraParam)
    else:
        return array

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
    elif rule == "rand":
        return random_rule(array)
    elif rule == "test":
        return np.ones(np.shape(array[1:-1, 1:-1]))
    elif rule == "skip":
        return array[1:-1, 1:-1]
    else:
        print("Something went wrong with attempting to do a rule")
        print(rule)
        return array[1:-1, 1:-1]


def next_frame_byslices(array, rule, extraParam, radius, offset):


    if radius <= 0:
        radius = 8

    if type(offset) == str:
        offset = 0
    else:
        offset = int(offset)

    if radius*2 > np.shape(array)[0]:
        padded = np.pad(array, (1, 1,))
        newArray = do_rule(padded, rule, extraParam)
        return (newArray[1:-1, 1:-1], rule, extraParam, 0, 0)

    else:
    
        padded = np.pad(array, (radius + offset + 1, radius + offset + 1,))
        newArray = np.zeros(np.shape(padded))
        for rowIndex in range(1, np.shape(padded)[0]-(radius+offset+1), radius+offset):
            if rowIndex != 1:
                for colIndex in range(1+offset, np.shape(padded)[0]-(radius+offset+1), radius+offset):
                    if np.shape(padded)[1] - colIndex > radius and colIndex != 1:
                        subarray = padded[(rowIndex-(radius+1)):(rowIndex+radius+2), (colIndex-(radius+1)):(colIndex+radius+2)]
                        subarray = do_rule(subarray, rule, extraParam)
                        newArray[rowIndex-radius:rowIndex+radius+1, colIndex-radius:colIndex+radius+1] = subarray

    return (newArray[radius + offset + 1:-(1+offset+radius), radius + offset + 1:-(1+offset+radius)], rule, extraParam, radius, offset)

def manual_mode():
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
                sequence.append(next_frame_byslices(currentFrame, rule, extraParam, radius, offset))
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

def file_mode():

    keepGoing = True

    while keepGoing:
        
        sequence = []
        

        fileFound = False
        while not fileFound:
            filename = input("Filename? Say \"help\" for file format. ")
            if filename == "help":
                print()
            else:
                try:
                    inputfile = open("inputfiles/" + filename, "r")
                    fileFound = True
                except:
                    print("Couldn't find file.")
        del fileFound

        if not os.path.exists("tests/" + filename):
            os.mkdir("tests/" + filename)

        v = 10000
        fileMade = False
        while fileMade == False:
            if os.path.exists("tests/"+filename+"/anim" + str(v)[1:5] + ".gif"):
                v += 1
            else:
                fileMade = True
        del fileMade

        for item in inputfile:
            line = item.split()

            if len(line) == 0:
                continue

            if line[0] == "size":
                size = int(line[1])
                currentFrame = np.zeros((size, size))

            elif line[0] == "noisemap":
                percent = float(line[1])
                print('Adding global noise at', percent, "percent")
                currentFrame = np.maximum(currentFrame, np.maximum(np.rint(np.random.rand(size, size)-0.005*(100-percent)), np.zeros((size, size))))
                sequence.append((currentFrame, "noisemap", [], 0, 0))

            elif line[0] == "clear":
                print('Clearing frame')
                currentFrame = np.zeros(np.shape(currentFrame))
                sequence.append((currentFrame, "clear", [], 0, 0))
            
            elif line[0] == "wait":
                print('Adding waiting frame')
                sequence.append((currentFrame, "skip", [], 0, 0))

            elif line[0] == "do":
                steps = int(line[2])
                radius = int(line[4])
                offset = line[6]
                rule, extraParam = parse.parse_input(" ".join(line[7::]))
                ruleDesc = rule + "".join([char for char in [value for value in str(extraParam) if len(extraParam) != 0] if char not in ('[', ']', '{', '}', ',', '\'', ' ')])
                print("Doing rule " + ruleDesc, "for", steps, "steps with radius", radius, "and offset", offset)

                for _ in range(steps):
                    sequence.append(next_frame_byslices(currentFrame, rule, extraParam, radius, offset))
                    currentFrame = sequence[-1][0]

        print("Creating image...")
        render.make_anim(sequence, v, "file", filename)
        render.make_png(sequence, v, "file", filename)
        print("Done!")

        another = input("Another? y/n: ")
        if another == "n":
            keepGoing = False
            print("Be seeing you.")

def main():
    getMode = True
    while getMode:
        #try:
        mode = input("Input mode: manual (m) or file (f): ")
        if mode == "f":
            file_mode()
            getMode = False
        elif mode == "m":
            manual_mode()
            getMode = False
        else:
            print("Enter a valid mode")
       # except Exception as e:
            #print("Something went wrong:", e)
    
                



            
main()
    
    
