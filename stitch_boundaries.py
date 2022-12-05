from matplotlib.collections import LineCollection
from numpy import array

import matplotlib.pyplot as plt


class StitchBoundary:
    """
    Base class for stitch boundary construct. By default it will only
    create vertical and horizontal stitches (2D). This version of the
    construct assumes positive integer lengths for the sutures and
    spacing between them.

    Sutures are represented as a series of points [[x_0, y_0], [x_1, y_1]]

    :constraint X_CONSTRAINT:       Prevents stitches from start at the
                                    zeroth or terminal locations along
                                    the horizontal.
    :constraint Y_CONSTRAINT:       Prevents stitches from start at the
                                    zeroth or terminal locations along
                                    the vertical.
    :constraint SUTURE_CONSTRAINT:  Prevents sutures from being negative
                                    and overlapping.
    """

    class ConstraintNotSatisfiedError(Exception):
        pass

    X_CONSTRAINT = 2
    Y_CONSTRAINT = 2
    SUTURE_CONSTRAINT = 1

    def __init__(
        self,
        *,
        x_0: int,
        y_0: int,
        width: int,
        height: int,
        suture_len: int
    ) -> None:
        """Construct.

        Constrains input values and initializes vertical and horizontal
        stitches according to the constraints.
        """
        if width < self.X_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(
                f'width must be greater than {self.X_CONSTRAINT}'
            )
        if height < self.Y_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(
                f'height must be greater than {self.Y_CONSTRAINT}'
            )
        if suture_len < self.SUTURE_CONSTRAINT:
            raise self.ConstraintNotSatisfiedError(
                f'suture_len must be greater than {self.SUTURE_CONSTRAINT}'
            )
        if suture_len > width/2:
            raise self.ConstraintNotSatisfiedError(
                f'suture_len ({suture_len}) must be leq half the width ({width})'
            )
        if suture_len > height/2:
            raise self.ConstraintNotSatisfiedError(
                f'suture_len ({suture_len}) must be leq half the height ({height})'
            )

        self.x_0 = x_0
        self.y_0 = y_0
        self.width = width
        self.height = height
        self.suture_len = suture_len

        self._init_sutures()

    def _north_south_iter(self) -> None:
        raise NotImplementedError

    def _west_east_iter(self) -> None:
        raise NotImplementedError

    def _init_sutures(self) -> None:
        """
        Make the basis set of sutures: North, South, West and East.
        """

        self.sutures = []

        # North and South boundaries
        for i in self._north_south_iter():
            self.sutures.append([
                [i, self.y_0],
                [i, self.y_0+self.suture_len]
            ])
            self.sutures.append([
                [i, self.y_0+self.height],
                [i, self.y_0+self.height-self.suture_len]
            ])

        # West and East boundaries
        for j in self._west_east_iter():
            self.sutures.append([
                [self.x_0, j],
                [self.x_0+self.suture_len, j]
            ])
            self.sutures.append([
                [self.x_0+self.width, j],
                [self.x_0+self.width-self.suture_len, j]
            ])

    def _add_line_segments(self, ax):
        sutures = array(self.sutures)
        lc = LineCollection(sutures, colors='black')
        ax.add_collection(lc)

    def visualize(self, grid=False) -> None:
        """
        Plots sutures as a collection of points
        and lines between them.
        """

        fig, ax = plt.subplots()

        sutures = array(self.sutures)

        # Add line segments
        self._add_line_segments(ax)

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


class PStitchBoundary(StitchBoundary):
    """
    The + variant of a stitch boundary. Does not contain
    diagonal sutures.
    """

    X_CONSTRAINT = 2
    Y_CONSTRAINT = 2

    def _north_south_iter(self):
        start = self.x_0+self.X_CONSTRAINT-1
        end = self.x_0+self.width-self.X_CONSTRAINT+2

        for i in range(start, end):
            yield i

    def _west_east_iter(self):
        start = self.y_0+self.Y_CONSTRAINT-1
        end = self.y_0+self.height-self.Y_CONSTRAINT+2

        for j in range(start, end):
            yield j


class XStitchBoundary(StitchBoundary):
    """
    The x variant of a stitch boundary. Containts diagonal
    sutures.
    """

    def _north_south_iter(self):
        start = self.x_0+self.X_CONSTRAINT
        end = self.x_0+self.width-self.X_CONSTRAINT+1

        for i in range(start, end):
            yield i

    def _west_east_iter(self):
        start = self.y_0+self.Y_CONSTRAINT
        end = self.y_0+self.height-self.Y_CONSTRAINT+1

        for j in range(start, end):
            yield j

    def _init_diagonals(self):
        self.sutures.append([
            [self.x_0, self.y_0],
            [self.x_0+self.suture_len, self.y_0+self.suture_len]
        ])
        self.sutures.append([
            [self.x_0+self.width, self.y_0],
            [self.x_0+self.width-self.suture_len, self.y_0+self.suture_len]
        ])
        self.sutures.append([
            [self.x_0, self.y_0+self.height],
            [self.x_0+self.suture_len, self.y_0+self.height-self.suture_len]
        ])
        self.sutures.append([
            [self.x_0+self.width, self.y_0+self.height],
            [self.x_0+self.width-self.suture_len, self.y_0+self.height-self.suture_len]
        ])

    def _init_sutures(self):
        super()._init_sutures()
        self._init_diagonals()


__all__ = ['PStitchBoundary', 'XStitchBoundary']
