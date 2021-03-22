import Board
from Piece import Piece
from Move import Move
from SpecialTurn import SpecialTurn
import pygame
import random

from copy import copy, deepcopy

def main():
	b = Board.Board()
	to_move = Piece.White
	num_squares_to_edge = [[]]
	all_moves = []

	#pygame setup
	pygame.init()
	screen = pygame.display.set_mode((700,700))
	pygame.display.set_caption("Pythonic Chess")
	screen.fill((60,60,60))
	draw(b,screen)
	pygame.display.update()
	pygame.display.flip()
	pygame.mixer.pre_init(44100, -16, 2, 2048)

	p1 = Piece.Pawn | Piece.Black
	p2 = Piece.Empty

	num_squares_to_edge = compute_margin_to_edge()
	print("Possible moves: "+str(all_possible_turns_player(to_move, b, all_moves)))
	# thats a temporary test structure for some example moves
	
	moves_to_do_list = [(14, 22), (52, 36), (5, 14)]

	#Attention this test-loop is now used ad the pygame-mainloop
	#Further changes here need to be well thought through
	"""for st, tg in moves_to_do_list:
		#Event-Loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		
		print("Turn "+get_move_notation(b.square[st], st, tg, b)+" legal: "+str(move(st, tg, b, all_moves, to_move, num_squares_to_edge)))
		b.print_board()
		draw(b,screen)
		pygame.display.update()

		# Source: https://github.com/ornicar/lila/tree/38bfadac3e319516341771086e8edc594d4d4b07/public/sound
		pygame.mixer.init()
		pygame.mixer.music.load('files/turn.ogg')
		pygame.mixer.music.play()

		
		to_move = get_other_colour(to_move)
		
		print("========")
		num_squares_to_edge = compute_margin_to_edge()
		print("Possible moves: "+str(all_possible_turns_player(to_move, b, all_moves, num_squares_to_edge)))

		#NextFrameSetUp
		pygame.display.flip()
		screen.fill((60,60,60))
		pygame.time.wait(3000)"""

	print(all_possible_turns_player_ai(to_move, b, all_moves, 3))



def is_legal(piece: Piece):
	pass


def all_possible_turns_piece(start_sq: int, all_moves: [Move], b: Board) -> [Move]:
	piece = b.square[start_sq]
	moves = []

	if is_sliding_piece(piece):
		moves.extend(generate_sliding_moves(start_sq, piece, b))
	elif Piece.King in piece:
		moves.extend(generate_king_moves(start_sq, piece, b))
	elif Piece.Pawn in piece:
		moves.extend(generate_pawn_moves(start_sq, piece, b, all_moves))
	elif Piece.Knight in piece:
		moves.extend(generate_knight_moves(start_sq, piece, b))

	return moves


def all_possible_turns_player_ai(player_to_move: Piece, b: Board, all_moves: [Move], depth: int) -> int:
	"""Experimental function for potential ai player"""

	if depth == 0:
		return 1

	move_list = all_possible_turns_player(player_to_move, deepcopy(b), deepcopy(all_moves))

	if len(all_moves) > 0:
		print("Zugmenge "+str(depth)+"|"+str(player_to_move)+": "+str(all_moves[-1])+";"+str(len(move_list))+str(move_list))
	else:
		print("Zugmenge "+str(depth)+"|"+str(player_to_move)+": "+str(len(move_list))+str(move_list))

	count = 0
	for move2 in move_list:
		board_copy = deepcopy(b)
		all_moves_copy = deepcopy(all_moves)
		
		move(move2.start_square, move2.target_square, board_copy, deepcopy(all_moves), player_to_move, move2.special_turn)
		
		count += all_possible_turns_player_ai(get_other_colour(player_to_move), board_copy, deepcopy(all_moves), depth-1)
	
	return count


def all_possible_turns_player(player_to_move: Piece, b: Board, all_moves: [Move]) -> [Move]:
	# for every piece, if colour of player to move
	# if own piece in way, change searching direction
	# if opponent's piece in way, capture it, then change direction

	moves = []

	for i in range(0, 64):
		if(is_same_colour(b.square[i], player_to_move)):
			if is_sliding_piece(b.square[i]):
				moves.extend(generate_sliding_moves(i, b.square[i], b))
			elif Piece.King in b.square[i]:
				moves.extend(generate_king_moves(i, b.square[i], b))
			elif Piece.Pawn in b.square[i]:
				moves.extend(generate_pawn_moves(i, b.square[i], b, all_moves))
			elif Piece.Knight in b.square[i]:
				moves.extend(generate_knight_moves(i, b.square[i], b))

	return moves


