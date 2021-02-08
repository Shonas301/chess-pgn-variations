import chess.pgn
import click

VARIATIONS = []


class VariationTracker(object):
    def __init__(self, initial_move_list=[]):
        self.moves = initial_move_list

    def append(self, move):
        self.moves.append(move)


class VariationVisitor(chess.pgn.BaseVisitor):
    variation_indent = ""
    main_variation = []
    variation_stack = []
    variations = []

    def visit_move(self, board, move):
        if len(self.variation_stack):
            variation = self.variation_stack.pop()
            variation.append(move)
            self.variation_stack.append(variation)
        else:
            self.main_variation.append(move)

    def begin_variation(self):
        if len(self.variation_stack) != 0:
            moves = [
                moves
                for variation in self.variation_stack
                for moves in variation.moves[:-1]
            ]
            moves = list(dict.fromkeys(moves))
        else:
            moves = self.main_variation[:-1]
        variation = VariationTracker(moves)
        self.variation_stack.append(variation)

    def end_variation(self):
        # print("end variation")
        self.variation_indent = self.variation_indent[:-2]
        variation = self.variation_stack.pop()
        VARIATIONS.append(variation)
        self.variations.append(variation)

    def result(self):
        return self.variations


def seperate_variations_from_pgn(pgn_file):
    pgn = open(pgn_file)
    while variations := chess.pgn.read_game(pgn, Visitor=VariationVisitor):
        variation_file_name = f"./{pgn_file.strip('.pgn')}_variations.pgn"
        board = chess.Board()
        for variation in variations:
            game = chess.pgn.Game()
            next_move = game.add_variation(variation.moves[0])
            for move in variation.moves[1:]:
                next_move = next_move.add_variation(move)
            print(game, file=open(variation_file_name, "a"), end="\n\n")


@click.command()
@click.argument("pgn_file", type=click.Path)
def main(pgn_file):
    seperate_variations_from_pgn(pgn_file)


if __name__ == "__main__":
    main()