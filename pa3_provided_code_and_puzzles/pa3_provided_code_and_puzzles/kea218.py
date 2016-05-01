# File: kea218.py
# Author(s) names AND netid's: Kristen Amaddio (kea218), Holliday Shuler (hls262), SangHee Kim (shk172)
# Date: May 3, 2016
# Group work statement: All group members were present and contributing during all work on this project.

#!/usr/bin/env python
import struct, string, math, copy

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board


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
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    # print "Your code will solve the initial_board here!"
    # print "Remember to return the final board (the SudokuBoard object)."
    # print "I'm simply returning initial_board for demonstration purposes."
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    found = False
    result = True
    domains = {}
    for row in range(size):
        for col in range(size):
            domains[(row, col)] = [i+1 for i in range(size)]
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for val in domains[(row, col)]:
                    found = False
                    if val in BoardArray[row]:  # if i is already in the row
                        found = True
                    if val in [BoardArray[i][col] for i in range(size)]:  # if i is already in the col
                        found = True
                    for i in range(subsquare):   # if i is already in the square
                        for j in range(subsquare):
                            if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == val)):
                                found = True
                    if found == False:
                        initial_board.set_value(row, col, val)
                        BoardArray = initial_board.CurrentGameBoard
                        result = solve(initial_board, forward_checking, MRV, Degree, LCV)
                        if result == False:
                            initial_board.set_value(row, col, 0)
                            BoardArray = initial_board.CurrentGameBoard
                        else:
                            print "Officially Set Value:", row, col, BoardArray[row][col]
                            domains[(row, col)] = "closed"
                            if(forward_checking == True):
                                # remove the value from the domains of all open variables in the same row
                                for row1 in range(size):
                                    if domains[(row1, col)] != "closed" and val in domains[(row1, col)]:
                                        temp = []
                                        for num in domains[(row1, col)]:
                                            if num != val:
                                                temp.append(num)
                                        domains[(row1, col)] = copy.deepcopy(temp)
                                        print "After removing: ", row1, col, domains[(row1, col)]
                                # remove the value from the domains of all open variables in the same col
                                for col1 in range(size):
                                    if domains[(row, col1)] != "closed" and val in domains[(row, col1)]:
                                        temp = []
                                        for num in domains[(row, col1)]:
                                            if num != val:
                                                temp.append(num)
                                        domains[(row, col1)] = temp
                                # remove the value from the domains of all open variables in the same col
                                for i in range(subsquare):
                                    for j in range(subsquare):
                                        if domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)] != "closed" and val in domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)]:
                                            temp = []
                                            for num in domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)]:
                                                if num != val:
                                                    temp.append(num)
                                            domains[(SquareRow*subsquare+i, SquareCol*subsquare+j)] = temp
                            break

                if BoardArray[row][col]==0:
                    return False

    return initial_board