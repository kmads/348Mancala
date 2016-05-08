# File: kea218.py
# Author(s) names AND netid's: Kristen Amaddio (kea218), Holliday Shuler (hls262), SangHee Kim (shk172)
# Date: May 3, 2016
# Group work statement: All group members were present and contributing during all work on this project.

#!/usr/bin/env python
import struct, string, math, copy, time

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board
      self.consistencyChecks = 0 # the total number of values tried for all variables


    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and calls a helper function to solve it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    start = time.time()
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    domains = {}  # a dictionary where a (row, col) tuple is the key and an array of possible values is the value

    # initialize the domains of each unassigned cell to 1-size, and the domains of assigned cells to []
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col] == 0:
                domains[(row, col)] = [i+1 for i in range(size)]
            else:
                domains[(row,col)] = []

    # Remove the initial board's set values from the domains of affected cells (same row, col, square)
    if forward_checking:
        for row in range(size):
            for col in range(size): 
                val = BoardArray[row][col]
                if val != 0:
                    domains = forwardChecking(row,col,val,domains,BoardArray)

    # pass the domains and the start time to the helper function to solve
    return solveWithDomains(initial_board, forward_checking, MRV, Degree, LCV, domains, start)

def solveWithDomains(initial_board, forward_checking, MRV, Degree, LCV, domains, start):
    """Takes an initial SudokuBoard to solve it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments) by keeping track of the domains of possible values for each variable.
     Times out after ten minutes. Returns the resulting board solution. """
    maxTime = 600 # Upper bound on time
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)

    if MRV == True:     # check the variables in order of increasing number of values in their domains
        mrvKeys = sortByMRV(domains)    # determine the order to check the variables
        for cell in mrvKeys:
            row = cell[0]
            col = cell[1]
            if BoardArray[row][col] == 0:   # only perform a check if the cell is unassigned
                for val in domains[(row, col)]:     # no set ordering of the values in MRV
                    curTime = time.time() - start
                    if curTime < maxTime:           # only keep checking if it has been less than 10 min
                        initial_board.consistencyChecks += 1    # for each value it tries, increment the consistency checks count
                        found = checkBoard(row, col, val, BoardArray)   # check if the value is already in the row, col, or square
                        if found == False:
                            # try the value by making recursive calls with forward checking to fill the board:
                            initial_board, domains = checkVal(initial_board, row, col, val, forward_checking, MRV, Degree, LCV, domains, start)
                            BoardArray = initial_board.CurrentGameBoard # since initial_board has changed, update BoardArray
                        if BoardArray[row][col] != 0:  # if the value was not rejected, don't try any more
                            break
                curTime = time.time() - start
                # if all values were tried and none worked and there's still time, return failure:
                if BoardArray[row][col] == 0 and curTime < maxTime:
                    return False
    if LCV == True:
        # check the next value that is in the fewest domains for other open variables in its row, col, and square
        for row in range(size):     # no set ordering of the variables in LCV
            for col in range(size):
                if BoardArray[row][col]==0:  # only perform a check if the cell is unassigned
                    sortedVals = sortByLCV(row, col, domains, size)     # sort the domain of the variable
                    for val in sortedVals:
                        curTime = time.time() - start
                        if curTime < maxTime:       # check how long it has been running
                            initial_board.consistencyChecks += 1    # for each value tried, increment the consistency checks count
                            found = checkBoard(row, col, val, BoardArray)   # make sure the val is not already in the row, col, square
                            if found == False:
                                # try the value by making recursive calls with forward checking to fill the board:
                                initial_board, domains = checkVal(initial_board, row, col, val, forward_checking, MRV, Degree, LCV, domains, start)
                                BoardArray = initial_board.CurrentGameBoard # since initial_board has changed, update BoardArray
                            if BoardArray[row][col] != 0:  # if the value was not rejected, don't try any more
                                break
                    curTime = time.time() - start
                    # if all values were tried and none worked and there's still time, return failure:
                    if BoardArray[row][col] == 0 and curTime < maxTime:
                        return False

    if Degree == True:
        # check the next variable with the most open variables in its row, col, and square
        degKeys = sortByDegree(BoardArray)  # sort the variables
        for cell in degKeys:
            row = cell[0]
            col = cell[1]
            for val in domains[(row, col)]:  # no set ordering of the values for Degree
                curTime = time.time() - start
                if curTime < maxTime:   # check how long it has been running
                    initial_board.consistencyChecks += 1  # for each value tried, increment the consistency checks count
                    found = checkBoard(row, col, val, BoardArray)  # make sure the val is not already in the row, col, square
                    if found == False:
                        # try the value by making recursive calls with forward checking to fill the board:
                        initial_board, domains = checkVal(initial_board, row, col, val, forward_checking, MRV, Degree, LCV, domains, start)
                        BoardArray = initial_board.CurrentGameBoard # since initial_board has changed, update BoardArray
                    if BoardArray[row][col] != 0:  # if the value was not rejected, don't try any more
                        break
            curTime = time.time() - start
            # if all values were tried and none worked and there's still time, return failure:
            if BoardArray[row][col]==0 and curTime < maxTime:
                return False

    if MRV == False and LCV == False and Degree == False:  # just backtracking and possibly forward checking
        for row in range(size):  # no set ordering for the variables
            for col in range(size):
                if BoardArray[row][col]==0:  # only perform a check if the cell is unassigned
                    for val in domains[(row, col)]:  # no set ordering for the values
                        curTime = time.time() - start
                        if curTime < maxTime:  # check how long it has been running
                            initial_board.consistencyChecks += 1  # for each value tried, increment the consistency checks count
                            found = checkBoard(row, col, val, BoardArray)   # make sure the val is not already in the row, col, square
                            if found == False:
                                # try the value by making recursive calls with forward checking to fill the board:
                                initial_board, domains = checkVal(initial_board, row, col, val, forward_checking, MRV, Degree, LCV, domains, start)
                                BoardArray = initial_board.CurrentGameBoard # since initial_board has changed, update BoardArray
                            if BoardArray[row][col] != 0:  # if the value was not rejected, don't try any more
                                break
                    curTime = time.time() -start
                    # if all values were tried and none worked and there's still time, return failure:
                    if BoardArray[row][col]==0 and curTime < maxTime:
                        return False

    # even if the board is not complete, always return it
    return initial_board


