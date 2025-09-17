import numpy as np
import math
import random
import rulesets
import parse
import nextframe

VAR = {}

SAVED_FRAMES = {}

TEST_PATTERN = np.array(([0, 1, 0, 1, 0],
                         [0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0],
                         [0, 0, 1, 1, 0],
                         [0, 1, 0, 1, 0]))
                         
# subsize, offsetRowBeg, offsetRowEnd, offsetColBeg, offsetColEnd = fit_subsize(subsize, np.shape(currentFrame))
def fit_subsize(subsize, arraysize):
    if type(subsize) == str:
        divisor = int(subsize[1::])
        roundUpRow = max(0, arraysize[0]%divisor)
        roundUpCol = max(0, arraysize[1]%divisor)
        subsize = (arraysize[0]//divisor + roundUpRow, arraysize[1]//divisor + roundUpCol)
    elif type(subsize) == list and type(subsize[0]) == str:
        divisorRow = int(subsize[0][1::])
        divisorCol = int(subsize[1][1::])
        roundUpRow = max(0, arraysize[0]%divisorRow)
        roundUpCol = max(0, arraysize[1]%divisorCol)
        subsize = (arraysize[0]//divisorRow + roundUpRow, arraysize[1]//divisorCol + roundUpCol)
    else:
        subsize = (subsize[0], subsize[1])

    if arraysize[0]%subsize[0] != 0:
        modRow =   subsize[0] - arraysize[0]%subsize[0]
    else:
        modRow = 0
    modRowBeg = modRow//2
    modRowEnd = modRow - modRowBeg

    if arraysize[1]%subsize[1] != 0:
        modCol =   subsize[1] - arraysize[1]%subsize[1]
    else:
        modCol = 0
    modColBeg = modCol//2
    modColEnd = modCol - modColBeg


    

    return subsize, modRowBeg, modRowEnd, modColBeg, modColEnd

def traverse_input(inputfile, currentFrame=None, sequence=[], condDepth = "", loopDepth = 0, subarrayDepth = 0):
    
    rowSeams = []
    colSeams = []

    for item in inputfile:
        
        if currentFrame is not None:
            size = np.shape(currentFrame)

        #init vars

        runLoop = False

        runSubarray = False

        line = item.split()

        # skip empty lines

        if len(line) == 0:
            continue

        # subarray block

        if line[0] == "sub" and subarrayDepth == 0:
            subarrayDepth += 1
            if len(line) == "1":
                subsize = "/2"
            elif len(line) == "2":
                if line[1][0] == "/":
                    subsize = line[1]
                else:
                    subsize = int(line[1])
                    subsize = (subsize, subsize)
            else:
                if line[1][0] == "/":
                    subsize = line[1:3]
                else:
                    subsize = (int(line[1]), int(line[2]))
            subarrayBlock = []
            continue

        if subarrayDepth > 0:
            if line[0] == "]":
                subarrayDepth -= 1
                subarrayBlock.append(item.strip("\n"))
                if subarrayDepth == 0:
                    runSubarray = True
                else:
                    subarrayBlock.append(item.strip("\n"))
                    continue
            else:
                subarrayBlock.append(item.strip("\n"))
                continue
        
        if runSubarray:
            rowSeams = []
            colSeams = []
            subsize, modRowBeg, modRowEnd, modColBeg, modColEnd = fit_subsize(subsize, np.shape(currentFrame))
            curSize = np.shape(currentFrame)
            for rowIndex in range(1, curSize[0]+modRowBeg+1, subsize[0]):
                for colIndex in range(1, curSize[1]+modColBeg+1, subsize[1]):

                    paddedFrame = np.pad(currentFrame, ((modRowBeg+1,modRowEnd+1),(modColBeg+1,modColEnd+1)))
                    subarray = paddedFrame[rowIndex - 1:rowIndex + subsize[0] + 2, colIndex - 1:colIndex + subsize[1] + 2]
                    temp_seq, temp_curFrame = traverse_input(subarrayBlock, currentFrame=subarray, sequence=[])
                    frame_for_seq = currentFrame.copy()
                    
                    rowCurBack = max(rowIndex-1-modRowBeg, 0)
                    rowCurFront = min(rowIndex-modRowBeg+subsize[0]-1, curSize[0]-1)
                    colCurBack = max(colIndex-1-modColBeg, 0)
                    colCurFront = min(colIndex-modColBeg+subsize[1]-1, curSize[1]-1)

                    rowTempBack = 1-min(rowIndex-(modRowBeg+1), 0)
                    rowTempFront = min(curSize[0]+modRowBeg-rowIndex+1, subsize[0]+1)
                    colTempBack = 1-min(colIndex-(modColBeg+1), 0)
                    colTempFront = min(curSize[1]+modColBeg-colIndex+1, subsize[1]+1)
                    
                    if colCurBack not in (0, curSize[1]-1) and colCurBack not in colSeams:
                        colSeams.append(colCurBack)

                    if rowCurBack not in (0, curSize[0]-1) and rowCurBack not in rowSeams:
                        rowSeams.append(rowCurBack)

                    currentFrame[rowCurBack:rowCurFront, colCurBack:colCurFront] = temp_curFrame[rowTempBack:rowTempFront, colTempBack:colTempFront]
                    for frame in temp_seq:
                        frame_for_seq[rowCurBack:rowCurFront, colCurBack:colCurFront] = frame[0][rowTempBack:rowTempFront, colTempBack:colTempFront]
                        sequence.append((frame_for_seq.copy(),) + frame[1::])
            subarrayDepth = 0
            subarrayBlock = []
            subsize = 0
            currentFrame = sequence[-1][0]
            continue

        # end subarray section

        #smoothing section

        if line[0] == "smooth":
            with open("smoothing/"+line[3], "r") as smoothfile:
                smoother = smoothfile.readlines()
            width = int(line[2])
            rSeams = rowSeams.copy()
            cSeams = colSeams.copy()
            print("Smoothing with width", width, "from file " + line[3] + "...")
            for row in rSeams:
                subarray = currentFrame[row-width-1:row+width+2, ::]
                temp_seq, temp_frame = traverse_input(smoother, currentFrame=subarray, sequence=[])
                frame_for_seq = currentFrame.copy()
                currentFrame[row-width:row+width+1, ::] = temp_frame[1:-1, ::]
                for frame in temp_seq:
                    frame_for_seq[row-width:row+width+1, ::] = frame[0][1:-1, ::]
                    sequence.append((frame_for_seq.copy(),) + frame[1::])

            for col in cSeams:
                subarray = currentFrame[::, col-width-1:col+width+2]
                temp_seq, temp_frame = traverse_input(smoother, currentFrame=subarray, sequence=[])
                frame_for_seq = currentFrame.copy()
                currentFrame[::, col-width:col+width+1] = temp_frame[::, 1:-1]
                for frame in temp_seq:
                    frame_for_seq[::, col-width:col+width+1] = frame[0][::, 1:-1]
                    sequence.append((frame_for_seq.copy(),) + frame[1::])

            currentFrame = sequence[-1][0]



        #end smoothing section
        
        # loop block

        if line[0] in ("for", "while") and loopDepth == 0:
            loopDepth += 1
            loopCond = item.strip("\n").strip(":") + ":"
            loopBlock = []
            continue

        if loopDepth > 0:
            if line[0] == ")":
                loopDepth -= 1
                loopBlock.append(item.strip("\n"))
                if loopDepth == 0:
                    runLoop = True
                else:
                    loopBlock.append(item.strip("\n"))
                    continue
            if line[0] == "(":
                loopDepth += 1
            else:
                loopBlock.append(item.strip("\n"))
                continue
        
        if runLoop:
            exec(loopCond + "\n\t" + "sequence += traverse_input(loopBlock, currentFrame=currentFrame, sequence=[])[0].copy()\n\tcurrentFrame = sequence[-1][0]")
            currentFrame = sequence[-1][0]
            loopCond = ""
            loopDepth = 0
            loopBlock = []
            continue

        # end loop section

        # comments and exec

        if item[0] == "!":
            exec(item.strip("!\n"))
            continue

        if parse.skip_comments(item):
            print(item.strip("\n"))
            continue

                            # conditional block

        if line[0] == "if":
            if eval(" ".join(line[1::]).strip(":")):
                condDepth += "t" # t for true
            else:
                condDepth += "f" # f for false, "i" will also be a state for ignoring elif/else blocks
                                # "p" will be for passing through failed blocks
                                # states: t - run block; f - run next true block; i - ignore redundant (no f) elif/else body, triggered if elif/else ran into with no "f" as previous state; p - superstate of f, pass through failed if/elif body
        if line[0] == "{":
            if len(condDepth) > 0:
                if condDepth[-1] == "f":
                    condDepth = condDepth[0:-1] + "p"
                else:
                    continue
            else:
                continue

        if line[0] not in ("elif", "else", "if", "{", "}") and len(condDepth) > 0 and condDepth[-1] == "f":
            condDepth = condDepth[0:-1] # if no elif or else immediately remove from depth

        if line[0] == "elif":
            if len(condDepth) > 0:
                if condDepth[-1] == "f" and eval(" ".join(line[1::])):
                    condDepth = condDepth[0:-1] + "t"
                else:
                    condDepth = condDepth + "i"
            else:
                    condDepth = condDepth + "i"

        if line[0] == "else":
            if len(condDepth) > 0:
                if condDepth[-1] == "f":
                    condDepth = condDepth[0:-1] + "t"
                else:
                    condDepth = condDepth + "i"
            else:
                condDepth = condDepth + "i"

        if line[0] == "}" and len(condDepth) > 0:
            if condDepth[-1] in ("i", "t"):
                condDepth = condDepth[0:-1]
            elif condDepth[-1] == "p":
                condDepth = condDepth[0:-1] + "f"
        elif line[0] == "}":
            continue


        if len(condDepth) > 0:
            if condDepth[-1] in ("p", "i"):
                continue
            
                # end conditionals
        

            

        if line[0] == "size":
            if len(line) == 2:
                size = int(line[1])
                size = (size, size)
            else:
                size = (int(line[1]), int(line[2]))
            currentFrame = np.zeros(size)
            SAVED_FRAMES["default"] = None
        
        if line[0] == "addtestpattern":
            currentFrame[size[0]//2-2:size[0]//2+3, size[1]//2-2:size[1]//2+3] = TEST_PATTERN

        elif line[0] == "noisemap":
            percent = float(line[1])
            print('Adding global noise at', percent, "percent")
            currentFrame = np.maximum(currentFrame, np.maximum(np.rint(np.random.rand(size[0], size[1])-0.005*(100-percent)), np.zeros(size)))
            sequence.append((currentFrame, "noisemap", [], 0, 0))

        elif line[0] == "sinenoisemap":
            mode = line[1]
            sines = int(line[2])
            avgSize = (size[0]+size[1])/2

            if line[4] != "rand":
                amp = float(line[4])
            else:
                amp = float(1/avgSize)*128*random.uniform(-30, 30)

            if line[6] != "rand":
                period = float(line[6])
            else:
                period = float(1/avgSize)*128*random.uniform(-30, 30)

            padded = np.pad(currentFrame, (1, 1,))

            print("Making a sine noise map with", sines, "sines on mode", mode, "with amp range", amp, "and period range", period)

            if mode == "add":
                currentFrame = rulesets.Sinenoise(padded, sines, amp, period).add()
            elif mode == "subtract":
                currentFrame = rulesets.Sinenoise(padded, sines, amp, period).subtract()
            elif mode == "negintersect":
                currentFrame = rulesets.Sinenoise(padded, sines, amp, period).neg_intersect()
            elif mode == "posintersect":
                currentFrame = rulesets.Sinenoise(padded, sines, amp, period).pos_intersect()
            elif mode == "replace":
                currentFrame = rulesets.Sinenoise(padded, sines, amp, period).replace()
            sequence.append((currentFrame, "noisemap", [], 0, 0))

        elif line[0] == "save":
            if len(line) == 1:
                print("Saving current frame to default save slot")
                SAVED_FRAMES["default"] = currentFrame
            else:
                print("Saving current frame to save slot", line[1])
                SAVED_FRAMES[line[1]] = currentFrame

        
        elif line[0] == "compo":
            mode = line[1]
            if len(line) == 2 and SAVED_FRAMES["default"] is not None:
                frame = "default"
            elif len(line) > 2 and line[2] in SAVED_FRAMES.keys():
                frame = line[2]
            else:
                print("No saved frame to compo. Skipping command.")
                continue

            if mode == "add":
                print("Adding saved frame with current frame")
                currentFrame = np.minimum(SAVED_FRAMES[frame] + currentFrame, np.ones(np.shape(currentFrame)))

            elif mode == "sub":
                print("Subtracting saved frame from current frame")
                currentFrame = np.maximum(currentFrame - SAVED_FRAMES[frame], np.zeros(np.shape(currentFrame)))

            elif mode == "savesub":
                print("Subtracting current frame from saved frame")
                currentFrame = np.maximum(SAVED_FRAMES[frame] - currentFrame, np.zeros(np.shape(currentFrame)))

            elif mode == "negintersect":
                print("Removing intersections in overlay of saved and current frame.")
                currentFrame = SAVED_FRAMES[frame] + currentFrame
                currentFrame[currentFrame > 1] = 0

            elif mode == "posintersect":
                print("Keeping only intersections in overlay of saved and current frame.")
                currentFrame = SAVED_FRAMES[frame] + currentFrame
                currentFrame[currentFrame < 2] = 0
                currentFrame[currentFrame == 2] = 1
            sequence.append((currentFrame, "compo", [], 0, 0))


        elif line[0] == "clear":
            print('Clearing frame')
            currentFrame = np.zeros(np.shape(currentFrame))
            sequence.append((currentFrame, "clear", [], 0, 0))

        elif line[0] == "fill":
            print('Filling frame')
            currentFrame = np.ones(np.shape(currentFrame))
            sequence.append((currentFrame, "fill", [], 0, 0))
        
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
                sequence.append(nextframe.by_slices(currentFrame, rule, extraParam, radius, offset))
                currentFrame = sequence[-1][0]

    return sequence, currentFrame