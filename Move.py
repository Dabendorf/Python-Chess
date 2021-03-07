class Move:
	start_square = -1
	target_square = -1
	notation = ""
	special_turn = None

	def __init__(self, sq, ts, notation, special_turn = None):
		self.start_square = sq
		self.target_square = ts
		self.notation = notation
		self.special_turn = special_turn

	def __repr__(self):
		if self.notation != "":
			return self.notation
		else:
			return str(self.start_square)+"-"+str(self.target_square)

	def __eq__(self, other):
		return self.notation == other.notation