def generate_sliding_moves(start_sq: int, piece: Piece, b: Board) -> [Move]:
	"""Generates moves for Rooks, Bishops and Queens"""

	num_squares_to_edge = compute_margin_to_edge()
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

			moves.append(Move(start_sq, target_sq, get_move_notation(piece, start_sq, target_sq, b)))

			if is_different_colour(piece, target_sq_piece):
				break

	return moves

			
def generate_king_moves(start_sq: int, piece: Piece, b: Board) -> [Move]:
	"""Generates moves for Kings"""
	moves = []

	dire = [-7, -8, -9, -1, 1, 7, 8, 9]
	for i in dire:
		if not is_check(b, piece):
			target_sq = start_sq+i
			if target_sq > -1 and target_sq < 64:
				if not is_same_colour(piece, b.square[target_sq]):
					moves.append(Move(start_sq, target_sq, get_move_notation(piece, start_sq, target_sq, b)))

	if castle(piece, True, deepcopy(b)):
		moves.append(Move(start_sq, start_sq-2, get_move_notation(piece, start_sq, start_sq-2, b), special_turn=SpecialTurn.CastlingLong))
	if castle(piece, False, deepcopy(b)):
		moves.append(Move(start_sq, start_sq+2, get_move_notation(piece, start_sq, start_sq+2, b), special_turn=SpecialTurn.CastlingShort))

	return moves


def generate_pawn_moves(start_sq: int, piece: Piece, b: Board, all_moves: [Move]) -> [Move]:
	"""Generates moves for Pawns"""
	moves = []

	promo_list = [SpecialTurn.PromoteQueen, SpecialTurn.PromoteRook, SpecialTurn.PromoteBishop, SpecialTurn.PromoteKnight]

	# print(str(start_sq)+str(piece))
	if Piece.White in piece:
		if start_sq//8 == 1:
			if Piece.Empty in b.square[start_sq+8] and Piece.Empty in b.square[start_sq+16]:
				moves.append(Move(start_sq, start_sq+16, get_move_notation(piece, start_sq, start_sq+16, b)))
		
		# checks if promotion
		# This is in fact highly redundant, but we did not find something better yet
		if start_sq//8 == 6:
			if Piece.Empty in b.square[start_sq+8]:
				for promo in promo_list:
					moves.append(Move(start_sq, start_sq+8, get_move_notation(piece, start_sq, start_sq+8, b, special_turn=promo), special_turn=promo))

			if start_sq % 8 != 0:
				if is_different_colour(piece, b.square[start_sq+7]):
					for promo in promo_list:
						moves.append(Move(start_sq, start_sq+7, get_move_notation(piece, start_sq, start_sq+7, b, special_turn=promo), special_turn=promo))

			if start_sq % 8 != 7:
				if is_different_colour(piece, b.square[start_sq+9]):
					for promo in promo_list:
						moves.append(Move(start_sq, start_sq+9, get_move_notation(piece, start_sq, start_sq+9, b, special_turn=promo), special_turn=promo))
		else:
			if Piece.Empty in b.square[start_sq+8]:
				moves.append(Move(start_sq, start_sq+8, get_move_notation(piece, start_sq, start_sq+8, b)))

			if start_sq % 8 != 0:
				if is_different_colour(piece, b.square[start_sq+7]):
					moves.append(Move(start_sq, start_sq+7, get_move_notation(piece, start_sq, start_sq+7, b)))

			if start_sq % 8 != 7:
				if is_different_colour(piece, b.square[start_sq+9]):
					moves.append(Move(start_sq, start_sq+9, get_move_notation(piece, start_sq, start_sq+9, b)))

	else:
		if start_sq//8 == 6:
			if Piece.Empty in b.square[start_sq-8] and Piece.Empty in b.square[start_sq-16]:
				moves.append(Move(start_sq, start_sq-16, get_move_notation(piece, start_sq, start_sq-16, b)))
		
		# if promotion
		if start_sq//8 == 1:
			if Piece.Empty in b.square[start_sq-8]:
				for promo in promo_list:
					moves.append(Move(start_sq, start_sq-8, get_move_notation(piece, start_sq, start_sq-8, b, special_turn=promo), special_turn=promo))

			if start_sq % 8 != 0:
				if is_different_colour(piece, b.square[start_sq-9]):
					for promo in promo_list:
						moves.append(Move(start_sq, start_sq-9, get_move_notation(piece, start_sq, start_sq-9, b, special_turn=promo), special_turn=promo))

			if start_sq % 8 != 7:
				if is_different_colour(piece, b.square[start_sq-7]):
					for promo in promo_list:
						moves.append(Move(start_sq, start_sq-7, get_move_notation(piece, start_sq, start_sq-7, b, special_turn=promo), special_turn=promo))
		else:
			if Piece.Empty in b.square[start_sq-8]:
				moves.append(Move(start_sq, start_sq-8, get_move_notation(piece, start_sq, start_sq-8, b)))

			if start_sq % 8 != 0:
				if is_different_colour(piece, b.square[start_sq-9]):
					moves.append(Move(start_sq, start_sq-9, get_move_notation(piece, start_sq, start_sq-9, b)))

			if start_sq % 8 != 7:
				if is_different_colour(piece, b.square[start_sq-7]):
					moves.append(Move(start_sq, start_sq-7, get_move_notation(piece, start_sq, start_sq-7, b)))

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
						moves.append(Move(start_sq, start_sq+9, get_move_notation(piece, start_sq, start_sq+9, b)))
					# En passante from right
					elif start_sq-1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq+7, get_move_notation(piece, start_sq, start_sq+7, b)))
				# Black
				else:
					# En passante from left
					if start_sq+1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq-7, get_move_notation(piece, start_sq, start_sq-7, b)))
					# En passante from right
					elif start_sq-1 == last_move.target_square:
						moves.append(Move(start_sq, start_sq-9, get_move_notation(piece, start_sq, start_sq-9, b)))

	return moves


