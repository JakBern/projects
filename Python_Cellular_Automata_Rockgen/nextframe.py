import numpy as np
import rulehelpers

def by_slices(array, rule, born, sustain, radius, stride, custom_random):

    if radius is None or (radius*2 + 1) > np.shape(array)[0] or (radius*2 + 1) > np.shape(array)[1]:
        return rulehelpers.do_rule(np.pad(array, (1, 1,)), rule, born, sustain, custom_random)
    else:
        radius = abs(radius)

    if stride is None:
        stride = radius*2 + 1
    elif stride == 0:
        stride = radius*2 + 1
    else:
        stride = abs(stride)
    
    padded = np.pad(array, (radius + stride + 1, radius + stride + 1,))
    newArray = np.zeros(np.shape(padded))
    for rowIndex in range(1, np.shape(padded)[0]-(radius+1), stride):
        if rowIndex != 1:
            for colIndex in range(1, np.shape(padded)[1]-(radius+1), stride):
                if colIndex != 1:
                    subarray = padded[(rowIndex-(radius+1)):(rowIndex+radius+2), (colIndex-(radius+1)):(colIndex+radius+2)]
                    subarray = rulehelpers.do_rule(subarray, rule, born, sustain, custom_random)
                    newArray[rowIndex-radius:rowIndex+radius+1, colIndex-radius:colIndex+radius+1] = subarray

    front = radius + stride + 1
    back = -(1+stride+radius)
    return (newArray[front:back, front:back], rule, (born, sustain), radius, stride)