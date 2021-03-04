from enum import Flag, auto

class SpecialTurn(Flag):
	"This class represents a piece and its colour"
	Empty = 0
	CastlingLong = auto()
	CastlingShort = auto()
	PromoteQueen = auto()
	PromoteRook = auto()
	PromoteBishop = auto()
	PromoteKnight = auto()