def sortByMRV(domains):
    """ sorts the variables by increasing length of their domains, returns an array of (row, col) tuples"""
    return sorted(domains, key=lambda k: len(domains[k]), reverse=False)


def sortByLCV(row, col, domains, size):
    """ sorts the values in the domain at (row, col) according to the least number of variables
    in the row, col, or square that also have that value in their domains, returns the sorted values as an array"""

    constraints ={}  # keeps track of how many open variables in the same row, col, or square also have that val in their domain
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for val in domains[(row, col)]:  # checks each val
        count = 0
        for row1 in range(size):    # checks the column
            if val in domains[(row1, col)]:
                count += 1
        for col1 in range(size):  # checks the row
            if val in domains[(row, col1)]:
                count += 1
        for i in range(subsquare):   # checks the square
            for j in range(subsquare):
                if val in domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)]:
                    count += 1
        constraints[val] = count  # adds the total count as the value in the dictionary
    return sorted(constraints, key=lambda k: constraints[k], reverse=True)  # sorts the dictionary, returns the values as an array


def sortByDegree(BoardArray):
    """ sorts the open variables by decreasing number of open variables in its
    row, col, or square (checks the most first). Returns an array of the sorted variables as (row, col) tuples"""

    openVars ={}
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    for row in range(size):     # iterate over whole board
        for col in range(size):
            if BoardArray[row][col] == 0:   # only examine open cells
                count = 0
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for col1 in BoardArray[row]:  # checks how many are unassigned in the same row
                    if col1 == 0:
                        count += 1
                for row1 in [BoardArray[i][col] for i in range(size)]:  # checks how many are unassigned in the same col
                    if row1 == 0:
                        count += 1
                for i in range(subsquare):   # checks how many are unassigned in the same square
                    for j in range(subsquare):
                        row1 = SquareRow*subsquare+i
                        col1 = SquareCol*subsquare+j
                        if BoardArray[row1][col1] == 0:
                            count += 1
                openVars[(row, col)] = count  # makes the total count of open variables the (row, col)'s value
    # sorts the (row, col) tuples (the keys) by decreasing value
    return sorted(openVars, key=lambda k: openVars[k], reverse=True)



def checkBoard(row, col, val, BoardArray):
    """ returns true if val is already assigned to a variable in the same row, col, or square, false otherwise"""

    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    found = False
    if val in BoardArray[row]:  # if val is already in the row
        found = True
    if val in [BoardArray[i][col] for i in range(size)]:  # if val is already in the col
        found = True
    for i in range(subsquare):   # if val is already in the square
        for j in range(subsquare):
            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == val)):
                found = True
    return found


def forwardChecking(row, col, val, domains, BoardArray):
    """ removes val from the domains of all open variables in row, col, or square. Returns updated domains """

    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for row1 in range(size):  # check every cell in the row
        if domains[(row1, col)] != [] and val in domains[(row1, col)]: # if an open variable has val in its domain
            temp = []
            for num in domains[(row1, col)]:
                if num != val:
                    temp.append(num)
            domains[(row1, col)] = copy.copy(temp)  # update domains

    for col1 in range(size): # check every cell in the col
        if domains[(row, col1)] != [] and val in domains[(row, col1)]:  # if an open variable has val in its domain
            temp = []
            for num in domains[(row, col1)]:
                if num != val:
                    temp.append(num)
            domains[(row, col1)] = copy.copy(temp)  # update domains

    for i in range(subsquare):  # check every cell in the square
        for j in range(subsquare):
            # if an open variable has val in its domain:
            if domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)] != [] and val in domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)]:
                temp = []
                for num in domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)]:
                    if num != val:
                        temp.append(num)
                domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)] = copy.copy(temp) # update domains
    return domains


def checkVal(initial_board, row, col, val, forward_checking, MRV, Degree, LCV, domains, start):
    """ tentatively assigns val to the cell at (row, col), then applies forward checking if necessary, and
    makes a recursive call to domains to see if the value causes issues later (backtracking). If the recursive call
    causes problems, the value is reset to 0. Returns the updated board and domains."""

    initial_board.set_value(row, col, val)
    tempDomains = copy.copy(domains) # keeps a copy of domains in case it must be reset
    domains[(row, col)] = []
    BoardArray = initial_board.CurrentGameBoard
    if(forward_checking == True):
        domains = forwardChecking(row, col, val, domains, BoardArray)
    result = solveWithDomains(initial_board, forward_checking, MRV, Degree, LCV, domains, start)
    if result == False:  # if it failed, reset the board and domains
        initial_board.set_value(row, col, 0)
        domains = copy.copy(tempDomains)

    return initial_board, domains