def generate_knight_moves(start_sq: int, piece: Piece, b: Board) -> [Move]:
	"""Generates moves for Knights"""
	moves = []

	# Up
	if start_sq % 8 != 0 and start_sq//8 < 6:
		if not is_same_colour(piece, b.square[start_sq+15]):
			moves.append(Move(start_sq, start_sq+15, get_move_notation(piece, start_sq, start_sq+15, b)))
	if start_sq % 8 != 7 and start_sq//8 < 6:
		if not is_same_colour(piece, b.square[start_sq+17]):
			moves.append(Move(start_sq, start_sq+17, get_move_notation(piece, start_sq, start_sq+17, b)))

	# Right
	if start_sq % 8 < 6 and start_sq//8 != 7:
		if not is_same_colour(piece, b.square[start_sq+10]):
			moves.append(Move(start_sq, start_sq+10, get_move_notation(piece, start_sq, start_sq+10, b)))
	if start_sq % 8 < 6 and start_sq//8 != 0:
		if not is_same_colour(piece, b.square[start_sq-6]):
			moves.append(Move(start_sq, start_sq-6, get_move_notation(piece, start_sq, start_sq-6, b)))

	# Down
	if start_sq % 8 != 0 and start_sq//8 > 1:
		if not is_same_colour(piece, b.square[start_sq-17]):
			moves.append(Move(start_sq, start_sq-17, get_move_notation(piece, start_sq, start_sq-17, b)))
	if start_sq % 8 != 7 and start_sq//8 > 1:
		if not is_same_colour(piece, b.square[start_sq-15]):
			moves.append(Move(start_sq, start_sq-15, get_move_notation(piece, start_sq, start_sq-15, b)))

	# Left
	if start_sq % 8 > 1 and start_sq//8 != 0:
		if not is_same_colour(piece, b.square[start_sq-10]):
			moves.append(Move(start_sq, start_sq-10, get_move_notation(piece, start_sq, start_sq-10, b)))
	if start_sq % 8 > 1 and start_sq//8 != 7:
		if not is_same_colour(piece, b.square[start_sq+6]):
			moves.append(Move(start_sq, start_sq+6, get_move_notation(piece, start_sq, start_sq+6, b)))
	
	return moves


