"""
Test started 9-23-2022 4:37 PM

exploring numpy features + graphics.py

test started again at noon on 9-24-2022
"""

import numpy as np
#from graphics import *
from PIL import Image
import os.path
import random
import math

def next_frame(lastFrame, sizeY, sizeX, wrapAround = False):
    """
    calculates next frame based on rules
    sizeX and sizeY should be calculated once outside of this function
    and stored as variables so they don't have to be calculated over
    and over

    nearbySum calculates the number of live nearby cells

    maybe i could do this easier by making a subset
    """
    nextFrame = np.zeros((sizeY, sizeX), dtype=bool)
    for index in np.ndindex(np.shape(nextFrame)):
        # Garbage that runs like shit, reenable for something that at least works
        tempMatrix = np.zeros((3, 3)) # THIS can be rewritten later for an arbitrarily large kernel (probably a function)
        """
        runs way too slow
        if wrapAround == False:
            ind1 = 0
            for num1 in range((index[0] - 1), (index[0] + 2)):
                ind2 = 0
                for num2 in range((index[1] - 1), (index[1] + 2)):
                    if num1 >= 0 and num1 < sizeY and num2 >= 0 and num2 < sizeX:
                        tempMatrix[ind1][ind2] = lastFrame[index[0] - 1 + ind1][index[1] -1 + ind2]
                    ind2 += 1
                ind1 += 1
        """
        # just change the beginning of each range
        # wait FUCK how do i position that correctly in the kernel
        # ok i need to add it to a slice of the kernel
        # ok i don't think kernel is the right term
        # ok i just change the bounds of matrix assignment
        top = bottom = left = right = 1 # this holds if not at the extremes of the matrix
        # top case
        if index[0] == 0:
            top = 0
        # bottom case
        if index[0] == sizeY - 1:
            bottom = 0
        # left case
        if index[1] == 0:
            left = 0
        # bottom case
        if index[1] == sizeX - 1:
            right = 0
        tempMatrix[1-top:2+bottom, 1-left:2+right] = lastFrame[index[0]-top:index[0]+1+bottom, index[1]-left:index[1]+1+right]
        if wrapAround == True:
            pass
            """
            ====CONSTRUCTION ZONE=====
            i1 = 0
            for num1 in range(index[0] - 1, index[0] + 2):
                i2 = 0
                for num2 in range(index[1] - 1, index[1] + 2):
                    if num1 >= sizeY and not num2 >= sizeX:
                        tempMatrix[i1][i2] = lastFrame[0][index[1] + i2 - 1]
                    if not num1 >= sizeY and num2 >= sizeX:
                        tempMatrix[i1][i2] = lastFrame[index[0] + i2 - 1][0]
                    if num1 >= sizeY and num2 >= sizeX:
                        tempMatrix[i1][i2] = lastFrame[0][0]
                    i2 += 1
            i1 += 1
            ==============
            """
        nearbySum = np.sum(np.short(tempMatrix)) - tempMatrix[1][1] # THIS can be rewritten later as a function for malleable update rules
        self = tempMatrix[1][1]
        #if self == True and (nearbySum == 2 or nearbySum == 3):
            #nextFrame[index[0]][index[1]] = True
        #elif self == False and nearbySum == 3:
            #nextFrame[index[0]][index[1]] = True
        if self == True and nearbySum in range(9):
            nextFrame[index[0]][index[1]] = True
        elif self == False and nearbySum in {2, 4, 7}:
        #elif self == False and nearbySum in {3, 4, 7}:
            nextFrame[index[0]][index[1]] = True
        else:
            nextFrame[index[0]][index[1]] = False

        """
        interesting ruleset 1
        if self == True and (nearbySum == 3 or nearbySum == 2 or nearbySum == 4):
            nextFrame[index[0]][index[1]] = True
        elif self == False and (nearbySum == 2 or nearbySum == 3):
            nextFrame[index[0]][index[1]] = True
        
            
        interesting ruleset 2
        if self == True and (nearbySum == 1 or nearbySum == 4):
            nextFrame[index[0]][index[1]] = True
        elif self == False and (nearbySum == 3 or nearbySum == 4):
            nextFrame[index[0]][index[1]] = True
        """
        
    return nextFrame

"""
def drawFrame(window, frame):
    for index, value in np.ndenumerate(frame):
        if value == 0:
            window.plot(index[0], index[1], "black")
        elif value == 1:
            window.plot(index[0], index[1], "white")
"""


def makeAnim(matrix, steps, sizeY, sizeX, fileNum):
    frames = []
    i = 0
    while i<steps:
        frame = Image.new("RGB", (sizeY, sizeX), (0, 0, 0))
        for index, value in np.ndenumerate(matrix):
            if value == 0:
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)
                #color = (random.randint(4, 255), random.randint(4, 255), random.randint(4, 255))
                #color = (min(max(0, 255-(index[0]*2)-(index[1]*2)), 255), min(max(0, (-255+index[0]*2+index[1]*2)), 255), min(max(0, (255-abs(-index[1]*4+256))), 255))
                #color = (min(max(0, 290-(index[0]*2)-(index[1]*2)), 255), min(max(0, (255-abs(-index[0]*4+256)-(255-index[1]*2))), 255), min(max(0, (255-abs(-index[1]*4+256)-(255-index[0]*2))), 255))
                #color = (int(math.sin(i/4.0)*255), int(math.cos((index[1]+i)/2.0)*255), int(math.cos(i/3.0)*255))
                #color = (int(math.sin(i/4.0)*255), int(math.cos((index[1]+i)/2.0)*255), int(math.cos(i/3.0)*255+128-math.cos(3*i/4)*(index[0]+index[1])))
            frame.putpixel((index[0], index[1]), color)
        frames.append(frame)
        matrix = next_frame(matrix, sizeY, sizeX)
        i += 1
    frames[0].save("anim" + str(fileNum)[1:5] + ".gif", save_all=True, append_images=frames[1:], optimize=True, duration=steps, loop=0)
    print("Done")
    
def main():
    fileMade = False
    v = 10000
    while fileMade == False:
        if os.path.exists("anim" + str(v)[1:5] + ".gif"):
            v += 1
        else:
            newImg = open("anim" + str(v)[1:5] + ".gif", "x")
            fileMade = True
    newImg.close()
    sizeY = int(input("Size x? "))
    sizeX = int(input("Size y? "))
    currentFrame = np.maximum(np.rint(np.random.rand(sizeY, sizeX)-0.48), np.zeros((sizeY, sizeX))) # makes an array of specified size with random starting values of 0 or 1
    #window = GraphWin("Game of Life", sizeY, sizeX, autoflush=False)
    while True:
        makeAnim(currentFrame, int(input("How many steps? ")), sizeY, sizeX, v)
        #drawFrame(window, currentFrame)
        #update()
        #currentFrame = next_frame(currentFrame, sizeY, sizeX)

main()
    
    
