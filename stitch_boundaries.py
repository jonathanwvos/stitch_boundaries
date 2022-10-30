class StitchBoundary:
    class ConstraintNotSatisfiedError(Exception): pass
    X_CONSTRAINT = 2
    Y_CONSTRAINT = 2
    SUTURE_CONSTRAINT = 1

    def __init__(self, x_0: int, y_0: int, x_diff: int, y_diff: int, suture_len: int):
        if x_diff < self.X_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(f'x_diff must be greater than {self.X_CONSTRAINT}')
        if y_diff < self.Y_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(f'y_diff must be greater than {self.Y_CONSTRAINT}')
        if suture_len < self.SUTURE_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(f'suture_len must be greater than {self.SUTURE_CONSTRAINT}')

        self.x_0 = x_0
        self.y_0 = y_0
        self.x_diff = x_diff
        self.y_diff = y_diff
        self.suture_len = suture_len

        self._init_sutures()

    def _init_sutures(self):
        self.sutures = []

        # UPPER AND LOWER BOUNDARIES
        for i in range(self.x_0+2, self.x_0+self.x_diff-1):
            lower_boundary = [[i, self.y_0], [i, self.y_0+1]]
            upper_boundary = [[i, self.y_0+self.y_diff], [i, self.y_0+self.y_diff-1]]

            self.sutures.append(lower_boundary)
            self.sutures.append(upper_boundary)

        # LEFT AND RIGHT BOUNDARIES
        for j in range(self.y_0+2, self.y_0+self.y_diff-1):
            left_boundary = [[self.x_0, j], [self.x_0+1, j]]
            right_boundary = [[self.x_0+self.x_diff, j], [self.x_0+self.x_diff-1, j]]
            self.sutures.append(left_boundary)
            self.sutures.append(right_boundary)


class TStitchBoundary(StitchBoundary):
    X_CONSTRAINT = 1
    Y_CONSTRAINT = 1


class XStitchBoundary(StitchBoundary):
    def _init_diagonals(self):
        self.sutures.append([[self.x_0, self.y_0], [self.x_0+1, self.y_0+1]])
        self.sutures.append([[self.x_0+self.x_diff, self.y_0], [self.x_0+self.x_diff-1, self.y_0+1]])
        self.sutures.append([[self.x_0, self.y_0+self.y_diff], [self.x_0+1, self.y_0+self.y_diff-1]])
        self.sutures.append([[self.x_0+self.x_diff, self.y_0+self.y_diff], [self.x_0+self.x_diff-1, self.y_0+self.y_diff-1]])

    def _init_sutures(self):
        super()._init_sutures()
        self._init_diagonals()
