from Piece import Piece

class Board:
	square : [Piece] = []
	moved_king_white = False
	moved_king_black = False
	moved_rook_white_a1 = False
	moved_rook_white_h1 = False
	moved_rook_black_a8 = False
	moved_rook_black_h8 = False

	def __init__(self):
		self.square = [Piece.Empty] * 64
		self.square[0] = Piece.White | Piece.Rook

		self.square[1] = Piece.White | Piece.Knight
		self.square[2] = Piece.White | Piece.Bishop
		self.square[3] = Piece.White | Piece.Queen
		self.square[4] = Piece.White | Piece.King
		self.square[5] = Piece.White | Piece.Bishop
		self.square[6] = Piece.White | Piece.Knight
		self.square[7] = Piece.White | Piece.Rook
		
		for i in range(8,16):
			self.square[i] = Piece.White | Piece.Pawn

		for i in range(48,56):
			self.square[i] = Piece.Black | Piece.Pawn

		self.square[56] = Piece.Black | Piece.Rook
		self.square[57] = Piece.Black | Piece.Knight
		self.square[58] = Piece.Black | Piece.Bishop
		self.square[59] = Piece.Black | Piece.Queen
		self.square[60] = Piece.Black | Piece.King
		self.square[61] = Piece.Black | Piece.Bishop
		self.square[62] = Piece.Black | Piece.Knight
		self.square[63] = Piece.Black | Piece.Rook

	def print_board(self):
		print("–"*17)
		for x in range(7,-1,-1):
			print("|", end="")
			for y in range(0,8):
				print(piece_to_letter(self.square[8*x+y]), end="")
				print("|", end="")
			print("")
			print("–"*17)

	def __copy__(self):
		newone = type(self)()
		newone.__dict__.update(self.__dict__)
		return newone


def piece_to_letter_colourless(piece: Piece):
	letter_dict = {Piece.Rook : "r", Piece.Knight : "n", Piece.Bishop : "b", Piece.Queen: "q", Piece.King : "k", Piece.Pawn : "p", Piece.Empty : " "}

	for key, value in letter_dict.items():
		if key in piece:
			return value

def piece_to_letter(piece: Piece):
	if Piece.White in piece:
		return piece_to_letter_colourless(piece).upper()
	elif Piece.Black in piece:
		return piece_to_letter_colourless(piece)
	else:
		return piece_to_letter_colourless(piece)
