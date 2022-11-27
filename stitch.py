from argparse import ArgumentParser
from stitch_bands import XStitchBand, PStitchBand
from stitch_boundaries import PStitchBoundary, XStitchBoundary


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
        default=2
    )
    parser.add_argument(
        '--width',
        type=int,
        help='The width of the stitch boundary.',
        default=2
    )
    parser.add_argument(
        '-sl',
        '--suture-len',
        type=int,
        help='The length of the sutures in the stitch boundary.',
        default=1
    )
    parser.add_argument('--grid', action='store_true', dest='grid')
    parser.add_argument(
        '-v',
        '--variant',
        type=str,
        help='The variant of stitch object to make.',
        choices=['x', '+'],
        required=True
    )
    
    subparsers = parser.add_subparsers(dest='type')
    band_parser = subparsers.add_parser('band')
    band_parser.add_argument(
        '-o',
        '--orientation',
        help='The orientation of the orthogonal stitches.',
        choices=['positive', 'negative', '+', '-'],
        default='+'
    )
    boundary_parser = subparsers.add_parser('boundary')

    return parser.parse_args()


DISPATCHER = {
    'band': {
        'x': XStitchBand,
        '+': PStitchBand
    },
    'boundary': {
        'x': XStitchBoundary,
        '+': PStitchBoundary
    }
}


def params(args):
    type = args.type
    
    params = {
        'x_0': args.x,
        'y_0': args.y,
        'width': args.width,
        'height': args.height,
        'suture_len': args.suture_len
    }

    if type == 'band':
        params['orientation'] = args.orientation

    return params


if __name__ == '__main__':
    args = parse_cli_args()
    type = args.type
    variant = args.variant

    params = params(args)
    # params = {
    #     'x_0': args.x,
    #     'y_0': args.y,
    #     'width': args.width,
    #     'height': args.height,
    #     'suture_len': args.suture_len
    # }

    # if type == 'band':
    #     params['orientation'] = args.orientation

    stitch = DISPATCHER[type][variant](**params)

    # stitch.visualize(grid=args.grid)