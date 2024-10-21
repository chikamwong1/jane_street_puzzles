import sympy as sp

def create_board_labels():
    board_labels = {}
    rows = ['1', '2', '3', '4', '5', '6']
    columns = ['a', 'b', 'c', 'd', 'e', 'f']

    for row in rows:
        for col in columns:
            position = col + row
            if row in ['1', '2']:
                if col in ['a', 'b', 'c']:
                    board_labels[position] = 'A'
                elif col in ['d', 'e']:
                    board_labels[position] = 'B'
                elif col == 'f':
                    board_labels[position] = 'C'
            elif row in ['3', '4']:
                if col in ['a', 'b']:
                    board_labels[position] = 'A'
                elif col in ['c', 'd']:
                    board_labels[position] = 'B'
                elif col in ['e', 'f']:
                    board_labels[position] = 'C'
            elif row in ['5', '6']:
                if col == 'a':
                    board_labels[position] = 'A'
                elif col in ['b', 'c']:
                    board_labels[position] = 'B'
                elif col in ['d', 'e', 'f']:
                    board_labels[position] = 'C'
    return board_labels

def get_knight_moves(position):
    col_letters = ['a', 'b', 'c', 'd', 'e', 'f']
    row_numbers = ['1', '2', '3', '4', '5', '6']
    col, row = position[0], position[1]
    x = col_letters.index(col)
    y = row_numbers.index(row)

    moves = [
        (x + 2, y + 1), (x + 2, y - 1),
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2),
        (x - 1, y + 2), (x - 1, y - 2),
    ]

    valid_moves = []
    for mx, my in moves:
        if 0 <= mx < 6 and 0 <= my < 6:
            new_col = col_letters[mx]
            new_row = row_numbers[my]
            valid_moves.append(new_col + new_row)
    return valid_moves

def dfs(current_position, end_position, path, label_sequence, expr, visited, expressions_dict, exact_length):
    if len(path) > exact_length:
        return
    if current_position == end_position:
        if len(path) == exact_length:
            simplified_expr = sp.simplify(expr)
            expr_str = str(simplified_expr)
            if expr_str in expressions_dict:
                expressions_dict[expr_str].append((path.copy(), label_sequence.copy(), path[0], path[-1]))
            else:
                expressions_dict[expr_str] = [(path.copy(), label_sequence.copy(), path[0], path[-1])]
        return
    for next_position in get_knight_moves(current_position):
        if next_position not in visited:
            next_label = board_labels[next_position]
            current_label = label_sequence[-1]
            next_symbol = label_symbols[next_label]
            if next_label == current_label:
                new_expr = expr + next_symbol
            else:
                new_expr = expr * next_symbol
            visited.add(next_position)
            path.append(next_position)
            label_sequence.append(next_label)
            dfs(
                next_position,
                end_position,
                path,
                label_sequence,
                new_expr,
                visited,
                expressions_dict,
                exact_length
            )
            visited.remove(next_position)
            path.pop()
            label_sequence.pop()

def find_paths(exact_length):
    start_positions = [('a1', 'f6'), ('a6', 'f1')]
    expressions_dict = {}

    for start_position, end_position in start_positions:
        initial_label = board_labels[start_position]
        initial_symbol = label_symbols[initial_label]
        dfs(
            current_position=start_position,
            end_position=end_position,
            path=[start_position],
            label_sequence=[initial_label],
            expr=initial_symbol,
            visited={start_position},
            expressions_dict=expressions_dict,
            exact_length=exact_length
        )
    return expressions_dict

def main():
    exact_length = 7  # Adjust as needed
    global board_labels, label_symbols
    board_labels = create_board_labels()
    A, B, C = sp.symbols('A B C')
    label_symbols = {'A': A, 'B': B, 'C': C}
    expressions_dict = find_paths(exact_length)

    if expressions_dict:
        print(f"Combined Paths of exact length {exact_length} from both trips:")
        for expr_str, paths in expressions_dict.items():
            print(f"\nSimplified Expression: {expr_str}")
            print(f"Number of Paths: {len(paths)}")
            for idx, (path, label_sequence, start_pos, end_pos) in enumerate(paths, 1):
                print(f"\nPath {idx}:")
                print(f"Start: {start_pos}, End: {end_pos}")
                for pos, label in zip(path, label_sequence):
                    print(f"  Position: {pos}, Label: {label}")
                print("\nFormatted Entry:")
                formatted_entry = ','.join(path)
                print(formatted_entry)
        print(f"\nTotal Unique Simplified Expressions: {len(expressions_dict)}")
    else:
        print(f"No paths of exact length {exact_length} found.")

if __name__ == "__main__":
    main()
