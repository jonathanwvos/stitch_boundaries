from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np

class StitchBoundary:
    class ConstraintNotSatisfiedError(Exception): pass
    X_CONSTRAINT = 2
    Y_CONSTRAINT = 2
    SUTURE_CONSTRAINT = 1

    def __init__(self, x_0: int, y_0: int, width: int, height: int, suture_len: int):
        if width < self.X_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(f'width must be greater than {self.X_CONSTRAINT}')
        if height < self.Y_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(f'height must be greater than {self.Y_CONSTRAINT}')
        if suture_len < self.SUTURE_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(f'suture_len must be greater than {self.SUTURE_CONSTRAINT}')

        self.x_0 = x_0
        self.y_0 = y_0
        self.width = width
        self.height = height
        self.suture_len = suture_len

        self._init_sutures()

    def _init_sutures(self):
        self.sutures = []

        # UPPER AND LOWER BOUNDARIES
        for i in range(self.x_0+2, self.x_0+self.width-1):
            lower_boundary = [[i, self.y_0], [i, self.y_0+1]]
            upper_boundary = [[i, self.y_0+self.height], [i, self.y_0+self.height-1]]

            self.sutures.append(lower_boundary)
            self.sutures.append(upper_boundary)

        # LEFT AND RIGHT BOUNDARIES
        for j in range(self.y_0+2, self.y_0+self.height-1):
            left_boundary = [[self.x_0, j], [self.x_0+1, j]]
            right_boundary = [[self.x_0+self.width, j], [self.x_0+self.width-1, j]]
            self.sutures.append(left_boundary)
            self.sutures.append(right_boundary)

    def visualize(self, grid=False):

        sutures = np.array(self.sutures)

        lc = LineCollection(sutures, colors='black')

        fig, ax = plt.subplots()

        # Add line segments
        ax.add_collection(lc)
        ax.autoscale()

        # Add points
        xy = sutures[:, 0]
        uv = sutures[:, 1]
        x = xy[:, 0]
        y = xy[:, 1]
        u = uv[:, 0]
        v = uv[:, 1]

        ax.scatter(x, y, c='black')
        ax.scatter(u, v, c='black')

        if grid:
            ax.grid()

        plt.show()


class TStitchBoundary(StitchBoundary):
    X_CONSTRAINT = 2
    Y_CONSTRAINT = 2


class XStitchBoundary(StitchBoundary):
    def _init_diagonals(self):
        self.sutures.append([[self.x_0, self.y_0], [self.x_0+1, self.y_0+1]])
        self.sutures.append([[self.x_0+self.width, self.y_0], [self.x_0+self.width-1, self.y_0+1]])
        self.sutures.append([[self.x_0, self.y_0+self.height], [self.x_0+1, self.y_0+self.height-1]])
        self.sutures.append([[self.x_0+self.width, self.y_0+self.height], [self.x_0+self.width-1, self.y_0+self.height-1]])

    def _init_sutures(self):
        super()._init_sutures()
        self._init_diagonals()