def is_check(b: Board, colour: Piece) -> bool:
	king_pos = -1
	for ind in range(0,64):
		if Piece.King in b.square[ind] and colour in b.square[ind]:
			king_pos = ind

	for ind in range(0,64):
		if Piece.Empty not in b.square[ind] and Piece.King not in b.square[ind]:
			poss_moves_piece = all_possible_turns_piece(ind, [], b)
			for move in poss_moves_piece:
				if move.target_square == king_pos:
					return True


def is_checkmate(b: Board) -> bool:
	pass


def move(start_sq, target_sq, b: Board, all_moves: [Move], to_move: Piece, special_turn: SpecialTurn = None) -> bool:
	"""Makes a move on the board, returns bool if successfull (false=illegal)"""

	if to_move not in b.square[start_sq]:
		return False

	if special_turn == None:
		new_move = Move(start_sq, target_sq, get_move_notation(b.square[start_sq], start_sq, target_sq, b))
	else:
		new_move = Move(start_sq, target_sq, get_move_notation(b.square[start_sq], start_sq, target_sq, b, special_turn=special_turn), special_turn=special_turn)

	poss_moves = all_possible_turns_piece(start_sq, deepcopy(all_moves), deepcopy(b))
	
	if new_move in poss_moves:
		if special_turn == SpecialTurn.CastlingShort:
			if Piece.White in to_move:
				b.square[4] = Piece.Empty
				b.square[5] = Piece.White | Piece.Rook
				b.square[6] = Piece.White | Piece.King
				b.square[7] = Piece.Empty
			else:
				b.square[60] = Piece.Empty
				b.square[61] = Piece.Black | Piece.Rook
				b.square[62] = Piece.Black | Piece.King
				b.square[63] = Piece.Empty
		elif special_turn == SpecialTurn.CastlingLong:
			if Piece.White in to_move:
				b.square[0] = Piece.Empty
				b.square[2] = Piece.White | Piece.King
				b.square[3] = Piece.White | Piece.Rook
				b.square[4] = Piece.Empty
			else:
				b.square[56] = Piece.Empty
				b.square[58] = Piece.Black | Piece.King
				b.square[59] = Piece.Black | Piece.Rook
				b.square[60] = Piece.Empty


		all_moves.append(new_move)
		b.square[target_sq] = b.square[start_sq]
		b.square[start_sq] = Piece.Empty

		if Piece.Rook in to_move:
			if start_sq==0:
				b.moved_rook_white_a1 = True
			elif start_sq==7:
				b.moved_rook_black_a8 = True
			elif start_sq==56:
				b.moved_rook_black_a8 = True
			elif start_sq==63:
				b.moved_rook_black_h8 = True

		if target_sq == 0:
			b.moved_rook_white_a1 = True
		elif target_sq==7:
				b.moved_rook_black_a8 = True
		elif target_sq==56:
				b.moved_rook_black_a8 = True
		elif target_sq==63:
				b.moved_rook_black_h8 = True

		if Piece.King in to_move:
			if Piece.White in to_move:
				b.moved_king_white = True
			else:
				b.moved_king_black = True

	colour = Piece.Empty
	if Piece.White in b.square[target_sq]:
		colour = Piece.White
	elif Piece.Black in b.square[target_sq]:
		colour = Piece.Black

	if special_turn != None:
		if SpecialTurn.PromoteQueen in special_turn:
			b.square[target_sq] = Piece.Queen | colour
		elif SpecialTurn.PromoteRook in special_turn:
			b.square[target_sq] = Piece.Rook | colour
		elif SpecialTurn.PromoteBishop in special_turn:
			b.square[target_sq] = Piece.Bishop | colour
		elif SpecialTurn.PromoteKnight in special_turn:
			b.square[target_sq] = Piece.Knight | colour
		

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

	if Piece.Empty in piece1 or Piece.Empty in piece2:
		return False

	if Piece.White in piece1 and Piece.White in piece2:
		return True
	elif Piece.Black in piece1 and Piece.Black in piece2:
		return True
	else:
		return False


def is_different_colour(piece1: Piece, piece2: Piece):
	""" For two pieces, function returns if both pieces are different
		Pay attention for the fact that this is not the opposite of same_colour as it is possible to be Piece.Empty"""

	if Piece.Empty in piece1 or Piece.Empty in piece2:
		return False

	if Piece.White in piece1 and Piece.Black in piece2:
		return True
	elif Piece.Black in piece1 and Piece.White in piece2:
		return True
	else:
		return False


