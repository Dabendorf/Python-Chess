from enum import Flag, auto

class Piece(Flag):
	"This class represents a piece and its colour"
	Empty = 0
	King = auto()
	Pawn = auto()
	Knight = auto()
	Bishop = auto()
	Rook = auto()
	Queen = auto()

	White = auto()
	Black = auto()