class Move:
    start_square = -1
    target_square = -1
    notation = ""

    def __init__(self, sq, ts, notation):
        self.start_square = sq
        self.target_square = ts
        self.notation = notation

    def __repr__(self):
        if self.notation != "":
            return self.notation
        else:
            return str(self.start_square)+"-"+str(self.target_square)