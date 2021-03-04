from enum import Flag, auto

class Piece(Flag):
	"This class represents a piece and its colour"
	Empty = auto()
	King = auto()
	Pawn = auto()
	Knight = auto()
	Bishop = auto()
	Rook = auto()
	Queen = auto()

	White = auto()
	Black = auto()