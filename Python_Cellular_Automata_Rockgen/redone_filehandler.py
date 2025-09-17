import numpy as np
import math
import random
import rulesets
import parse
import nextframe
import render
from customrandom import CustomRandom 
import typing

class RockGen:

    def __init__(self   ):
        
        self.verbose = True
        self.image_mode = True
        self.anim_mode = True
        self.row_seams = []
        self.col_seams = []
        self.sequence = []
        self.buffer_seq = []
        self.array_mode = "default"
        self.current_frame = None
        self.padded_frame = None
        self.buffer_frame = None
        self.sub_coords = []        # used both in sub array mode and smoothing mode
        self.current_subsection = 0
        self.size = 0
        self.saved_frames = {}
        self.save_frames_buffer = {}
        self.saved_frames["default"] = None

        self.full_size = ()
        self.subsize = () 
        self.mod_row_beg = 0
        self.mod_row_end = 0
        self.mod_col_beg = 0 
        self.mod_col_end = 0

    def _fit_subsize(self, subsize, arraysize):
        """hidden method to make sure the subsize of an array is correctly fit to the array"""
        if type(subsize) == str:
            divisor = int(subsize[1::])
            round_up_row = max(0, arraysize[0]%divisor)
            round_up_col = max(0, arraysize[1]%divisor)
            subsize = (arraysize[0]//divisor + round_up_row, arraysize[1]//divisor + round_up_col)
        elif type(subsize) == list and type(subsize[0]) == str:
            divisor_row = int(subsize[0][1::])
            divisor_col = int(subsize[1][1::])
            round_up_row = max(0, arraysize[0]%divisor_row)
            round_up_col = max(0, arraysize[1]%divisor_col)
            subsize = (arraysize[0]//divisor_row + round_up_row, arraysize[1]//divisor_col + round_up_col)
        else:
            subsize = (subsize[0], subsize[1])

        if arraysize[0]%subsize[0] != 0:
            mod_row =   subsize[0] - arraysize[0]%subsize[0]
        else:
            mod_row = 0
        mod_row_beg = mod_row//2
        mod_row_end = mod_row - mod_row_beg

        if arraysize[1]%subsize[1] != 0:
            mod_col =   subsize[1] - arraysize[1]%subsize[1]
        else:
            mod_col = 0
        mod_col_beg = mod_col//2
        mod_col_end = mod_col - mod_col_beg

        self.subsize = subsize 
        self.mod_row_beg = mod_row_beg
        self.mod_row_end = mod_row_end
        self.mod_col_beg = mod_col_beg
        self.mod_col_end = mod_col_end

    def _reset_buffers(self):
        """
            Hidden method to clear all buffers and assign the values held to the originals 
            called when switching modes
        """
        self.sub_coords = []
        self.saved_frames = self.save_frames_buffer
        self.save_frames_buffer = {}
        self.current_frame = self.buffer_frame
        self.buffer_frame = None
        self.padded_frame = None
        self.subsize = () 
        self.mod_row_beg = 0
        self.mod_row_end = 0
        self.mod_col_beg = 0 
        self.mod_col_end = 0
        if self.anim_mode:
            self.sequence = self.buffer_seq
            self.buffer_seq = []
  
    def _init_buffers(self):
        """
            Hidden method to assign current frame, sequence, and saved frames to their buffers
            Also empties them of current values
        """
        self.save_frames_buffer = self.saved_frames
        self.save_frames = {}
        self.buffer_frame = self.current_frame
        self.current_frame = None
        if self.anim_mode:
            self.buffer_seq = self.sequence
            self.sequence = []

    def _patch(self):
        """
            hidden method
            called when a sub-array must be patched into the greater array
            (eg, when self.next_section is called or the mode is changed)
            also patches the current sequence into the original if
            animation mode is on
        """
        row_index = self.sub_coords[self.current_subsection][0]
        col_index = self.sub_coords[self.current_subsection][1]
        row_full_back = max(row_index-1-self.mod_row_beg, 0)
        row_full_front = min(row_index-self.mod_row_beg+self.subsize[0]-1, self.full_size[0]-1)
        col_full_back = max(col_index-1-self.mod_col_beg, 0)
        col_full_front = min(col_index-self.mod_col_beg+self.subsize[1]-1, self.full_size[1]-1)

        row_sub_back = 1-min(row_index-(self.mod_row_beg+1), 0)
        row_sub_front = min(self.full_size[0]+self.mod_row_beg-row_index+1, self.subsize[0]+1)
        col_sub_back = 1-min(col_index-(self.mod_col_beg+1), 0)
        col_sub_front = min(self.full_size[1]+self.mod_col_beg-col_index+1, self.subsize[1]+1)
        
        frame_for_seq = self.buffer_frame.copy()

        self.buffer_frame[row_full_back:row_full_front, col_full_back:col_full_front] = self.current_frame[row_sub_back:row_sub_front, col_sub_back:col_sub_front]
        for frame in self.sequence:
            frame_for_seq[row_full_back:row_full_front, col_full_back:col_full_front] = frame[0][row_sub_back:row_sub_front, col_sub_back:col_sub_front]
            self.buffer_seq.append((frame_for_seq.copy(),) + frame[1::])

        # anything i need to add here?

    def _set_default_mode(self) -> None:
        """hidden method to set mode to default"""
        if self.array_mode == "default":
            pass
        elif self.array_mode == "sub":
            self.__patch()
            self._reset_buffers()
            self.sub_coords = []
            self.current_subsection = 0
            self.array_mode = "default"
        elif self.array_mode == "smooth":
            self.__patch()
            self._reset_buffers()
            self.row_seams = []
            self.col_seams = []
            self.sub_coords = []
            self.current_subsection = 0
            self.array_mode = "default"


    def _set_sub_mode(self, *args) -> None:
        """hidden method to set mode to subarray"""
        if self.array_mode == "sub":
            return
        elif self.array_mode == "smooth":
            self._reset_buffers()
            self.row_seams = []
            self.col_seams = []
            self.sub_coords = []
            self.current_subsection = 0
        
        self._init_buffers()

        self.array_mode = "sub"

        
        if len(args) == 0:
            subsize = "/2"
        elif len(args) == 1:
            if isinstance(args[0], str) and args[0][0] == "/":
                subsize = args[0]
            else:
                subsize = int(args[0])
                subsize = (subsize, subsize)
        else:
            if isinstance(args[1], str) and args[0][0] and args[0][0] == "/":
                subsize = args
            else:
                subsize = (int(args[0]), int(args[0]))
        
        self.fit_subsize(subsize, np.shape(self.current_frame))

        self.full_size = np.shape(self.current_frame)
        self.sub_coords = [
                        (row_index, col_index) 
                        for row_index in range(1, self.full_size[0]+self.mod_row_beg+1, subsize[0])
                        for col_index in range(1, self.full_size[1]+self.mod_col_beg+1, subsize[1])
                        ]
        self.padded_frame = np.pad(self.current_frame, ((self.mod_row_beg+1,self.mod_row_end+1),(self.mod_col_beg+1,self.mod_col_end+1)))
        self._update_subarray() # current subsection defaults to 0 during buffer reset
        
        self.row_seams = list({x for x, y in self.sub_coords})
        self.col_seams = list({y for x, y in self.sub_coords})

    def set_mode(self, mode: str, *args) -> None:
        """
        Changes the mode for the next lines until mode is changed again.

        Modes are:

            - "normal", "n", "default", "d"
                - reverts to using full array or does nothing.

            - "subarray" or "subsection" or "sub"
                - divides array into sections which can be worked on independently.
                - there are two methods to change to the next subsection:
                    - the next_section() method, which keeps track of the current section's index and increments
                        - next_section() loops after the last index
                    - the set_section(<section indices>) method
                - the former is recommended to be used with for loops over a range of the rockgen's .subcount()
                - changing to this mode will create a list of seams of rows and columns to be used with smoothing
                - arguments are:
                    - size of row and size of colums
                        - this can be represented as either two ints, or /<int>, or /<int1> /<int2>
                            - the second and third type will divide the array into equal subsections.
                              using one argument will divide into squares.
                              using two arguments will divide into rectangles of size
                              num_rows//<int1>, num_cols//<int2>
                        - defaults to /2 for both rows and columns

            - "smooth" or "smoothing"
                - will not work if the array hasn't been previously put into subarray mode
                - operates on slices where the subsections were made
                - arguments
                    - width (from center of seam) that is considered as subsection.
                      creates a subsection centered at the seam going all the way across the image
                      with n pixels on each side
                - can switch to the next seam through the next_section() method or set_section.
                    - recommended to iterate through the .subcount() (which is changed to refer to the total amount of seams)
        """

        match mode:

            case "default" | "d" | "normal" | "n":
                self._set_default_mode()
                if self.verbose:
                    print("Switched to default mode.")


            case "sub" | "subsection" | "subarray":
                self._set_sub_mode(args)
                if self.verbose:
                    print("Switched to subarray mode.")

            case "smoothing" | "smooth":
                pass
            
            case _:
                if self.verbose:
                    print("Error: Attempted mode switch not processed")
                pass


    def subcount(self):
        """
            returns the amount of subarrays the current array is divided into
            only valid for sub array and smoothing mode
            returns 0 in default mode  
        """
        return len(self.sub_coords)

    def _update_subarray(self):
        """
            Updates the sub array based on the current subsection value
            patch should be called beforehand except when first switching modes
            """
        if self.array_mode == "sub":
            row_index = self.sub_coords[self.current_subsection][0]
            col_index = self.sub_coords[self.current_subsection][1]
            self.current_frame = self.padded_frame[row_index - 1:row_index + self.subsize[0] + 2, col_index - 1:col_index + self.subsize[1] + 2]
            if self.anim_mode:
                self.sequence = []
        elif self.array_mode == "smooth":
            pass
            if self.anim_mode:
                self.sequence = []
            
        else:
            return

    
    def next_section(self):
        """
            moves sequentially to the next subsection according to the sub_coords
            patches in the current changes to the subarray first
            columns are incremented first, then rows.
        """
        self._patch()
        self.current_subsection = (self.current_subsection + 1) % (self.subcount())
        if self.verbose:
            print("Switching from subsection", self.current_subsection - 1, "to subsection", self.current_subsection)
        self._update_subarray()

    def prev_section(self):
        """
            moves sequentially to the previous subsection according to the sub_coords
            columns are decremented first, then rows.
        """
        self._patch()
        self.current_subsection = (self.current_subsection - 1) % (self.subcount())
        if self.verbose:
            print("Switching from subsection", self.current_subsection - 1, "to subsection", self.current_subsection)
        self._update_subarray()

    def set_section(self, index: int|None=None, indices: tuple|None=None) -> None:
        """
            sets the sub array section based on either the subsection number in the current_subsection ordering
            or by the indices of the subsection as a tuple
            failure to provide proper indices will lead to the subsection not being changed
            subsection numbers outside of the possible range will be modulo'd to fit
            too many arguments defaults to nothing
        """
        if self.array_mode == "default":
            if self.verbose:
                print("Attempted to set section in default mode. Skipping command.")
            return

        if index is None and indices is None:
            if self.verbose:
                print("No arguments given. Skipping set_section command.")
                return
        elif index is not None and indices is not None:
            if self.verbose:
                print("Too many arguments given. Skipping set_section command.")
                return
        elif index is None:
            if indices in self.sub_coords: # case where it works
                self._patch()

                if self.verbose:
                    print(
                        "Switching from subsection", self.current_subsection, 
                        "with indices", self._get_indices(self.current_subsection), end=""
                            )
                self.current_subsection = self._match_indices(indices)
                if self.verbose:
                    print(
                        " to subsection", self.current_subsection, 
                        "with indices", indices
                            )
                self._update_subarray()

            elif not isinstance(indices, tuple): # case where indices are incorrectly given
                if self.verbose:
                    print("Incorrect argument type for indices. Skipping set_section command")
                return
           
            else:   # case where indices are not in sub_coords list
                if self.verbose:
                    print("Indices do not define subsection in a valid way. Skipping set_section command")
                return

        elif indices is None:
            if isinstance(index, int): # case where it works
                self._patch()
                if self.verbose:
                    print(
                        "Switching from subsection", self.current_subsection, 
                        "with indices", self._get_indices(self.current_subsection), end=""
                            )
                self.current_subsection = index % len(self.sub_coords)
                if self.verbose:
                    print(
                        " to subsection", self.current_subsection, 
                        "with indices", self._get_indices(self.current_subsection)
                            )
                self._update_subarray()
            else: # case where it doesn't
                if self.verbose:
                    print("Incorrect argument type for index. Skipping set_section command")
                return

    def _match_indices(self, indices: tuple) -> int:
        """
            returns index where the specified indices occur in the sub array section
            should not be called if they do not exist
        """
        index = [index for index, coords in enumerate(self.sub_coords) if coords == indices]
        return index[0]

    def _get_indices(self, index: int) -> tuple:
        """
            returns indices of index in sub array section
            should not be called index does not exist
        """
        indices = self.sub_coords[index]
        return indices
    
    if runSubarray:
        # this section can be the intialization into sub array mode
        full_size = np.shape(self.current_frame)
        for row_index in range(1, full_size[0]+self.mod_row_beg+1, subsize[0]): #these will be made into the coords
            for col_index in range(1, full_size[1]+self.mod_col_beg+1, subsize[1]):  
                # this will be part of initialization
                self.padded_frame = np.pad(self.current_frame, ((self.mod_row_beg+1,self.mod_row_end+1),(self.mod_col_beg+1,self.mod_col_end+1)))
                subarray = paddedFrame[row_index - 1:row_index + subsize[0] + 2, col_index - 1:col_index + subsize[1] + 2]
                # this section can be cut out
                temp_seq, temp_curFrame = traverse_input(subarrayBlock, self.current_frame=subarray, self.sequence=[])
                frame_for_seq = self.current_frame.copy()
                # this section will be patch
                rowCurBack = max(row_index-1-self.mod_row_beg, 0)
                rowCurFront = min(row_index-self.mod_row_beg+self.subsize[0]-1, self.full_size[0]-1)
                colCurBack = max(col_index-1-self.mod_col_beg, 0)
                colCurFront = min(col_index-self.mod_col_beg+self.subsize[1]-1, self.full_size[1]-1)

                rowTempBack = 1-min(row_index-(self.mod_row_beg+1), 0)
                rowTempFront = min(full_size[0]+self.mod_row_beg-row_index+1, self.subsize[0]+1)
                colTempBack = 1-min(col_index-(self.mod_col_beg+1), 0)
                colTempFront = min(full_size[1]+self.mod_col_beg-col_index+1, self.subsize[1]+1)
                

                self.current_frame[rowCurBack:rowCurFront, colCurBack:colCurFront] = temp_curFrame[rowTempBack:rowTempFront, colTempBack:colTempFront]
                for frame in temp_seq:
                    frame_for_seq[rowCurBack:rowCurFront, colCurBack:colCurFront] = frame[0][rowTempBack:rowTempFront, colTempBack:colTempFront]
                    self.sequence.append((frame_for_seq.copy(),) + frame[1::])
        subarrayDepth = 0
        subarrayBlock = []
        subsize = 0
        self.current_frame = self.sequence[-1][0]
        continue

    # end subarray section

    #smoothing section

    def smooth(self):
        with open("smoothing/"+line[3], "r") as smoothfile:
            smoother = smoothfile.readlines()
        width = int(line[2])
        rSeams = rowSeams.copy()
        cSeams = colSeams.copy()
        print("Smoothing with width", width, "from file " + line[3] + "...")
        for row in rSeams:
            subarray = self.current_frame[row-width-1:row+width+2, ::]
            temp_seq, temp_frame = traverse_input(smoother, self.current_frame=subarray, self.sequence=[])
            frame_for_seq = self.current_frame.copy()
            self.current_frame[row-width:row+width+1, ::] = temp_frame[1:-1, ::]
            for frame in temp_seq:
                frame_for_seq[row-width:row+width+1, ::] = frame[0][1:-1, ::]
                self.sequence.append((frame_for_seq.copy(),) + frame[1::])

        for col in cSeams:
            subarray = self.current_frame[::, col-width-1:col+width+2]
            temp_seq, temp_frame = traverse_input(smoother, self.current_frame=subarray, self.sequence=[])
            frame_for_seq = self.current_frame.copy()
            self.current_frame[::, col-width:col+width+1] = temp_frame[::, 1:-1]
            for frame in temp_seq:
                frame_for_seq[::, col-width:col+width+1] = frame[0][::, 1:-1]
                self.sequence.append((frame_for_seq.copy(),) + frame[1::])

        self.current_frame = self.sequence[-1][0]



        #end smoothing section


            

    def set_size(self, size_x: int, size_y: int=0):
        if size_y == 0:
            size_y = size_x
        self.size = (size_x, size_y)
        self.current_frame = np.zeros(size)

    def noisemap(self, percent: float):
        """
        Adds noise of a given percentage over the entire frame.
        Ex: 1.5 => 1.5% of normal noise over the entire map
        """
        if self.verbose:
            print('Adding global noise at', percent, "percent")
        self.current_frame = np.maximum(self.current_frame, np.maximum(np.rint(np.random.rand(size[0], size[1])-0.005*(100-percent)), np.zeros(size)))
        if self.image_mode:
            self.sequence.append((self.current_frame, "noisemap", [], 0, 0))

    def sinenoisemap(self, method: str, sines: int, period: float=30, amp: float=30, rand: bool=True):
        """
            Creates blobby noise over the image using sine functions which vary with the row and column values
            If the sum of a cell's sine functions is >= 1, it is turned on
            3-6 is the reccommended minimum amount of sines to use.
            Each sine from 1-6 takes in array inputs differently. After that, it repeats.
            Each sine has a randomly assigned period and amplitude.

            ==Sines==
            The amount of sines to use. Be aware: the period and amplitude internally
            are damped by the amount of sines divided by 2.

            ==Period==
            The absolute value bound within which the period of every sine function is randomly determined.
            30 by default.

            ==Amp==
            The absolute value bound within which the amplitude of every sine function is determined.
            30 by default.

            ==Rand==
            Boolean value. If true, assigns a random bound below or at the user given bounds
            for period and amplitude multiplied by 1 divided by the dimension size for the array
            multiplied by 128. 

            ------------------------------------------------
            Methods are:
                add - adds sine noise to current frame
                sub - subtracts sine noise from current frame
                replace - completely replaces current frame with sine noise
                negintersect - adds current frame and sine noise but removes any intersections
                posintersect - removes everything except intersections of sine noise and current frame
        """
        avgSize = (np.size(self.current_frame))/2

        if not rand:
            pass
        else:
            amp = float(1/avgSize)*128*random.uniform(-amp, amp)

        if not rand:
            pass
        else:
            period = float(1/avgSize)*128*random.uniform(-period, period)

        padded = np.pad(self.current_frame, (1, 1,))
        if self.verbose:
            print("Making a sine noise map with", sines, "sines on mode", method, "with amp range", amp, "and period range", period)

        if method == "add":
            self.current_frame = rulesets.Sinenoise(padded, sines, amp, period).add()
        elif method == "subtract":
            self.current_frame = rulesets.Sinenoise(padded, sines, amp, period).subtract()
        elif method == "negintersect":
            self.current_frame = rulesets.Sinenoise(padded, sines, amp, period).neg_intersect()
        elif method == "posintersect":
            self.current_frame = rulesets.Sinenoise(padded, sines, amp, period).pos_intersect()
        elif method == "replace":
            self.current_frame = rulesets.Sinenoise(padded, sines, amp, period).replace()
        if self.image_mode:
            self.sequence.append((self.current_frame, "noisemap", [], 0, 0))

    def save(self, save_name: str = "default"):
        """Saves the current frame to a dictionary with a user-given key, or to "default" slot"""
        if self.verbose:
            print("Saving current frame to save slot", line[1])
        self.saved_frames[line[1]] = self.current_frame

    
    def compo(self, method: str, saved_frame: str = "default"):
        """
            Short for "composite"
            Combines the current frame with a saved frame from the saved_frames dictionary
            using a user-specified method.
            ------------------------------------------------
            Methods are:
                add - adds current frame to saved frame
                sub - subtracts saved frame from current frame
                savesub - subtracts current frame from saved frame
                negintersect - adds current and saved frame but removes any intersections
                posintersect - removes everything except intersections of saved frame and current frame
        """
        if saved_frame in self.saved_frames.keys():
            pass
        else:
            if self.verbose:
                print("Error: Frame key not in dict")
            return

        if method == "add":
            if self.verbose:
                print("Adding saved frame with current frame")
            self.current_frame = np.minimum(self.saved_frames[saved_frame] + self.current_frame, np.ones(np.shape(self.current_frame)))

        elif method == "sub":
            if self.verbose:
                print("Subtracting saved frame from current frame")
            self.current_frame = np.maximum(self.current_frame - self.saved_frames[saved_frame], np.zeros(np.shape(self.current_frame)))

        elif method == "savesub":
            if self.verbose:
                print("Subtracting current frame from saved frame")
            self.current_frame = np.maximum(self.saved_frames[saved_frame] - self.current_frame, np.zeros(np.shape(self.current_frame)))

        elif method == "negintersect":
            if self.verbose:
                print("Removing intersections in overlay of saved and current frame.")
            self.current_frame = self.saved_frames[saved_frame] + self.current_frame
            self.current_frame[self.current_frame > 1] = 0

        elif method == "posintersect":
            if self.verbose:
                print("Keeping only intersections in overlay of saved and current frame.")
            self.current_frame = self.saved_frames[saved_frame] + self.current_frame
            self.current_frame[self.current_frame < 2] = 0
            self.current_frame[self.current_frame == 2] = 1

        if self.image_mode:
            self.sequence.append((self.current_frame, "compo", [], 0, 0))


    def clear(self):
        """clears the entire given frame"""
        if self.verbose:
            print('Clearing frame')
        self.current_frame = np.zeros(np.shape(self.current_frame))
        if self.image_mode:
            self.sequence.append((self.current_frame, "clear", [], 0, 0))

    def fill(self) -> None:
        """Fills the entire given frame"""
        if self.verbose:
            print('Filling frame')
        self.current_frame = np.ones(np.shape(self.current_frame))
        if self.image_mode:
            self.sequence.append((self.current_frame, "fill", [], 0, 0))
    
    def wait(self) -> None:
        """Waits a frame and appends to self.sequence. Only useful when making process images."""
        if self.verbose:
            print('Adding waiting frame')
        if self.image_mode:
            self.sequence.append((self.current_frame, "skip", [], 0, 0))

    def do_rule(self, rule: str, steps: int, radius: int | None=None, stride: int | None=None, born: set | int | None=None, sustain: set | int | None=None, custom_random: CustomRandom | None=None) -> None:
        """
        Performs a Moore-neighborhood cellular automata rule (or random ruleset) upon the passed in frame
        for a given amount of steps. Performs the rules subsections of the array using a kernel if
        a radius and offset are given a value besides None, 0, or a size greater the smallest dimension of the array.

        ===Steps===
        How many times the operation is performed on the passed in array.

        ===Radius===
        Size of the kernel measured from the center pixel + 2*radius outwards.
        For example, a radius of 1 would result in a 3x3 kernel.
        A radius of 0 is a single pixel. Negative radii are taken for their absolute value.
        The kernel is automatically made bigger by 1 pixel on each size
        so that rulesets have the proper information to update, but only the original radius kernel information
        is put back onto the greater array.
        If radius is None, it performs the rule over the entire array.

        ===Stride===
        How many pixels the kernel slides along each substep.
        Defaults to radius*2 + 1. None or 0 also sets it to radius.
        Negative inputs are put through absolute value function.

        ===Rule===
        The cellular automata rule to apply. Several built-in rules are given below.
        Rules are case insensitive.
        Special cases: 
            - "skip" passes the kernel over the sub-section without modifying it
            - "custom" allows you to specify "born" and "sustain" parameters
            - "random" types pick a random rule from a subset of built-in rules to apply each substep
            - ""custom random" allows user to specify a CustomRandom object
                they can pass in with a set of custom rules and weights to each rule.
                Preferable to using sub-arrays and writing if-else random blocks if you want to use different strides.

        ===Born/Sustain===
        Rules for custom Moore-neighborhood cellular automata.
        If a cell's neighborhood sum is within the born set and the cell is dead, the cell comes to life.
        If a cell's neighborhood sum is within the sustain set and the cell is alive, the cell stays alive.
        Otherwise, the cell dies.

        ===custom_random===
        See: Rule for explanation of when to use this parameter.
        CustomRandom objects can have rules and weights added to them using
        the CustomRandom.add_rules() function.
        Rules should be added with their weights (ints, relative weights) at the beginning of the ruleset file.
        They are added in the form [(rule1, weight1), (rule2, weight2), etc].
        Rules are structured as ["rule name", <born_set>, <sustain_set>].
        ------------------------------------------------
            Built-in rules:
                - grow types -
                grow1 - born={2, 4, 7}, sustain=set(range(9)) # cells never die
                grow2 - born={3}, sustain=set(range(9)) 
                grow2 - born={1, 3, 5, 8}, sustain=set(range(8))
                grow rand - picks from these rules randomly

                - decay types -
                decay1 - born={}, sustain=set(range(2, 6))
                decay2 - born={3}, sustain={2, 3} # can also be called by "GoL"
                decay3 - born={}, sustain={1, 2, 3, 5, 6, 7} 
                decay rand - picks from these rules randomly

                - utility/misc -
                skip - does not modify subsection
                random - picks from all grow rules, decay rules, and skip for each substep
                cleanup - born={} sustain={2, 3, 4, 5, 6, 7, 8} # removes pixels with no neighbors
                fill holes - born={8} sustain={range(9)} # fills in holes with 8 neighbors
                fill - returns sub-section of ones (totally filled)
                clear - returns sub-section of zeroes (totally cleared)
                boulder - born={3, 4} sustain={range(9)} # creates nice boulders. 6% noise works well. 1-12 steps recommended
                box2 - born={1, 2, 3} sustain={range(9)} # creates odd boxes. 5-7 steps with 1.5% noise will fill large parts of screen.
        """
        ruleDesc = rule
        if rule == "custom":
            if isinstance(born, int):
                born = (born)
            else:
                born = ()
            if isinstance(sustain, int):
                sustain = (sustain)
            else:
                sustain = ()
            ruleDesc += " born: " + str(born) + " sustain: " + str(sustain)
        if self.verbose:
            print("Doing rule " + ruleDesc, "for", steps, "steps with radius", radius, "and stride", stride)

        for _ in range(steps):
            if self.image_mode:
                self.sequence.append(nextframe.by_slices(self.current_frame, rule, born, sustain, radius, stride, custom_random))
                self.current_frame = self.sequence[-1][0]
            else:
                self.current_frame = nextframe.by_slices(self.current_frame, rule, born, sustain, radius, stride, custom_random)
            
    
    def finish(self) -> np.array:
        """
            Ends processing on array and returns array full of ones and zeros.
            If in image mode, renders png in the "terrain renders" folder under the ruleset name.
            If in anim mode, renders gif in the "terrain renders" folder under the ruleset name.
        """
        if self.verbose:
            print("Terrain gen finished")
            if self.image_mode:
                print("Exporting as image")
        if self.image_mode:
            render.make_png(self.current_frame)
        if self.anim_mode and self.verbose:
                print("Exporting as animation")
        if self.anim_mode:
            render.make_anim(self.sequence)
        return self.current_frame