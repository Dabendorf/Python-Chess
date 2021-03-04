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
	b.square[36] = Piece.White | Piece.Bishop
	num_squares_to_edge = compute_margin_to_edge()
	
	global to_move

	print(all_possible_turns_player(to_move))
	print(all_possible_turns_piece(27))
	print(all_possible_turns_piece(36))

	""" p = Piece.Black | Piece.King
	print(p)
	print(Piece.Black in p)
	print(Piece.King in p)
	print(Piece.White in p)
	print(Piece.Knight in p) """
	
	b.print_board()

def is_legal(piece: Piece):
	pass

def all_possible_turns_piece(start_sq: int) -> [Move]:
	piece = b.square[start_sq]
	moves = []

	if is_sliding_piece(piece):
		moves.extend(generate_sliding_moves(start_sq, piece))
	elif Piece.King in piece:
		moves.extend(generate_king_moves(start_sq, piece))
	elif Piece.Pawn in piece:
		moves.extend(generate_pawn_moves(start_sq, piece))
	elif Piece.Knight in piece:
		moves.extend(generate_knight_moves(start_sq, piece))

	return moves

	# TODO More pieces

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

	# TODO weitere Pieces hinzufügen


def generate_sliding_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Rooks, Bishops and Queens"""
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

			moves.append(Move(start_sq, target_sq, get_move_notation(piece, start_sq, target_sq)))
			# moves.append(Move(start_sq, target_sq, ""))

			if is_different_colour(piece, target_sq_piece):
				break

	return moves

			
def generate_king_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Kings"""
	moves = []
	return moves # TODO Implement


def generate_pawn_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Pawns"""
	moves = []
	return moves # TODO Implement


def generate_knight_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Knights"""
	moves = []
	return moves # TODO Implement


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


def get_move_notation(piece: Piece, start_sq: int, target_sq: int) -> str:
	"""This method returns a string of algebraic chess notation for a move"""
	start_sq_ind = index_to_square_name(start_sq)
	target_sq_ind = index_to_square_name(target_sq)

	# TODO Please note: This function is programmed in a way to calculate the notation __before__ the move happens
	# TODO Does not include check, checkmate, castling or promotion yet

	#print(piece)
	if Piece.Pawn in piece:
		# TODO Promoting pieces missing
		if start_sq % 8 == target_sq % 8:
			return target_sq
		elif abs((start_sq % 8) - (target_sq % 8)) == 1:
			# Capture to the left
			if (start_sq % 8) - (target_sq % 8) == 1:
				# Edge on the left
				if (start_sq % 8) != 1:
					# If other pawn was able to do it
					if Piece.Pawn in b.square[start_sq-2]:
						return start_sq_ind+"x"+target_sq_ind
					else:
						"x"+target_sq_ind
				else:
					"x"+target_sq_ind
			# Capture to the right
			else:
				# Edge on the right
				if (start_sq % 8) != 6:
					# If other pawn was able to do it
					if Piece.Pawn in b.square[start_sq+2]:
						return start_sq_ind+"x"+target_sq_ind
					else:
						"x"+target_sq_ind
				else:
					"x"+target_sq_ind


	elif Piece.King in piece:
		if Piece.Empty not in b.square[target_sq]:
			return "Kx" + target_sq_ind
		else:
			return "K" + target_sq_ind

	elif Piece.Queen in piece:
		# TODO Fix ambiguatiy if two Queens where able to get here
		if Piece.Empty not in b.square[target_sq]:
			return "Qx" + target_sq_ind
		else:
			return "Q" + target_sq_ind

	elif Piece.Rook in piece:
		# TODO Fix ambiguatiy if two Rooks where able to get here
		if Piece.Empty not in b.square[target_sq]:
			return "Rx" + target_sq_ind
		else:
			return "R" + target_sq_ind

	elif Piece.Bishop in piece:
		# TODO Fix ambiguatiy if two Bishops where able to get here
		if Piece.Empty not in b.square[target_sq]:
			return "Bx" + target_sq_ind
		else:
			return "B" + target_sq_ind

	elif Piece.Knight in piece:
		# TODO Fix ambiguatiy if two Knight where able to get here
		if Piece.Empty not in b.square[target_sq]:
			return "Nx" + target_sq_ind
		else:
			return "N" + target_sq_ind

	else:
		return ""

def index_to_square_name(ind: int) -> str:
	"""Returns the name of a square (e.g. A4) for any index on the board """
	num_dict = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

	#return ""
	return num_dict[ind%8]+str(int(ind/8)+1)

def castle(player_to_move: Piece, long: bool) -> bool:
	"""Möglich wenn: der König noch nicht gezogen wurde,
    der beteiligte Turm noch nicht gezogen wurde,
    zwischen dem König und dem beteiligten Turm keine andere Figur steht,
    der König über kein Feld ziehen muss, das durch eine feindliche Figur bedroht wird,
    der König vor und nach Ausführung der Rochade nicht im Schach steht."""
	
	global b

	if is_check(b):
		return False
	elif Piece.White in player_to_move:
		# White Player
		if b.moved_king_white:
			return False
		elif long:
			if b.moved_rook_white_a1:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-fields
		else:
			# Short
			if b.moved_rook_white_h1:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-fields
	else:
		# Black Player
		if b.moved_king_black:
			return False
		elif long:
			if b.moved_rook_black_a8:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-fields
		else:
			# Short
			if b.moved_rook_black_h8:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-fields
		
	

	# TODO Proof of all the named conditions and the booleans
	pass


if __name__ == "__main__":
	main()