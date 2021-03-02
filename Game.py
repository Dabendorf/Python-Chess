from Board import Board
from Piece import Piece
from Move import Move

b = Board()
to_move = Piece.White
num_squares_to_edge = [[]]

def main():
	global b

	moves = []
	global num_squares_to_edge
	b.square[27] = Piece.White | Piece.Rook
	num_squares_to_edge = compute_margin_to_edge()
	
	global to_move

	print(all_possible_turns_player(to_move))

	""" p = Piece.Black | Piece.King
	print(p)
	print(Piece.Black in p)
	print(Piece.King in p)
	print(Piece.White in p)
	print(Piece.Knight in p) """
	
	b.print_board()

def is_legal(piece: Piece):
	pass

def all_possible_turns_piece(piece: Piece) -> [Move]:
	pass

def all_possible_turns_player(player_to_move: Piece) -> [Move]:
	# for every piece, if colour of player to move
	# if own piece in way, change searching direction
	# if opponent's piece in way, capture it, then change direction

	global b
	moves = []

	for i in range(0, 64):
		if(is_same_colour(b.square[i], player_to_move)):
			if is_sliding_piece(b.square[i]):
				moves.extend(generate_sliding_moves(i, b.square[i]))

	return moves

	# weitere Pieces hinzufügen


def generate_sliding_moves(start_sq: int, piece: Piece) -> [Move]:
	""""""
	direction_offsets = [8, -8, -1, 1, 7, -7, 9, -9]
	moves = []
	start_ind = 0
	end_ind = 8
	if Piece.Bishop in piece:
		start_ind = 4
	if Piece.Rook in piece:
		end_ind = 4

	for direction in range(start_ind, end_ind):
		for to_go in range(0, num_squares_to_edge[start_sq][direction]):
			target_sq = start_sq + direction_offsets[direction] * (to_go + 1)
			target_sq_piece = b.square[target_sq]

			if is_same_colour(piece, target_sq_piece):
				break

			moves.append(Move(start_sq, target_sq, ""))

			if is_different_colour(piece, target_sq_piece):
				break

	return moves

			



def is_check(b: Board):
	pass


def is_checkmate(b: Board):
	pass


def move(p: Piece):
	if is_sliding_piece(p):
		pass
	elif Piece.Pawn in p:
		pass
	elif Piece.King in p:
		pass
	elif Piece.Knight in p:
		pass
	pass
	# Rook: +8, -8, +1, -1
	# Bishop: 7, 9, -9, -7


def compute_margin_to_edge() -> [[int]]:
	""" Helping method calculating the margin of a piece to the edge of the bord in all directions"""

	num_squares_to_edge = [0]*64
	for letter in range(0,8):
		for number in range(0,8):
			margin_N = 7 - letter
			margin_S = letter
			margin_W = number
			margin_E = 7 - number

			index_square = 8*letter + number

			num_squares_to_edge[index_square] = [margin_N, margin_S, margin_W, margin_E,
			min(margin_N, margin_W), min(margin_S, margin_E), min(margin_N, margin_E), min(margin_S, margin_W)]

	return num_squares_to_edge


def is_same_colour(piece1: Piece, piece2: Piece):
	""" For two pieces, function returns if both pieces have the same colour"""

	if Piece.White in piece1 and Piece.White in piece2:
		return True
	elif Piece.Black in piece1 and Piece.Black in piece2:
		return True
	else:
		return False

def is_different_colour(piece1: Piece, piece2: Piece):
	""" For two pieces, function returns if both pieces are different
		Pay attention for the fact that this is not the opposite of same_colour as it is possible to be Piece.Empty"""

	if Piece.White in piece1 and Piece.Black in piece2:
		return True
	elif Piece.Black in piece1 and Piece.White in piece2:
		return True
	else:
		return False


def is_sliding_piece(piece: Piece):
	""" Rooks, Bishops and Queens share some properties, function returns if piece is one of them"""

	return Piece.Rook in piece or Piece.Bishop in piece or Piece.Queen in piece


if __name__ == "__main__":
	main()