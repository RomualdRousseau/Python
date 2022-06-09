import sys
import argparse
from PIL import Image

DENSITIES = [
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "@%#*+=-:. "
]

def _convert_to_ascii(img, width = 64, height = None, density = DENSITIES[0]):
    """
    This function converts an image to its ascii art counterpart. It will map the luminance value of the image
    to an ascii character with a given density. It will also scale the image to take into account the fact ascii
    character have double height verses their width.
    """

    if height == None:
        w, h = img.size
        r = h / w
        height =  int(width * r * 0.5)

    img = img.convert('L')
    img = img.resize((width, height))
    
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            l = pixels[x, y] / 255
            d = int((len(density) - 1) * l)
            print(density[d], end='')
        print()


def _parser():
    """
    This function parses the command line arguments.
    """

    my_parser = argparse.ArgumentParser(description='Convert an image to ascii art.')
    my_parser.add_argument(
            '-f', 
            '--file',
            action='store', 
            type=str, 
            required=True, 
            help='Set the image file')
    my_parser.add_argument(
            '-d', 
            '--density', 
            action='store', 
            type=int, 
            required=False,
            default=1,
            help='Set the density of the output')
    my_parser.add_argument(
            '-W',
            '--width',
            action='store',
            type=int,
            required=False,
            default=64,
            help='Set the width of the output')
    my_parser.add_argument(
            '-H',
            '--height',
            action='store',
            type=int,
            required=False,
            help='Set the height of the output')
    args = my_parser.parse_args()

    return args


def main():

    args = _parser()    

    with Image.open(args.file) as img:
        _convert_to_ascii(img, args.width, args.height, DENSITIES[args.density])


if __name__ == "__main__":
    sys.exit(main())
