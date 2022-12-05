from math import atan2
from matplotlib.collections import LineCollection
from numpy import array
from stitch_boundaries import StitchBoundary, XStitchBoundary, PStitchBoundary

import matplotlib.pyplot as plt


ORIENTATION = {
    'positive': False,
    '+': False,
    'negative': True,
    '-': True
}


class StitchBand(StitchBoundary):
    def __init__(
        self,
        *,
        x_0: int,
        y_0: int,
        width: int,
        height: int,
        suture_len: int,
        orientation: str
    ) -> None:
        super().__init__(
            x_0=x_0,
            y_0=y_0,
            width=width,
            height=height,
            suture_len=suture_len
        )
        self.orientation = orientation
        self.inner_curve, self.outer_curve = self._init_curves()

    def _init_curves(self):
        inner_curve = []
        outer_curve = []
        centre_x = (self.x_0+self.width)/2
        centre_y = (self.y_0+self.height)/2

        temp = []
        for suture in self.sutures:
            x, y = suture[0]
            x = x - centre_x
            y = y - centre_y

            temp.append({
                'suture': suture,
                'angle': atan2(y, x)
            })

        temp = sorted(
            temp,
            key=lambda x: x['angle'],
            reverse=ORIENTATION[self.orientation]
        )

        no_points = len(temp)
        for i in range(-1, no_points-1):
            suture_i0 = temp[i]['suture']
            suture_i1 = temp[i+1]['suture']

            outer_curve.append([suture_i0[0], suture_i1[0]])
            inner_curve.append([suture_i0[1], suture_i1[1]])

        return inner_curve, outer_curve

    def _add_line_segments(self, ax):
        sutures = array(self.sutures)
        inner_curve = array(self.inner_curve)
        outer_curve = array(self.outer_curve)

        sutures_lc = LineCollection(sutures, colors='black')
        ax.add_collection(sutures_lc)

        inner_curve_lc = LineCollection(inner_curve, colors='red')
        ax.add_collection(inner_curve_lc)

        outer_curve_lc = LineCollection(outer_curve, colors='blue')
        ax.add_collection(outer_curve_lc)

    def visualize(self, grid=False) -> None:
        """
        Plots sutures as a collection of points
        and lines between them.
        """

        fig, ax = plt.subplots()

        # Add line segments
        self._add_line_segments(ax)

        # Add points
        sutures = array(self.sutures)
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


class XStitchBand(XStitchBoundary, StitchBand):
    pass


class PStitchBand(PStitchBoundary, StitchBand):
    pass


__all__ = ['PStitchBand', 'XStitchBand']
