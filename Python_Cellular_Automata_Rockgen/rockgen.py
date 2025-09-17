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
import timeit
from customrandom import CustomRandom
import filehandler
import nextframe
import rulehelpers

def file_mode():

    keepGoing = True

    while keepGoing:
        

        fileFound = False
        while not fileFound:
            filename = input("Filename? Say \"help\" for file format. ")
            if filename == "help":
                print()
            else:
                try:
                    inputfile = open("inputfiles/" + filename.split()[0], "r")
                    fileFound = True
                    inputfile.close()
                except:
                    print("Couldn't find file.")
        del fileFound

        if len(filename.split()) > 1:
            repeat = int(filename.split()[1])
        else:
            repeat = 1
        
        filename = filename.split()[0]

        #for timing
        iteration = 0
        avgTime = 0
        #for timing

        while repeat > 0:
            #timeit part
            start = timeit.default_timer()

            inputfile = open("inputfiles/" + filename, "r")

            if not os.path.exists("tests/" + filename):
                os.mkdir("tests/" + filename)

            v = 10000
            fileMade = False
            while fileMade == False:
                if os.path.exists("tests/"+filename+"/anim" + str(v)[1:5] + ".gif") or os.path.exists("tests/"+filename+"/final" + str(v)[1:5] + "-" + filename +  ".png"):
                    v += 1
                else:
                    fileMade = True
            del fileMade

            sequence = []

            sequence = filehandler.traverse_input(inputfile, sequence=sequence)[0].copy()

            print("Creating image...")
            render.make_anim(sequence, v, "file", filename)
            render.make_png(sequence, v, "file", filename)
            print("Done!")

            filehandler.SAVED_FRAMES = {}

            #more timeit stuff
            stop = timeit.default_timer()
            execution_time = stop - start

            print("Program Executed in "+str(execution_time))

            avgTime += execution_time
            iteration += 1
            #timeit stuff end

            inputfile.close()

            repeat -= 1
        
        print("Average runtime: "+str(avgTime/iteration))

        another = input("Another? y/n: ")
        if another == "n":
            keepGoing = False
            print("Be seeing you.")

def main():
    file_mode()
    
                          
main()
    
    