def is_sliding_piece(piece: Piece):
	""" Rooks, Bishops and Queens share some properties, function returns if piece is one of them"""

	return Piece.Rook in piece or Piece.Bishop in piece or Piece.Queen in piece


def get_move_notation(piece: Piece, start_sq: int, target_sq: int, b: Board, special_turn: SpecialTurn = None, is_check : bool = False, is_checkmate = False) -> str:
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
						move_string = "x"+target_sq_ind
				else:
					move_string = "x"+target_sq_ind
			# Capture to the right
			else:
				# Edge on the right
				if (start_sq % 8) != 6:
					# If other pawn was able to do it
					if Piece.Pawn in b.square[start_sq+2]:
						move_string = start_sq_ind+"x"+target_sq_ind
					else:
						move_string = "x"+target_sq_ind
				else:
					move_string = "x"+target_sq_ind


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


def castle(player_to_move: Piece, long: bool, b: Board) -> bool:
	"""Proves if castling is possible"""

	# King and Rook did not move yet
	# No other piece between King and Rook
	# King not in check, not moving over check squares, not ending in check

	if is_check(b, player_to_move):
		return False

	if Piece.White in player_to_move:
		if b.moved_king_white:
			return False

		if long:
			if b.moved_rook_white_a1:
				return False
			else:
				if Piece.Empty not in b.square[1] or Piece.Empty not in b.square[2] or Piece.Empty not in b.square[3]:
					return False
				b_copy1 = deepcopy(b)
				b_copy1.square[3] = Piece.King | Piece.White
				if is_check(b_copy1, player_to_move):
					return False
				b_copy2 = deepcopy(b)
				b_copy2.square[2] = Piece.King | Piece.White
				if is_check(b_copy2, player_to_move):
					return False
				
				return True

		else:
			if b.moved_rook_white_h1:
				return False
			else:
				if Piece.Empty not in b.square[5] or Piece.Empty not in b.square[6]:
					return False
				b_copy1 = deepcopy(b)
				b_copy1.square[5] = Piece.King | Piece.White
				if is_check(b_copy1, player_to_move):
					return False
				b_copy2 = deepcopy(b)
				b_copy2.square[6] = Piece.King | Piece.White
				if is_check(b_copy2, player_to_move):
					return False
				
				return True
	else:
		if b.moved_king_black:
			return False

		if long:
			if b.moved_rook_black_a8:
				return False
			else:
				if Piece.Empty not in b.square[57] or Piece.Empty not in b.square[58] or Piece.Empty not in b.square[59]:
					return False
				b_copy1 = deepcopy(b)
				b_copy1.square[59] = Piece.King | Piece.Black
				if is_check(b_copy1, player_to_move):
					return False
				b_copy2 = deepcopy(b)
				b_copy2.square[58] = Piece.King | Piece.Black
				if is_check(b_copy2, player_to_move):
					return False
				
				return True
		else:
			if b.moved_rook_black_h8:
				return False
			else:
				if Piece.Empty not in b.square[61] or Piece.Empty not in b.square[62]:
					return False
				b_copy1 = deepcopy(b)
				b_copy1.square[61] = Piece.King | Piece.Black
				if is_check(b_copy1, player_to_move):
					return False
				b_copy2 = deepcopy(b)
				b_copy2.square[62] = Piece.King | Piece.Black
				if is_check(b_copy2, player_to_move):
					return False
				
				return True


def draw(board, screen):
	"""This method draws the board as designed"""
	xsize = screen.get_height()//8
	ysize = screen.get_width()//8
	off = 5 #offset between singel squares
	font = pygame.font.Font(None, 42)
	for i in range(8):
		for j in range(8):
			val = 255*((i+j+1)%2)
			colour = (val,val,val)
			rect = pygame.Rect(xsize*j+off,ysize*i+off,xsize-off,ysize-off)
			pygame.draw.rect(screen, colour, rect)

			text = font.render(Board.piece_to_letter(board.square[((7-i)*8)+(j)]),1, (90, 90, 90))
			textpos = text.get_rect()
			textpos.centerx = rect.centerx
			textpos.centery = rect.centery
			screen.blit(text, textpos)


def get_other_colour(piece: Piece) -> Piece:
	""" Returns the person who isn't in charge of doing the next turn"""

	if Piece.White in piece:
		return Piece.Black
	else:
		return Piece.White

	

if __name__ == "__main__":
	main()