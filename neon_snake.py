#!/usr/bin/env python3
"""
Neon Snake
Single-file pygame game: snake with power-ups, procedural obstacles, levels, and a local leaderboard.
Save as neon_snake.py and run: python neon_snake.py
"""

import pygame
import random
import sys
import json
from collections import deque
from pathlib import Path

# -------------------------
# Config
# -------------------------
GRID_SIZE = 20           # number of cells horizontally
CELL = 24                # pixel size of a cell
WIDTH = GRID_SIZE * CELL
HEIGHT = GRID_SIZE * CELL
FPS = 12                 # base FPS, increases with level
LEADERBOARD = Path("neon_snake_scores.json")
FONT_NAME = None         # default pygame font

# Colors (neon palette)
BG = (10, 12, 18)
GRID_COLOR = (20, 24, 30)
NEON_HEAD = (0, 252, 168)
NEON_BODY = (0, 180, 140)
FOOD_COLOR = (255, 105, 180)
POWER_COLORS = {
    "slow": (102, 153, 255),
    "reverse": (255, 176, 64),
    "shrink": (200, 100, 255)
}
OBSTACLE_COLOR = (45, 45, 50)
TEXT_COLOR = (220, 220, 230)

# Power-up durations (ms)
POWER_DURATION = 6000
POWER_SPAWN_INTERVAL = 15000  # ms
OBSTACLE_INCREASE_EVERY = 3   # levels

# -------------------------
# Utilities
# -------------------------
def load_leaderboard():
    if LEADERBOARD.exists():
        try:
            return json.loads(LEADERBOARD.read_text())
        except Exception:
            return []
    return []

def save_leaderboard(entries):
    try:
        LEADERBOARD.write_text(json.dumps(entries[:10], indent=2))
    except Exception:
        pass

# -------------------------
# Game classes
# -------------------------
class Snake:
    def __init__(self):
        mid = GRID_SIZE // 2
        self.body = deque([(mid, mid), (mid-1, mid), (mid-2, mid)])
        self.dir = (1, 0)   # moving right
        self.grow_pending = 0
        self.alive = True

    def head(self):
        return self.body[0]

    def move(self, direction_override=None):
        if direction_override is None:
            dx, dy = self.dir
        else:
            dx, dy = direction_override

        hx, hy = self.head()
        new = ((hx + dx) % GRID_SIZE, (hy + dy) % GRID_SIZE)
        # insert new head
        self.body.appendleft(new)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def set_dir(self, d):
        # prevent reversing into itself directly
        if (d[0] * -1, d[1] * -1) == self.dir and len(self.body) > 1:
            return
        self.dir = d

    def grow(self, n=1):
        self.grow_pending += n

    def shrink(self, n=2):
        # remove from tail up to n cells (but leave at least 3)
        for _ in range(n):
            if len(self.body) > 3:
                self.body.pop()

    def collides_with_self(self):
        h = self.head()
        return list(self.body).count(h) > 1

# -------------------------
# Game functions
# -------------------------
def random_empty_cell(occupied, obstacles):
    attempts = 0
    while True:
        attempts += 1
        x = random.randrange(GRID_SIZE)
        y = random.randrange(GRID_SIZE)
        if (x,y) in occupied or (x,y) in obstacles:
            continue
        return (x,y)
        if attempts > 1000:
            # fallback
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if (i,j) not in occupied and (i,j) not in obstacles:
                        return (i,j)
    return (0,0)

def draw_grid(screen):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID_COLOR, (x,0), (x,HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID_COLOR, (0,y), (WIDTH,y))

def draw_cell(screen, pos, color, border_radius=6):
    x, y = pos
    rect = pygame.Rect(x*CELL+2, y*CELL+2, CELL-4, CELL-4)
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)

def render_text(surface, text, size, pos, center=False):
    font = pygame.font.Font(FONT_NAME, size)
    text_surf = font.render(text, True, TEXT_COLOR)
    if center:
        r = text_surf.get_rect(center=pos)
        surface.blit(text_surf, r)
    else:
        surface.blit(text_surf, pos)

