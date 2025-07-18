import sys
import os
import numpy as np
import random as rand


# Print help for command line usage
def print_help():
    print(
        "usage: \n\
  >> python3 bingo.py INPUT_PATH CARDS_NB OUTPUT_DIR\n\
  with - INPUT_PATH: path to the input file containing the text of bingo cells, ONE BY LINE\n\
       - CARDS_NB:   number of random cards to produce\n\
       - OUTPUT_DIR: path to the output directory where cards will be generated as csv files\n"
    )


# Function to handle command line arguments.
def handle_args(args: list[str]) -> tuple[str, int, str]:
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
            "input, number of cards, and output paths must be provided, use '-h' for help"
        )
    return (args[0], int(args[1]), args[2])


# Get bingo cells content from filepath.
def get_cells(filepath: str) -> list[str]:
    cells = []
    with open(filepath) as file:
        for cell in file:
            cells.append(cell.rstrip())
    return cells


# Generate random bingo cards.
def generate_cards(cells_nb: int, cards_nb: int) -> list[list[int]]:
    # check that the number of cells makes a square card
    if int(np.sqrt(cells_nb)) ** 2 != cells_nb:
        sys.exit("invalid number of bingo cells, it should be a square number")
    # generate random index sequences
    cards = []
    for _ in range(0, cards_nb):
        card = list(range(0, cells_nb))
        rand.shuffle(card)
        cards.append(card)
    return cards


# Generate files with bingo cards.
def print_cards(outdir: str, cards: list[list[int]], cells: list[str]):
    # create folder if not exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # cards size = N*N
    cells_nb = len(cells)
    N = int(np.sqrt(cells_nb))
    # function to get the actual cells
    into_cell = lambda indices: map(lambda index: cells[index], indices)
    # create `.csv` file for each card
    for n, card in enumerate(cards):
        with open(outdir + "/card_" + str(n) + ".csv", "w") as file:
            for i in range(0, cells_nb, N):
                file.write(",".join(into_cell(card[i : i + N])) + "\n")


def main():
    args = sys.argv[1:]
    (filepath, cards_nb, outdir) = handle_args(args)
    cells = get_cells(filepath)
    cards = generate_cards(len(cells), cards_nb)
    print_cards(outdir, cards, cells)


if __name__ == "__main__":
    main()
