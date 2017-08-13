#!/usr/local/bin/python3

"""Solve sudoku puzzles"""

def xprod(A, B):
    """Cross product of elements in A and elements in B"""

    return [a + b for a in A for b in B]

# Setup grid, coordinates, and groups.
digits = "123456789"
rows = "ABCDEFGHI"
cols = digits

grid = xprod(rows, cols)

groups = ([xprod(r, cols) for r in rows]
          + [xprod(rows, c) for c in cols]
          + [xprod(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
             for cs in ('123', '456', '789')])

hoods = dict([(x, [g for g in groups if x in g]) for x in grid])
neighbors = dict([(x, set(sum(hoods[x], [])) - set([x])) for x in grid])

def solve_sudoku(game):
    """Solve the sudoku puzzle. Main function."""

    initial_state = game_state(game)
    print_game(initial_state)

    if input("Is this your game? ('Yes' or 'No'):\n\t") == 'Yes':
        solution = force(fill_game(game))
        print_game(solution)

    else:
        solve_sudoku(input("Input game values in order (left to right, top " \
                            "to bottom; '.' for empty):\n\t"))



def game_state(game):
    """Convert game input into dict of coordinates and values
    Input requires numbers to be in order from left to right, top to bottom.
    Will ignore all non-numbers or non-designated empty placeholders.
    """

    values = [x for x in game if x in digits or x in '0.*?']
    assert len(values) == 81  # check if input is a full grid
    return dict(zip(grid, values))

def fill_game(game):
    """Convert game state to a dict of square coords and possible values."""

    values = dict((sq, digits) for sq in grid)

    for sq, d in game_state(game).items():
        # If d is an invalid value of square ...
        if d in digits and not assign(sq, values, d):
            return False

    return values


def assign(sq, values, d):
    """Attempt to remove all but d from square's possible values."""

    xd = values[sq].replace(d, '')

    if all(eliminate(sq, values, di) for di in xd):
        return values

    return False

def eliminate(sq, values, d):
    """Attempt to remove d from square's possible values.
    Check for contradictions."""

    if d not in values[sq]:
        return values

    values[sq] = values[sq].replace(d, '')

    # If there are no possible values ...
    if not values[sq]:
        return False

    # If there is one possible value, check if there's a contradiction.
    elif len(values[sq]) == 1:
        h = values[sq]

        if not all(eliminate(sqi, values, h) for sqi in neighbors[sq]):
            return False

    # Check if removed d has only one place to go in a group.
    for hood in hoods[sq]:
        homes = [sqi for sqi in hood if d in values[sqi]]

        if not homes:
            return False

        elif len(homes) == 1:
            if not assign(homes[0], values, d):
                return False

    return values

def force(values):
    """For each square, for each possible value of that square, try to solve."""

    if not values:
        return False

    if all(len(values[sq]) == 1 for sq in grid):
        return values

    # Find square with the least possible values.
    n, sq = min((len(values[sq]), sq) for sq in grid if len(values[sq]) > 1)

    for d in values[sq]:
        solution = force(assign(sq, values.copy(), d))

        if not solution:
            pass
        else:
            return solution  # IT IS SOLVED.

def print_game(values):
    """Print the game grid for given values"""

    sqwidth = 1 + max(len(values[x]) for x in grid)
    line = '+'.join(['-' * (sqwidth * 3)] * 3)

    for r in rows:
        print(''.join(values[r + c].center(sqwidth) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)

if __name__ == '__main__':
    solve_sudoku(input("Input game values in order (left to right, top " \
                       "to bottom; '.' for empty):\n\t"))
