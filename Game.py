from Board import Board
from Piece import Piece
from Move import Move
from SpecialTurn import SpecialTurn

#global variables are evil and need to go
b = Board()
to_move = Piece.White
num_squares_to_edge = [[]]
all_moves = []

def main():
	global b
	global all_moves
	global to_move
	global num_squares_to_edge

	num_squares_to_edge = compute_margin_to_edge()
	print("Possible moves: "+str(all_possible_turns_player(to_move)))
	# thats a temporary test structure for some example moves
	
	moves_to_do_list = [(14, 22), (52, 36), (5, 14)]

	for st, tg in moves_to_do_list:
		print("Turn "+get_move_notation(b.square[st], st, tg)+" legal: "+str(move(st, tg)))
		b.print_board()

		if to_move == Piece.White:
			to_move = Piece.Black
		else:
			to_move = Piece.White
		
		print("========")
		num_squares_to_edge = compute_margin_to_edge()
		print("Possible moves: "+str(all_possible_turns_player(to_move)))



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
			elif Piece.King in b.square[i]:
				moves.extend(generate_king_moves(i, b.square[i]))
			elif Piece.Pawn in b.square[i]:
				moves.extend(generate_pawn_moves(i, b.square[i]))
			elif Piece.Knight in b.square[i]:
				moves.extend(generate_knight_moves(i, b.square[i]))

	return moves


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

			if is_different_colour(piece, target_sq_piece):
				break

	return moves

			
def generate_king_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Kings"""
	moves = []

	global b

	dire = [-7, -8, -9, -1, 1, 7, 8, 9]
	for i in dire:
		if not is_check(b):
			target_sq = start_sq+i
			if target_sq > -1 and target_sq < 64:
				if not is_same_colour(piece, b.square[target_sq]):
					moves.append(Move(start_sq, target_sq, get_move_notation(piece, start_sq, target_sq)))

	# TODO: Rochade
	# TODO the used check function above is not working yet

	return moves


def generate_pawn_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Pawns"""
	moves = []
	global b

	if Piece.White in piece:
		if start_sq//8 == 1:
			if Piece.Empty in b.square[start_sq+8] and Piece.Empty in b.square[start_sq+16]:
				moves.append(Move(start_sq, start_sq+16, get_move_notation(piece, start_sq, start_sq+16)))
		
		if Piece.Empty in b.square[start_sq+8]:
			moves.append(Move(start_sq, start_sq+8, get_move_notation(piece, start_sq, start_sq+8)))

		if start_sq % 8 != 0:
			if is_same_colour(piece, b.square[start_sq+7]):
				moves.append(Move(start_sq, start_sq+7, get_move_notation(piece, start_sq, start_sq+7)))

		if start_sq % 8 != 7:
			if is_different_colour(piece, b.square[start_sq+9]):
				moves.append(Move(start_sq, start_sq+9, get_move_notation(piece, start_sq, start_sq+9)))

	else:
		if start_sq//8 == 6:
			if Piece.Empty in b.square[start_sq-8] and Piece.Empty in b.square[start_sq-16]:
				moves.append(Move(start_sq, start_sq-16, get_move_notation(piece, start_sq, start_sq-16)))
		
		if Piece.Empty in b.square[start_sq-8]:
			moves.append(Move(start_sq, start_sq-8, get_move_notation(piece, start_sq, start_sq-8)))

		if start_sq % 8 != 0:
			if is_same_colour(piece, b.square[start_sq-9]):
				moves.append(Move(start_sq, start_sq-9, get_move_notation(piece, start_sq, start_sq-9)))

		if start_sq % 8 != 7:
			if is_different_colour(piece, b.square[start_sq-7]):
				moves.append(Move(start_sq, start_sq-7, get_move_notation(piece, start_sq, start_sq-7)))

	global all_moves

	# En passante
	if len(all_moves) != 0:
		last_move = all_moves[-1]
		last_move_str = str(last_move.__str__)
		if len(last_move_str.replace("+", "")) == 2:
			if abs(last_move.start_square - last_move.target_square) == 16:
				# White
				if Piece.White in piece:
					# En passante from left
					if start_sq+1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq+9, get_move_notation(piece, start_sq, start_sq+9)))
					# En passante from right
					elif start_sq-1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq+7, get_move_notation(piece, start_sq, start_sq+7)))
				# Black
				else:
					# En passante from left
					if start_sq+1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq-7, get_move_notation(piece, start_sq, start_sq-7)))
					# En passante from right
					elif start_sq-1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq-9, get_move_notation(piece, start_sq, start_sq-9)))

	# TODO: Promotion; a bit tricky because it must be included in all the other existing things, four times for four different promotion pieces

	return moves


