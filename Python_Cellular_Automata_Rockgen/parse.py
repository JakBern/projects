def parse_input(inpstr):
    """
    parses input string
    returns mode (growth "g", decay "d", custom "c")
    and any extra parameters as a list (with b1234s78 being sent as  ["b", {1, 2, 3, 4}, "s", {7, 8}])

    
    """
    mode = ""
    steps = 0
    lastInd = None
    extraParam = []
    tempSet = []
    for i, value in enumerate(inpstr.split()):
        if i == 0:
            mode = value

        if i > 0:

            if lastInd == None:
                lastInd = value.lower()
                extraParam.append(value)

            if lastInd in ("b", "s") and value not in ("b", "s", "a"):
                tempSet.append(int(value))

            if lastInd in ("b", "s") and value == "a":
                tempSet = (range(9))

            if lastInd == "b" and value == "s":
                lastInd = "s"
                extraParam.append(set(tempSet))
                tempSet = []
                extraParam.append(value)

    if lastInd == "s":
        extraParam.append(set(tempSet))

    return mode, extraParam

def skip_comments(line):
    return line[0] == "#"