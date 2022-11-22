from matplotlib.collections import LineCollection
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np


class StitchBoundary:
    class ConstraintNotSatisfiedError(Exception): pass

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

    def _upper_lower_iter(self):
        raise NotImplementedError

    def _left_right_iter(self):
        raise NotImplementedError

    def _init_sutures(self):
        self.sutures = []

        # UPPER AND LOWER BOUNDARIES
        for i in self._upper_lower_iter():
            self.sutures.append([
                [i, self.y_0],
                [i, self.y_0+self.suture_len]
            ])
            self.sutures.append([
                [i, self.y_0+self.height],
                [i, self.y_0+self.height-self.suture_len]
            ])

        # LEFT AND RIGHT BOUNDARIES
        for j in self._left_right_iter():
            self.sutures.append([
                [self.x_0, j],
                [self.x_0+self.suture_len, j]
            ])
            self.sutures.append([
                [self.x_0+self.width, j],
                [self.x_0+self.width-self.suture_len, j]
            ])

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


class PStitchBoundary(StitchBoundary):
    X_CONSTRAINT = 2
    Y_CONSTRAINT = 2

    def _upper_lower_iter(self):
        start = self.x_0+self.X_CONSTRAINT-1
        end = self.x_0+self.width-self.X_CONSTRAINT+2

        for i in range(start, end):
            yield i

    def _left_right_iter(self):
        start = self.y_0+self.Y_CONSTRAINT-1
        end = self.y_0+self.height-self.Y_CONSTRAINT+2

        for j in range(start, end):
            yield j


class XStitchBoundary(StitchBoundary):
    def _upper_lower_iter(self):
        start = self.x_0+self.X_CONSTRAINT
        end = self.x_0+self.width-self.X_CONSTRAINT+1

        for i in range(start, end):
            yield i

    def _left_right_iter(self):
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


def parse_cli_args():
    parser = ArgumentParser()

    parser.add_argument(
        '-x',
        type=int,
        help='The initial X coordinate.',
        default=0
    )
    parser.add_argument(
        '-y',
        type=int,
        help='The initial Y coordinate.',
        default=0
    )
    parser.add_argument(
        '--height',
        type=int,
        help='The height of the stitch boundary.',
        default=StitchBoundary.Y_CONSTRAINT
    )
    parser.add_argument(
        '--width',
        type=int,
        help='The width of the stitch boundary.',
        default=StitchBoundary.X_CONSTRAINT
    )
    parser.add_argument(
        '--suture-len',
        type=int,
        help='The length of the sutures in the stitch boundary.',
        default=StitchBoundary.SUTURE_CONSTRAINT
    )
    parser.add_argument(
        '--type',
        type=str,
        help='The type of stitch boundary to make.',
        choices=['x', '+'],
        required=True
    )
    parser.add_argument('--grid', action='store_true', dest='grid')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_cli_args()
    params = {
        'x_0': args.x,
        'y_0': args.y,
        'width': args.width,
        'height': args.height,
        'suture_len': args.suture_len
    }

    if args.type == 'x':
        stitch_boundary = XStitchBoundary(**params)
    elif args.type == '+':
        stitch_boundary = PStitchBoundary(**params)

    stitch_boundary.visualize(grid=args.grid)
