import chess.pgn
import click
from copy import deepcopy

VARIATIONS = []


def traverse(node, path=[], collector=[]):
    path.append(node)
    if node.is_end():
        board = chess.Board()
        move_list = []
        for child in path:
            move_list.append(child)
        collector.append(move_list)
        # print(board.variation_san(move_list), "*\n")
        path.pop()
    else:
        for child in node.variations:
            traverse(child, path, collector=collector)
        path.pop()


def save_line(line, headers, num, file_path):
    game_line = chess.pgn.Game()
    game_line.headers = deepcopy(headers)
    game_line.headers["White"] += f"-{num}"
    game_line.headers["Black"] += f"-{num}"
    first_node = line[0]
    next_move = game_line.add_variation(first_node.move)
    next_move.comment = first_node.comment
    for move in line[1:]:
        next_move = next_move.add_variation(move.move)
        next_move.comment = move.comment
    print("?")
    print(game_line, file=open(file_path, "a"), end="\n\n")


def seperate_variations_from_pgn(pgn_file):
    pgn = open(pgn_file)
    while base_game := chess.pgn.read_game(pgn):
        for first_move in base_game.variations:
            collector = []
            traverse(first_move, [], collector=collector)
            i = 0
            variation_file_name = f"{pgn_file.strip('.pgn')}_variations.pgn"
            for line in collector:
                i += 1
                save_line(line, base_game.headers, i, variation_file_name)


@click.command()
@click.argument("pgn_file", type=click.Path(exists=True, resolve_path=True))
def main(pgn_file):
    seperate_variations_from_pgn(pgn_file)


if __name__ == "__main__":
    main()