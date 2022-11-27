from stitch_boundaries import XStitchBoundary, PStitchBoundary
from numpy import arctan2, array


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

        centre_x = (x_0+width)/2
        centre_y = (y_0+height)/2

        # sutures = array(self.sutures)
        # xy = sutures[:, 0]
        # x = xy[:, 0] - centre_x
        # y = xy[:, 1] - centre_y

        # angles = arctan2(y, x)
        # print(angles)
        temp = []
        for suture in self.sutures:
            x, y = suture[0]

            temp.append({
                'suture': suture,
                'angle': arctan2(y, x)
            })

        temp = sorted(temp, key=lambda x: x['angle'])

        print(temp)


class PStitchBand(PStitchBoundary):
    pass


__all__ = ['PStitchBand', 'XStitchBand']
