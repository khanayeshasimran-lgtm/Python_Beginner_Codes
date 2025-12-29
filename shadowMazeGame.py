import random
import os
import time

WIDTH = 21
HEIGHT = 21
VISION_RADIUS = 2

PLAYER = "@"
WALL = "█"
FLOOR = "."
UNKNOWN = "?"
TRAP = "T"
EXIT = "E"

health = 5


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def generate_maze():
    maze = [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]

    x, y = 1, 1
    maze[y][x] = FLOOR
    stack = [(x, y)]

    while stack:
        x, y = stack.pop()
        directions = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < WIDTH-1 and 1 <= ny < HEIGHT-1:
                if maze[ny][nx] == WALL:
                    maze[y + dy//2][x + dx//2] = FLOOR
                    maze[ny][nx] = FLOOR
                    stack.append((nx, ny))

    return maze


def place_items(maze):
    empty = [(x, y) for y in range(HEIGHT) for x in range(WIDTH) if maze[y][x] == FLOOR]

    traps = random.sample(empty, 6)
    for x, y in traps:
        maze[y][x] = TRAP

    exit_pos = random.choice(empty)
    maze[exit_pos[1]][exit_pos[0]] = EXIT

    return exit_pos


def render(maze, px, py):
    clear()
    print(f"❤️ Health: {health}\n")

    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if abs(px - x) <= VISION_RADIUS and abs(py - y) <= VISION_RADIUS:
                if (x, y) == (px, py):
                    row += PLAYER
                else:
                    row += maze[y][x]
            else:
                row += UNKNOWN
        print(row)


def game():
    global health

    maze = generate_maze()
    exit_pos = place_items(maze)

    px, py = 1, 1

    while True:
        render(maze, px, py)

        move = input("\nMove (WASD) | Q to quit: ").lower()

        if move == "q":
            break

        dx, dy = 0, 0
        if move == "w": dy = -1
        elif move == "s": dy = 1
        elif move == "a": dx = -1
        elif move == "d": dx = 1
        else:
            continue

        nx, ny = px + dx, py + dy

        if maze[ny][nx] == WALL:
            continue

        px, py = nx, ny

        if maze[py][px] == TRAP:
            health -= 1
            maze[py][px] = FLOOR
            print("\n💥 You stepped on a trap!")
            time.sleep(1)

        if (px, py) == exit_pos:
            render(maze, px, py)
            print("\n🎉 You escaped the Shadow Maze!")
            break

        if health <= 0:
            render(maze, px, py)
            print("\n☠️ You died in the maze.")
            break


if __name__ == "__main__":
    game()