def generate_knight_moves(start_sq: int, piece: Piece) -> [Move]:
	"""Generates moves for Knights"""
	moves = []
	global b

	# Up
	if start_sq % 8 != 0 and start_sq//8 < 6:
		if not is_same_colour(piece, b.square[start_sq+15]):
			moves.append(Move(start_sq, start_sq+15, get_move_notation(piece, start_sq, start_sq+15)))
	if start_sq % 8 != 7 and start_sq//8 < 6:
		if not is_same_colour(piece, b.square[start_sq+17]):
			moves.append(Move(start_sq, start_sq+17, get_move_notation(piece, start_sq, start_sq+17)))

	# Right
	if start_sq % 8 < 6 and start_sq//8 != 7:
		if not is_same_colour(piece, b.square[start_sq+10]):
			moves.append(Move(start_sq, start_sq+10, get_move_notation(piece, start_sq, start_sq+10)))
	if start_sq % 8 < 6 and start_sq//8 != 0:
		if not is_same_colour(piece, b.square[start_sq-6]):
			moves.append(Move(start_sq, start_sq-6, get_move_notation(piece, start_sq, start_sq-6)))

	# Down
	if start_sq % 8 != 0 and start_sq//8 > 1:
		if not is_same_colour(piece, b.square[start_sq-17]):
			moves.append(Move(start_sq, start_sq-17, get_move_notation(piece, start_sq, start_sq-17)))
	if start_sq % 8 != 7 and start_sq//8 > 1:
		if not is_same_colour(piece, b.square[start_sq-15]):
			moves.append(Move(start_sq, start_sq-15, get_move_notation(piece, start_sq, start_sq-15)))

	# Left
	if start_sq % 8 > 1 and start_sq//8 != 0:
		if not is_same_colour(piece, b.square[start_sq-10]):
			moves.append(Move(start_sq, start_sq-10, get_move_notation(piece, start_sq, start_sq-10)))
	if start_sq % 8 > 1 and start_sq//8 != 7:
		if not is_same_colour(piece, b.square[start_sq+6]):
			moves.append(Move(start_sq, start_sq+6, get_move_notation(piece, start_sq, start_sq+6)))
	
	return moves


def is_check(b: Board) -> bool:
	return False # TODO


def is_checkmate(b: Board) -> bool:
	pass


def move(start_sq, target_sq) -> bool:
	"""Makes a move on the board, returns bool if successfull (false=illegal)"""
	global b
	global all_moves

	if to_move not in b.square[start_sq]:
		return False

	new_move = Move(start_sq, target_sq, get_move_notation(b.square[start_sq], start_sq, target_sq))

	poss_moves = all_possible_turns_piece(start_sq)
	
	if new_move in poss_moves:
		all_moves.append(new_move)
		b.square[target_sq] = b.square[start_sq]
		b.square[start_sq] = Piece.Empty

		return True
	else:
		return False



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


def get_move_notation(piece: Piece, start_sq: int, target_sq: int, special_turn: SpecialTurn = None, is_check : bool = False, is_checkmate = False) -> str:
	"""This method returns a string of algebraic chess notation for a move"""
	start_sq_ind = index_to_square_name(start_sq)
	target_sq_ind = index_to_square_name(target_sq)

	# TODO Please note: This function is programmed in a way to calculate the notation __before__ the move happens
	# TODO Does not include promotion yet
	# TODO Please note: This function does not handle ambiguatiy yet (e.g. if two rooks could have moved to a square)

	check_string = ""
	if is_checkmate:
		check_string = "#"
	elif is_check:
		check_string = "+"

	promotion_string = ""
	
	if special_turn is not None:
		if SpecialTurn.PromoteQueen in special_turn:
			promotion_string = "=Q"
		elif SpecialTurn.PromoteRook in special_turn:
			promotion_string = "=R"
		elif SpecialTurn.PromoteBishop in special_turn:
			promotion_string = "=B"
		elif SpecialTurn.PromoteKnight in special_turn:
			promotion_string = "=K"

	move_string = ""

	if Piece.Pawn in piece:
		if start_sq % 8 == target_sq % 8:
			move_string = target_sq_ind
		elif abs((start_sq % 8) - (target_sq % 8)) == 1:
			# Capture to the left
			if (start_sq % 8) - (target_sq % 8) == 1:
				# Edge on the left
				if (start_sq % 8) != 1:
					# If other pawn was able to do it
					if Piece.Pawn in b.square[start_sq-2]:
						move_string = start_sq_ind+"x"+target_sq_ind
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
						move_string = start_sq_ind+"x"+target_sq_ind
					else:
						"x"+target_sq_ind
				else:
					"x"+target_sq_ind


	elif Piece.King in piece:
		castled = False
		if special_turn is not None:
			if SpecialTurn.CastlingLong in special_turn:
				castled = True
				move_string = "O-O-O"
			elif SpecialTurn.CastlingShort in special_turn:
				move_string = "O-O"
				castled = True
		
		if not castled:
			if Piece.Empty not in b.square[target_sq]:
				move_string = "Kx" + target_sq_ind
			else:
				move_string = "K" + target_sq_ind

	elif Piece.Queen in piece:
		# TODO Fix ambiguatiy if two Queens where able to get here
		if Piece.Empty not in b.square[target_sq]:
			move_string = "Qx" + target_sq_ind
		else:
			move_string = "Q" + target_sq_ind

	elif Piece.Rook in piece:
		# TODO Fix ambiguatiy if two Rooks where able to get here
		if Piece.Empty not in b.square[target_sq]:
			move_string = "Rx" + target_sq_ind
		else:
			move_string = "R" + target_sq_ind

	elif Piece.Bishop in piece:
		# TODO Fix ambiguatiy if two Bishops where able to get here
		if Piece.Empty not in b.square[target_sq]:
			move_string = "Bx" + target_sq_ind
		else:
			move_string = "B" + target_sq_ind

	elif Piece.Knight in piece:
		# TODO Fix ambiguatiy if two Knight where able to get here
		if Piece.Empty not in b.square[target_sq]:
			move_string = "Nx" + target_sq_ind
		else:
			move_string = "N" + target_sq_ind

	else:
		move_string = ""

	return move_string + promotion_string + check_string

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
				# TODO Check other conditions: King not moving over check-squares
		else:
			# Short
			if b.moved_rook_white_h1:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-squares
	else:
		# Black Player
		if b.moved_king_black:
			return False
		elif long:
			if b.moved_rook_black_a8:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-squares
		else:
			# Short
			if b.moved_rook_black_h8:
				return False
			else:
				pass
				# TODO Check other conditions: King not moving over check-squares
		
	

	# TODO Proof of all the named conditions and the booleans
	pass


if __name__ == "__main__":
	main()