def uci_to_algebraic(uci_notation):
    file_mapping = {
        'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd',
        'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h'
    }

    rank_mapping = {
        '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8'
    }

    piece_mapping = {
        'P': '', 'N': 'N', 'B': 'B', 'R': 'R',
        'Q': 'Q', 'K': 'K'
    }

    from_file = uci_notation[0]
    from_rank = uci_notation[1]
    to_file = uci_notation[2]
    to_rank = uci_notation[3]

    if len(uci_notation) == 5:
        promotion_piece = uci_notation[4]
        promotion_piece = piece_mapping[promotion_piece]

    else:
        promotion_piece = ''

    algebraic_notation = (
        piece_mapping['P'] +
        file_mapping[from_file] +
        rank_mapping[from_rank] +
        ('x' if 'x' in uci_notation else '') +
        file_mapping[to_file] +
        rank_mapping[to_rank] +
        promotion_piece
    )

    return algebraic_notation

def main():
    uci_input = input("Enter UCI notation: ")
    algebraic_output = uci_to_algebraic(uci_input)
    print("Algebraic notation: " + algebraic_output)


main()