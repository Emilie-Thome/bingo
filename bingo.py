import os
import random as rand
import sys

import numpy as np

from render import draw_table


# Print help for command line usage
def print_help():
    print(
        "usage: \n\
  >> python3 bingo.py INPUT_PATH NAMES_PATH OUTPUT_DIR\n\
  with - INPUT_PATH: path to the input file containing the text of bingo cells, ONE BY LINE\n\
       - NAMES_PATH: file with the names of the people participating in the bingo\n\
       - OUTPUT_DIR: path to the output directory where cards will be generated as PNG images\n"
    )


# Function to handle command line arguments.
def handle_args(args: list[str]) -> tuple[str, str, str]:
    # first time using this program?
    if len(args) == 0:
        sys.exit("arguments must be provided, use '-h' for help")
    # do we print help?
    if (
        args[0] == "-h"
        or args[0] == "--h"
        or args[0] == "-H"
        or args[0] == "--H"
        or args[0] == "-help"
        or args[0] == "--help"
    ):
        print_help()
        sys.exit()
    # correct number of arguments?
    if len(args) != 3:
        sys.exit(
            "input, file with names, and output paths must be provided, use '-h' for help"
        )
    return (args[0], args[1], args[2])


# Read players' names from namepath.
def read_names(namepath: str) -> list[str]:
    with open(namepath, "r") as file:
        return [name.rstrip().replace(" ", "_") for name in file]


# Get bingo cells content from filepath.
def get_cells(filepath: str) -> list[str]:
    with open(filepath) as file:
        return [cell.rstrip() for cell in file]


# Generate random bingo cards for each player.
def generate_cards(cells: list[str], names: list[str], outdir: str):
    # cards size = N*N
    cells_nb = len(cells)
    N = int(np.sqrt(cells_nb))

    # check that the number of cells makes a square card
    if N**2 != cells_nb:
        sys.exit("invalid number of bingo cells, it should be a square number")

    # one random bingo card.
    def random_card() -> list[list[str]]:
        card = cells.copy()
        rand.shuffle(card)
        return [card[i * N : (i + 1) * N] for i in range(0, N)]

    # create folder if not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # create `.png` file for each card
    for name in names:
        image = draw_table(random_card())
        image.save(os.path.join(outdir, f"{name}.png"), "PNG")


def main():
    args = sys.argv[1:]
    (filepath, namepath, outdir) = handle_args(args)
    names = read_names(namepath)
    cells = get_cells(filepath)
    print("generate cards...")
    generate_cards(cells, names, outdir)
    print("bingo!")


if __name__ == "__main__":
    main()
