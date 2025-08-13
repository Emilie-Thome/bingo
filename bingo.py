import os
import random as rand
import sys

import numpy as np

from render import TableImage


def print_help():
    """
    Prints help for command line usage.
    """
    print(
        "usage: \n\
  >> python3 bingo.py INPUT_PATH NAMES_PATH OUTPUT_DIR\n\
  with - INPUT_PATH: path to the input file containing the text of bingo cells, ONE BY LINE\n\
       - NAMES_PATH: file with the names of the people participating in the bingo\n\
       - OUTPUT_DIR: path to the output directory where cards will be generated as PNG images\n"
    )


def handle_args(args: list[str]) -> tuple[str, str, str]:
    """
    Function to handle command line arguments.

    :returns: Tuple corresponding to cells path, names path, and output directory.

    :param args: The command line arguments.
    """
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


def read_names(namepath: str) -> list[str]:
    """
    Reads players' names from names path.

    :returns: List of names, adapted to file-naming.

    :param namepath: Path to names.
    """
    with open(namepath, "r") as file:
        return [name.rstrip().replace(" ", "_") for name in file]


def get_cells(filepath: str) -> list[str]:
    """
    Gets bingo cells content from filepath.

    :returns: List of bingo cells content.

    :param filepath: Path to bingo cells.
    """
    with open(filepath) as file:
        return [cell.rstrip() for cell in file]


def generate_cards(cells: list[str], names: list[str], outdir: str):
    """
    Generates random bingo cards for each player.

    :param cells:  Path to bingo cells.
    :param names:  Players' names.
    :param outdir: Output directory.
    """
    # cards size = N*N
    cells_nb = len(cells)
    N = int(np.sqrt(cells_nb))

    # check that the number of cells makes a square card
    if N**2 != cells_nb:
        sys.exit("invalid number of bingo cells, it should be a square number")

    def random_card() -> list[list[str]]:
        """
        :returns: One random bingo card.
        """
        card = cells.copy()
        rand.shuffle(card)
        return [card[i * N : (i + 1) * N] for i in range(0, N)]

    # create folder if not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # create `.png` file for each card
    for name in names:
        image = TableImage(random_card()).draw()
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