# -------------------------
# Main game
# -------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon Snake")
    clock = pygame.time.Clock()

    score = 0
    level = 1
    fps = FPS

    snake = Snake()
    obstacles = set()
    # create a few initial obstacles
    for _ in range(5):
        obstacles.add((random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)))

    occupied = set(snake.body) | obstacles
    food = random_empty_cell(occupied, obstacles)
    power_up = None  # (type, pos, spawn_time)
    last_power_spawn = pygame.time.get_ticks()

    power_active = None  # (type, activated_at)
    power_end_time = 0
    control_reversed = False
    slow_factor = 1.0

    running = True
    paused = False
    game_over = False

    # leaderboards
    leaderboard = load_leaderboard()

    # control mapping (normal)
    DIRS = {
        pygame.K_UP: (0,-1),
        pygame.K_DOWN: (0,1),
        pygame.K_LEFT: (-1,0),
        pygame.K_RIGHT: (1,0),
        pygame.K_w: (0,-1),
        pygame.K_s: (0,1),
        pygame.K_a: (-1,0),
        pygame.K_d: (1,0),
    }

    while running:
        dt = clock.tick(int(fps * slow_factor))
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_p:
                    paused = not paused

                if game_over:
                    if event.key == pygame.K_RETURN:
                        # restart
                        main()
                        return

                # Movement
                if event.key in DIRS and not paused and not game_over:
                    desired = DIRS[event.key]
                    # if controls reversed and a power is active, invert desired
                    if control_reversed:
                        desired = (-desired[0], -desired[1])
                    snake.set_dir(desired)

        if paused or game_over:
            # render paused / game over screen overlays
            screen.fill(BG)
            draw_grid(screen)
            render_text(screen, f"Score: {score}  Level: {level}", 18, (8,8))
            if paused:
                render_text(screen, "PAUSED - press P to resume", 28, (WIDTH//2, HEIGHT//2), center=True)
            else:
                render_text(screen, "GAME OVER", 36, (WIDTH//2, HEIGHT//2 - 20), center=True)
                render_text(screen, f"Score: {score}", 24, (WIDTH//2, HEIGHT//2 + 16), center=True)
                render_text(screen, "Press Enter to play again", 18, (WIDTH//2, HEIGHT//2 + 50), center=True)
            pygame.display.flip()
            continue

        # Handle power expiration
        if power_active and now >= power_end_time:
            # deactivate all power effects
            if power_active == "slow":
                slow_factor = 1.0
            if power_active == "reverse":
                control_reversed = False
            # shrink is instantaneous so nothing to revert
            power_active = None

        # Spawn power-ups periodically
        if power_up is None and now - last_power_spawn >= POWER_SPAWN_INTERVAL:
            ptype = random.choice(list(POWER_COLORS.keys()))
            occupied = set(snake.body) | obstacles | {food}
            pos = random_empty_cell(occupied, obstacles)
            power_up = (ptype, pos, now)
            last_power_spawn = now

        # Move snake based on current direction
        snake.move()

        # Collision checks
        if snake.collides_with_self():
            game_over = True

        # collision with obstacles
        if snake.head() in obstacles:
            game_over = True

        # Eat food
        if snake.head() == food:
            score += 10
            snake.grow(2)
            # increase speed slightly
            if score % 50 == 0:
                level += 1
                fps += 1 + level // 2
                # add obstacles every few levels
                if level % OBSTACLE_INCREASE_EVERY == 0:
                    for _ in range(level // OBSTACLE_INCREASE_EVERY + 1):
                        obstacles.add((random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)))
            occupied = set(snake.body) | obstacles
            food = random_empty_cell(occupied, obstacles)

        # Power-up pickup
        if power_up and snake.head() == power_up[1]:
            ptype = power_up[0]
            # activate
            power_active = ptype
            power_end_time = now + POWER_DURATION
            if ptype == "slow":
                slow_factor = 0.6  # game slows down
            elif ptype == "reverse":
                control_reversed = True
            elif ptype == "shrink":
                snake.shrink(3)
            power_up = None

        # power-up timeout (disappear if not picked for long)
        if power_up and now - power_up[2] > POWER_SPAWN_INTERVAL:
            power_up = None

        # Clear screen and draw
        screen.fill(BG)
        draw_grid(screen)

        # draw obstacles
        for ob in obstacles:
            draw_cell(screen, ob, OBSTACLE_COLOR, border_radius=4)

        # draw food
        draw_cell(screen, food, FOOD_COLOR, border_radius=10)

        # draw power-up
        if power_up:
            draw_cell(screen, power_up[1], POWER_COLORS.get(power_up[0], (200,200,200)), border_radius=8)
            # small label
            font = pygame.font.Font(FONT_NAME, 12)
            label = font.render(power_up[0][0].upper(), True, (10,10,10))
            rect = label.get_rect(center=(power_up[1][0]*CELL + CELL//2, power_up[1][1]*CELL + CELL//2))
            screen.blit(label, rect)

        # draw snake body (tail to head)
        body_list = list(snake.body)
        for i, b in enumerate(reversed(body_list)):  # draw tail first
            # gradient effect
            t = i / max(1, len(body_list))
            color = tuple(int(NEON_BODY[j] * (1 - t) + NEON_HEAD[j] * t) for j in range(3))
            draw_cell(screen, b, color, border_radius=8 if i==0 else 6)

        # HUD
        render_text(screen, f"Score: {score}", 18, (8, 4))
        render_text(screen, f"Level: {level}", 18, (WIDTH - 88, 4))

        # Active power indicator
        if power_active:
            remaining = max(0, (power_end_time - now) // 1000)
            render_text(screen, f"Power: {power_active} ({remaining}s)", 16, (WIDTH//2 - 70, 4))

        pygame.display.flip()

        # extra: if snake occupies entire board -> win (rare)
        if len(snake.body) >= GRID_SIZE * GRID_SIZE - len(obstacles):
            game_over = True

        # handle death: show final and write leaderboard
        if game_over:
            # add to leaderboard
            name = input_name_popup(screen, score)
            entry = {"name": name, "score": score}
            leaderboard = sorted(leaderboard + [entry], key=lambda e: e["score"], reverse=True)
            save_leaderboard(leaderboard)
            # show game over for one loop iteration (handled above)
    pygame.quit()
    sys.exit()

# -------------------------
# Input popup implemented with pygame (blocking)
# -------------------------
def input_name_popup(screen, score):
    # Simple text input handled inside pygame
    w, h = screen.get_size()
    font = pygame.font.Font(FONT_NAME, 20)
    name = ""
    clock = pygame.time.Clock()
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                return "Player"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player"
                    active = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode
        # draw popup
        screen.fill(BG)
        draw_grid(screen)
        render_text(screen, "GAME OVER", 40, (w//2, 40), center=True)
        render_text(screen, f"Score: {score}", 24, (w//2, 92), center=True)
        # input box
        box = pygame.Rect(w//2 - 160, h//2 - 20, 320, 40)
        pygame.draw.rect(screen, (30,30,40), box, border_radius=6)
        pygame.draw.rect(screen, (100,100,120), box, 2, border_radius=6)
        nm_surf = font.render(name or "Enter name...", True, TEXT_COLOR)
        screen.blit(nm_surf, (box.x + 10, box.y + 8))

        render_text(screen, "Press Enter to save score", 18, (w//2, h//2 + 60), center=True)

        # draw leaderboard (top 5)
        lb = load_leaderboard()
        render_text(screen, "Leaderboard:", 18, (20, h-140))
        for i, e in enumerate((lb[:5] if lb else [])):
            render_text(screen, f"{i+1}. {e['name']} - {e['score']}", 16, (20, h-120 + 20*i))

        pygame.display.flip()
        clock.tick(30)
    return name or "Player"

if __name__ == "__main__":
    main()
