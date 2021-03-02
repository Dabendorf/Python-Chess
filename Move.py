class Move:
    start_square = -1
    target_square = -1

    def __init__(self, sq, ts):
        self.start_square = sq
        self.target_square = ts