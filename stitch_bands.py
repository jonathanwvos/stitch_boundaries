from stitch_boundaries import XStitchBoundary, PStitchBoundary
from numpy import array, pi
from math import atan2
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt


ORIENTATION = {
    'positive': False,
    '+': False,
    'negative': True,
    '-': True
}


class XStitchBand(XStitchBoundary):
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

    def visualize(self, grid=False) -> None:
        """
        Plots sutures as a collection of points
        and lines between them.
        """

        sutures = array(self.sutures)
        inner_curve = array(self.inner_curve)
        outer_curve = array(self.outer_curve)

        fig, ax = plt.subplots()

        lc = LineCollection(sutures, colors='black')
        ax.add_collection(lc)

        lc = LineCollection(inner_curve, colors='red')
        ax.add_collection(lc)

        lc = LineCollection(outer_curve, colors='blue')
        ax.add_collection(lc)

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

class PStitchBand(PStitchBoundary):
    pass


__all__ = ['PStitchBand', 'XStitchBand']
