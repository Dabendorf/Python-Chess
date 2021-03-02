from Board import Board
from Piece import Piece
from Move import Move

def main():
	b = Board()
	moves = []
	num_squares_to_edge = compute_margin_to_edge()
	direction_offsets = [8, -8, -1, 1, 7, -7, 9, -9]
	
	to_move = Piece.White

	p = Piece.Black | Piece.King
	print(p)
	print(Piece.Black in p)
	print(Piece.King in p)
	print(Piece.White in p)
	print(Piece.Knight in p)
	
	b.print_board()

def is_legal(piece: Piece):
	pass

def all_possible_turns_piece(piece: Piece) -> [Move]:
	pass

def all_possible_turns_player(piece: Piece) -> [Move]:
	# for every piece, if colour of player to move
	# if own piece in way, change searching direction
	# if opponent's piece in way, capture it, then change direction


	pass

def is_check(b: Board):
	pass


def is_checkmate(b: Board):
	pass

def move(p: Piece):
	if Piece.Bishop in p or Piece.Rook in p or Piece.Queen in p:
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




if __name__ == "__main__":
	main()