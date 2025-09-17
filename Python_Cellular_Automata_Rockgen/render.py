import numpy as np
from PIL import Image
import os.path
import random
import math

DECAY_RAND  = (255, 0, 0)
DECAY_1     = (255, 50, 50)
DECAY_2     = (255, 100, 100)
DECAY_3     = (255, 150, 150)
GROW_RAND   = (0, 255, 0)
GROW_1      = (50, 255, 20)
GROW_2      = (100, 255, 100)
GROW_3      = (150, 255, 100)
CUSTOM_M    = (0, 0, 255)
RAND        = (210, 200, 170)
GRASS       = (123, 230, 133)
ROCK        = (213, 205, 205)

def get_color(mode):

    if mode.split("_")[0] in ("custrand", "custom random", "customrandom", "cust rand"):
        return (50, 160, 255)

    match mode:
        case "grow rand" | "growrand" | "grow random":
            return GROW_RAND
        case "grow1":
            return GROW_1
        case "grow2":
            return GROW_2
        case "grow3":
            return GROW_3
        case "decay rand" | "decayrand" | "decay random":
            return DECAY_RAND
        case "decay1":
            return DECAY_1
        case "decay2":
            return DECAY_2
        case "decay3":
            return DECAY_3
        case "custom":
            return CUSTOM_M
        case "rand" | "random":
            return RAND
        case "noisemap":
            return (255, 255, 255)
        case "noisepass":
            return (177, 177, 177)
        case "sinenoise":
            return (80, 20, 170)
        case "addblob" | "boulder" | "box" | "box2":
            return (150, 40, 190)
        case "removeblob" | "cleanup" | "fill holes":
            return (230, 120, 70)
        case "skip" | "test" | "clear" | "fill":
            return (200, 200, 200)
        case "compo":
            return (50, 150, 50)

def get_filename(sequence):
    lastmode = None
    lastParam = []
    lastradius = 0
    lastoffset = 0
    filename = []
    steps = 0
    for index, (array, mode, extraParam, radius, offset) in enumerate(sequence[1::]):
        if mode == lastmode and extraParam == lastParam and radius == lastradius and index != (len(sequence[1::]) - 1):
            steps += 1
        elif lastmode == None:
            lastmode = mode
            lastParam = extraParam
            lastradius = radius
            lastoffset = offset
            steps = 1
        elif index == (len(sequence[1::]) - 1):
            filename.append(mode)
            filename.extend(extraParam)
            filename.append("rad")
            filename.append(str(radius))
            filename.append("offset")
            filename.append(str(radius))
            filename.append("steps")
            filename.append(str(steps))
        else:
            filename.append(lastmode)
            filename.extend(lastParam)
            filename.append("rad")
            filename.append(str(lastradius))
            filename.append("offset")
            filename.append(str(lastradius))
            filename.append("steps")
            filename.append(str(steps))
            lastmode = mode
            lastParam = extraParam
            lastradius = radius
            lastoffset = offset
            steps = 0
    return filename

def make_png(sequence, fileNum, mode = "manual", inputFile = ""):
    if mode == "manual":
        filename = "-".join(get_filename(sequence))
    elif mode == "file":
        filename = inputFile
    final = Image.new("RGB", np.shape(sequence[-1][0]), GRASS)
    for index, value in np.ndenumerate(sequence[-1][0]):
            if value == 0:
                color = GRASS
            else:
                color = ROCK
            final.putpixel((index[0], index[1]), color)
    final.save("tests/" + filename + "/final" + str(fileNum)[1:5] + "-" + filename +".png", optimize=True)

def make_anim(sequence, fileNum,  mode = "manual", inputFile = ""):
    if mode == "manual":
        filename = "-".join(get_filename(sequence))
    elif mode == "file":
        filename = inputFile

    if not os.path.exists("tests/" + filename):
            os.mkdir("tests/" + filename)
    
    frames = []
    frame = Image.new("RGB", np.shape(sequence[0][0]), (0, 0, 0))
    for array, mode, extraParam, radius, offset in sequence:
        live_cell = get_color(mode)
        frame = Image.new("RGB", np.shape(array), (0, 0, 0))
        if mode == "clear":
            pass
        else:
            for index, value in np.ndenumerate(array):
                if value == 0:
                    color = (0, 0, 0)
                else:
                    color = live_cell
                frame.putpixel((index[0], index[1]), color)
        frames.append(frame)
    frames[0].save("tests/" + filename +"/anim" + str(fileNum)[1:5] + ".gif", save_all=True, append_images=frames[1:], optimize=True, duration=len(frames), loop=0)