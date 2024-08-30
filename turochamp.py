#!/usr/bin/python

# Program that places a number of chess pieces on a board so that they can't capture each other
# Problem originated from GCHQ: https://www.gchq.gov.uk/information/turing-challenge/crown

import os

# Some chess-related definitions

KING =   1
QUEEN =  2
KNIGHT = 3
BISHOP = 4
ROOK =   5

# Possible moves for various pieces, relative notation [rank, coulumn]
not_used = []
knight_moves = [[-1,-2],[-2,-1],[1,2],[2,1],[-1,2],[-2,1],[1,-2],[2,-1]]
bishop_moves = [[-7,-7],[-6,-6],[-5,-5],[-4,-4],[-3,-3],[-2,-2],[-1,-1],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],
                [-7,7],[-6,6],[-5,5],[-4,4],[-3,3],[-2,2],[-1,1],[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7]]
rook_moves = [[-7,0],[-6,0],[-5,0],[-4,0],[-3,0],[-2,0],[-1,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],
              [0,-7],[0,-6],[0,-5],[0,-4],[0,-3],[0,-2],[0,-1],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]]
queen_moves = bishop_moves + rook_moves

# Put move lists in another list, indexed by piece type
moves = [not_used, not_used, queen_moves, knight_moves, bishop_moves, rook_moves]

# Utility functions

# Check if a position lies within the board
def is_valid(rank,file):
        return rank >= 0 and rank <= 7 and file >= 0 and file <= 7

# Converts algebraic notation to [rank, file] numbers
def coords(position):
        # [rank, file]
        return [ord(position[1])-ord('1'), ord(position[0])-ord('a')]

def is_free(position, free):
        # [rank][file]
	return free[position[0]][position[1]] == 0

# Check that the piece in the position won't threaten other pieces
def check_moves(position, moves, placement):
        for move in moves:
                if is_valid(position[0]+move[0], position[1]+move[1]):
                        if placement[position[0]+move[0]][position[1]+move[1]] != 0:
                                return False
        return True

# Python uses references for lists, so we need to make a new instead of assigning
def makecopy(board):
        res = []
        for rank in board:
                res.append(list(rank))
        return res

# Ordinary assignment in python just copies reference. This is deep ... copy
def copy(board, new_board):
        for i in range(8):
                for j in range(8):
                        board[i][j] = new_board[i][j]

# Place a piece in position and mark threatened positions
def place_piece(pos, b, h, moves, marker):
        b[pos[0]][pos[1]] = marker
        h[pos[0]][pos[1]] = marker
        for move in moves:
                if is_valid(pos[0]+move[0],pos[1]+move[1]):
                        h[pos[0]+move[0]][pos[1]+move[1]] = marker

# The actual problem solution

def check_pieces(b, h, pieces, positions):
        if not pieces:
                # If the list is empty, we're done
                return True
        else:
                # Pick the first piece in the list
                piece = pieces[0]
                # Check its possible postions
                for pos in positions[0]:
                        # Check that the proposed position isn't held by another piece
                        if is_free(coords(pos), h):
                                # Check that the proposed position can't threaten any other piece
                                if check_moves(coords(pos), moves[piece], b):
                                        # Make copies and place the piece in the copy
                                        b_test = makecopy(b)
                                        h_test = makecopy(h)
                                        place_piece(coords(pos), b_test, h_test, moves[piece], piece)
                                        # If the other pieces could be placed this way, we're done
                                        if check_pieces(b_test, h_test, pieces[1:],positions[1:]):
                                                # It worked, so we can copy back
                                                copy(b, b_test)
                                                copy(h, h_test)
                                                return True
                return False

# Note reverse order of ranks

# Represents the contents of the board at the start
board = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,KING,0,0,0,0,0,0]]

# Shows which piece that can take each square on the board. Only one is shown.
held = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[KING,KING,KING,0,0,0,0,0],[KING,KING,KING,0,0,0,0,0]]

# The seven pieces that we are going to place on the board
pieces = [QUEEN, KNIGHT, KNIGHT, BISHOP, BISHOP, ROOK, ROOK]

# Possible positions for each of the pieces
squares = [['d7', 'd6', 'd3', 'g8', 'h8'],['d4','d5','b1','g6'],['a6','b6','e7','f7','e8','f8','g4','g5'],
           ['a3','a4','c2','e4','e5','f4','f5','h4'],['b3','b4','b5','d8','e2','h5','h6','h7'],
           ['a1','a2','c4','c5','c7','c8','e3','e6','f6','g2','g3','h2','h3'],
           ['b2','c1','c6','d1','f1','g1','g7','h1']]

if check_pieces(board, held, pieces, squares):
        for rank in range(7,-1,-1):
                print(board[rank])
