from Board import Board
from Piece import Piece

def main():
	b = Board()
	moves = []

	p = Piece.Black | Piece.King
	print(p)
	print(Piece.Black in p)
	print(Piece.King in p)
	print(Piece.White in p)
	print(Piece.Knight in p)
	
	b.print_board()

def is_legal(piece: Piece):
	pass

def all_possible_turns_piece(piece: Piece):
	pass

def all_possible_turns_player(piece: Piece):
	# for every piece, if colour of player to move
	# wenn eigene Figur im Weg, dann Richtung ändern
	# wenn fremde Figur, dann ggf. nehmen
	pass

def is_check(b: Board):
	pass


def is_checkmate(b: Board):
	pass

def move(p: Piece):
	pass
	# Rook: +8, -8, +1, -1
	# Bishop: 7, 9, -9, -7



if __name__ == "__main__":
	main()