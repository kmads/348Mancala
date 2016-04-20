# File: kea218.py
# Author(s) names AND netid's: Kristen Amaddio (kea218), Holliday Shuler (hls262), SangHee Kim (shk172)
# Date: April 22, 2016
# Group work statement: All group members were present and contributing during all work on this project.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            # print m
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            # print m
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        # print "Alpha Beta Move not yet implemented"
        #returns the score adn the associated moved
        move = -1
        score = -INFINITY
        alpha = -INFINITY
        beta = INFINITY
        turn = kea218(self.num, self.type, self.ply)
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (turn.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValueAB(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValueAB(self, board, ply, turn, alpha, beta):
        """ Find the alpha-beta utility value for the next move for this player
        at a given board configuation. Returns score.
        alpha = best alternative for MAX along the path
        beta = best alternative for MIN along the path"""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValueAB(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
            # Don't go any further because you won't find any better
            # print m
            if score >= beta:
                return score
            # Otherwise change the alpha value to keep track of the best (highest) score
            # we found so far
            alpha = max(alpha, score)
        return score
    
    def minValueAB(self, board, ply, turn, alpha, beta):
        """ Find the alpha-beta utility value for the next move for this player
            at a given board configuation. Returns score.
            alpha = best alternative for MAX along the path
            beta = best alternative for MIN along the path"""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValueAB(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
            # Don't go any further because you won't find any better
            # print m
            if score <= alpha:
                return score
            # Otherwise change the beta value to keep track of the best (lowest) score
            # we found so far
            beta = min(beta, score)
        return score
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            # Use AB pruning with a ply of 9
            val, move = self.alphaBetaMove(board, 9)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class kea218(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Calculates the score from the perspective of Player, assuming they have just made a move
        # Considers overall Mancala difference, and if Player has set up the other player to earn lots of points
        score = 0

        if(self.num == 1):
            score += board.scoreCups[0] - board.scoreCups[1]      	# basic overall score gained *after* this turn
            # check how much P2 can now gain:
            for i in range(0, len(board.P2Cups)):
                if board.P2Cups[i] == 0:   # empty cups on the other side
                    for j in range(0, len(board.P2Cups)):   # look for starting cups on the other side that can land in the empty cup
                        if j < i and (board.P2Cups[j] == i-j or board.P2Cups[j] == 14 + i-j):
                            score -= board.P1Cups[j]

                elif (6 - i) < board.P2Cups[i] < (12 - i):  # if P2 lands on P1's side P2 added one to its Mancala
                    score -= 1			                    # without adding one to P1's Mancala - lose points

                # If the pebbles end at the mancala, player gets one more turn and
                # no pebble is given to the opponent lose some more points since the
                # player gets an extra turn
                elif board.P1Cups[i] == (6 - i):
                    score -= 4

                # If the pebbles end at the mancala after two full rounds, lose fewer points
                # since the player gave the opponents some pebbles as well
                elif board.P1Cups[i] == (20 - i):
                    score -= 2

        else:   # from the perspective of P2
            score += board.scoreCups[1] - board.scoreCups[0]      	# basic overall score gained *after* this turn

            for i in range(0, len(board.P1Cups)):   # empty cups on the other side
                if board.P1Cups[i] == 0:
                    # find starting cups on the other side that can land in the empty cup
                    for j in range(0, len(board.P1Cups)):
                        if j < i and (board.P1Cups[j] == i-j or board.P1Cups[j] == 14 + i-j):
                            score -= board.P2Cups[j]

                elif (6 - i) < board.P1Cups[i] < (12 - i):# if P2 lands on P1's side P2 added one to its Mancala
                    score -= 1			                    # without adding one to P1's Mancala - lose points

                # If the pebbles end at the mancala, player gets one more turn and
                # no pebble is given to the opponent lose some more points since the
                # player gets an extra turn
                elif board.P1Cups[i] == (6 - i):
                    score -= 4

                # If the pebbles end at the mancala after two full rounds, lose fewer points
                # since the player gave the opponents some pebbles as well
                elif board.P1Cups[i] == (20 - i):
                    score -= 1.5

        print "Calling score in MancalaPlayer"
        return score
        
