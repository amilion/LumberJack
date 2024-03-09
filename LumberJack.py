import random
import curses

stdscr = curses.initscr()
curses.noecho()

level = "easy"  # the choises are 'easy', 'medium', 'hard', and 'insane'
lines = curses.LINES
cols = curses.COLS
environment_chr = " "
tree_chr = "|"
branch_chr = "_"
tree_width = 20
branch_width = 10
branch_height = 3
jack_width = 3
jack_chr = "$"

world = []
level_dict = {"easy": 40, "medium": 60, "hard": 80, "insane": 90}

start_of_tree = cols // 2 - int(tree_width / 2)
end_of_tree = cols // 2 + int(tree_width / 2)


def generate_environment():
    global world
    for row in range(lines):
        row_lst = []
        for col in range(cols):
            row_lst.append(environment_chr)
        world.append(row_lst)


def generate_tree():
    for row in range(lines):
        world[row][start_of_tree:end_of_tree] = [tree_chr] * 2 * int(tree_width / 2)


def branch_drawer(side: str, row: int):
    if side == "left":
        start_point = start_of_tree - branch_width
    elif side == "right":
        start_point = end_of_tree
    else:
        raise KeyError(f"the side {side} is not defiened!")
    for height in range(row, row + branch_height):
        for col in range(start_point, start_point + branch_width):
            world[height][col] = branch_chr


def generate_initial_branches():
    for row in range(0, lines - branch_height * 4, branch_height):
        generate_branch(row)


def generate_branch(row: int):
    prob_of_branch_generation = level_dict[level] / 100
    if prob_of_branch_generation > random.random():
        if random.random() > 0:
            if random.random() > 0.5:
                # left branch generation
                branch_drawer("left", row)
            else:
                # right branch generation
                branch_drawer("right", row)


def generate_jack(side: str):
    if side == "left":
        for row in range(lines - branch_height - 1, lines):
            for col in range(start_of_tree - jack_width - 1, start_of_tree - 1):
                world[row][col] = jack_chr
    elif side == "right":
        for row in range(lines - branch_height - 1, lines):
            for col in range(end_of_tree + 1, end_of_tree + 1 + jack_width):
                world[row][col] = jack_chr
    else:
        raise KeyError(f"the side {side} is not defiened!")


def draw_world():
    generate_environment()
    generate_tree()
    generate_initial_branches()
    generate_jack("left")
    for row in range(lines - 1):
        for col in range(cols - 1):
            stdscr.addch(row, col, world[row][col])


def main():
    stdscr.clear()

    draw_world()

    stdscr.refresh()


main()
