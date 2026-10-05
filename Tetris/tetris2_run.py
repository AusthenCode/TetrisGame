import pygame
import random

#Sound setup (in try /except so missing/ broken audio device)
#never crashes the game. Small, quiet effects only.
SoundOn = True
try:
    pygame.mixer.init()
    ClearSound = pygame.mixer.Sound("Tetris/sounds/clear_line.mp3")
    PauseSound = pygame.mixer.Sound("Tetris/sounds/pause.mp3")
    ClearSound.set_volume(0.3)
    PauseSound.set_volume(0.3)
except Exception:
    SoundOn = False

def play_sound(sound):
    # Small helper so every place that wants to play
    # goes through one safe spot instead of repeating the check.
    if SoundOn:
        sound.play()
    
# Global constants - it's OK as it's read only
# code smell - why list when tuple (immutable) is OK? Use immutable objects as much as possible
Colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RAINBOW = (
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (0, 200, 0),
    (0, 100, 255),
    (148, 0, 211),
)

# code smell - why use mutable list when tuple (immutable) is OK? Use immutable objects as much as possible
Figures = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]
# Landscape window with room for the board and a controls panel.
size = (760, 620)

# ADDED: Clear 5 lines per level; finish all 3 levels to win.
MAX_LEVEL = 3
LINES_PER_LEVEL = 5
# CHANGED: Shorter drop delays make each new level noticeably faster.
# Level 1: 0.6 seconds, level 2: 0.4 seconds, level 3: 0.2 seconds.
FALL_TIMES = (600, 400, 200)

# Global variables (code smell - we should remove them by refactoring)
Type = 0
Color = 0
Rotation = 0
NextType = 0
NextColor = 1

State = "start" # "gameover" or "won" when the game ends.
Field = []

# Tetris block Height and Width
Height = 0
Width = 0
# StartX/Y position in the screen
StartX = 55
StartY = 80
# Block size
Tzoom = 25
# Shift left/right or up/down
ShiftX = 0
ShiftY = 0
Score = 0
Level = 1
Lines = 0

# code smell - global variable access, refactor to use
# parameters (if you use a function) or class fields (if you use a class)
def make_figure(x, y):
    global ShiftX, ShiftY, Type, Color, Rotation, NextType, NextColor
    ShiftX = x
    ShiftY = y
    Type = NextType
    Color = NextColor
    NextType = random.randint(0, len(Figures) - 1)
    NextColor = random.randint(1, len(Colors) - 1)
    Rotation = 0

def intersects(image):
    intersection = False
    # code smell - what is 4? Magic number
    for i in range(4):
        for j in range(4):
            if i * 4 + j in image:
                # out of bounds
                # code smell - confusing, why Y is related i and X is related j?
                if i + ShiftY > Height - 1 or \
                   j + ShiftX > Width - 1 or \
                   j + ShiftX < 0 or \
                   Field[i + ShiftY][j + ShiftX] > 0:
                       intersection = True
    return intersection

def break_lines():
    global Field, Score, Lines, Level, State
    # CHANGED: Remove full rows and add empty ones at the top.
    # This also clears the top row correctly without copying filled rows.
    remaining_rows = [row for row in Field if 0 in row]
    cleared = Height - len(remaining_rows)
    Field = [[0] * Width for _ in range(cleared)] + remaining_rows
    Score += cleared ** 2

    if cleared > 0:
        play_sound(ClearSound)

    # ADDED: Count cleared lines, increase the level, and stop at the goal.
    Lines += cleared
    Level = min(Lines // LINES_PER_LEVEL + 1, MAX_LEVEL)
    if Lines >= MAX_LEVEL * LINES_PER_LEVEL:
        State = "won"

def freeze(image):
    # code smell - can you guess what it does? why there is no comments on what it does, how, and why?
    global Field, State
    for i in range(4):
        for j in range(4):
            if i * 4 + j in image:
                Field[i + ShiftY][j + ShiftX] = Color
    break_lines()
    if State == "won": # ADDED: Do not spawn another piece after winning.
        return
    make_figure(3, 0) 
    if intersects(Figures[Type][Rotation]):
        State = "gameover"

def go_space():
    global ShiftY
    while not intersects(Figures[Type][Rotation]):
        ShiftY += 1
    ShiftY -= 1
    freeze(Figures[Type][Rotation])

def go_down():
    global ShiftY
    ShiftY += 1
    if intersects(Figures[Type][Rotation]):
        ShiftY -= 1 
        freeze(Figures[Type][Rotation])

def go_side(dx):
    global ShiftX
    old_x = ShiftX
    ShiftX += dx
    if intersects(Figures[Type][Rotation]):
        ShiftX = old_x

def rotate():
    global Rotation
    def rotate_figure():
        global Rotation
        Rotation = (Rotation + 1) % len(Figures[Type])
        
    old_rotation = Rotation
    rotate_figure()
    if intersects(Figures[Type][Rotation]):
        Rotation = old_rotation
        
def init_board():
    for i in range(Height):
        new_line = [0] * Width # polymorphism using * 
        Field.append(new_line)

def draw_board(screen, x, y, zoom):
    screen.fill(BLACK)

    for i in range(Height):
        for j in range(Width):
            pygame.draw.rect(screen, GRAY, [x + zoom * j, y + zoom * i, zoom, zoom], 1)
            if Field[i][j] > 0:
                pygame.draw.rect(screen, Colors[Field[i][j]],
                                 [x + zoom * j + 1, y + zoom * i + 1, zoom - 2, zoom - 1])

    board_width = Width * zoom
    board_height = Height * zoom
    segments = 12
    for i in range(segments):
        color = RAINBOW[i % len(RAINBOW)]
        left = x + board_width * i // segments
        right = x + board_width * (i + 1) // segments
        top = y + board_height * i // segments
        bottom = y + board_height * (i + 1) // segments
        pygame.draw.line(screen, color, (left, y - 3), (right, y - 3), 4)
        pygame.draw.line(screen, color, (left, y + board_height + 3), (right, y + board_height + 3), 4)
        pygame.draw.line(screen, color, (x - 3, top), (x - 3, bottom), 4)
        pygame.draw.line(screen, color, (x + board_width + 3, top), (x + board_width + 3, bottom), 4)

def draw_figure(screen, image, x, y, shift_x, shift_y, zoom, color):
    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in image:
                pygame.draw.rect(screen, Colors[color],
                                 [x + zoom * (j + shift_x) + 1,
                                  y + zoom * (i + shift_y) + 1,
                                  zoom - 2, zoom - 2])

def draw_next_piece(screen, image, color, left, top, zoom):
    rows = [position // 4 for position in image]
    columns = [position % 4 for position in image]
    min_row, max_row = min(rows), max(rows)
    min_column, max_column = min(columns), max(columns)
    piece_width = (max_column - min_column + 1) * zoom
    piece_height = (max_row - min_row + 1) * zoom
    padding = 10
    box_width = piece_width + padding * 2
    box_height = piece_height + padding * 2
    box = pygame.Rect(left, top, box_width, box_height)
    pygame.draw.rect(screen, GRAY, box, 2)

    figure_x = box.x + padding - min_column * zoom
    figure_y = box.y + padding - min_row * zoom
    draw_figure(screen, image, figure_x, figure_y, 0, 0, zoom, color)
            
def initialize(height, width):
    global Height, Width, Field, State, Score, Lines, Level, NextType, NextColor
    Height = height
    Width = width
    Field = []
    State = "start"
    # ADDED: Reset progress when starting or restarting.
    Score = 0
    Lines = 0
    Level = 1
    NextType = random.randint(0, len(Figures) - 1)
    NextColor = random.randint(1, len(Colors) - 1)
    # code smell - why another initializion in the initalize() function?
    init_board()

def main():
    global State
    # Pygame related init
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # CHANGED: Use milliseconds so controls and falling do not depend on FPS.
    fps = 60
    fall_timer = 0
    move_timer = 0
    font = pygame.font.SysFont('Calibri', 23, True, False)
    help_font = pygame.font.SysFont('Calibri', 20)

    initialize(20, 10)
    make_figure(3, 0)
    done = False
    while not done:
        elapsed = clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:

                # Added: Quit any time; restart after winning or losing
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    done = True
                elif event.key == pygame.K_r and State in ("gameover", "won", "paused"):
                    initialize(20, 10)
                    make_figure(3, 0)
                    fall_timer = 0
                    move_timer = 0
                elif event.key == pygame.K_p and State in ("start", "paused"):
                    State = "paused" if State == "start" else "start"
                    play_sound(PauseSound)
                elif event.key == pygame.K_m:
                    global SoundOn
                    SoundOn = not SoundOn 
                elif State == "start":
                    if event.key == pygame.K_UP:
                        rotate()
                    if event.key == pygame.K_LEFT:
                        go_side(-1)
                        move_timer = 180
                    if event.key == pygame.K_RIGHT:
                        go_side(1)
                        move_timer = 180
                    if event.key == pygame.K_SPACE:
                        go_space()
                        fall_timer = 0
        if done:
            break

        if State == "start":
            # Added: Hold left/ right to repeat, with a short initial delay.
            # Rotation and hard drop still happen only once per key press.
            keys = pygame.key.get_pressed()
            move_timer -= elapsed
            direction = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            if direction and move_timer <= 0:
                go_side(direction)
                move_timer = 90

            # CHANGED: Hold down for controlled soft drop; levels get faster.
            fall_timer += elapsed
            fall_delay = 60 if keys[pygame.K_DOWN] else FALL_TIMES[Level - 1]
            if fall_timer >= fall_delay:
                go_down()
                fall_timer = 0

        draw_board(screen = screen, x = StartX, y = StartY, zoom = Tzoom)
        
        if State == "start":
            draw_figure(screen = screen, image = Figures[Type][Rotation], x = StartX, y = StartY, shift_x = ShiftX, shift_y = ShiftY, zoom = Tzoom, color = Color)

        # Show the score above the board and keep controls in a side panel.
        text = font.render(f"Score: {Score}    Level: {Level}/{MAX_LEVEL}", True, WHITE)
        screen.blit(text, [15, 5])
        target = Level * LINES_PER_LEVEL
        text = help_font.render(f"Lines: {Lines}/{target} - Clear {LINES_PER_LEVEL} per level", True, WHITE)
        screen.blit(text, [15, 32])
        draw_next_piece(screen, Figures[NextType][0], NextColor, 322, 55, 20)
        controls_rect = pygame.Rect(350, 165, 240, 296)
        pygame.draw.rect(screen, GRAY, controls_rect, 2)
        screen.blit(font.render("CONTROLS", True, WHITE), [375, 190])
        instructions = (
            "Hold Left / Right: Move",
            "Up: Rotate",
            "P: Pause / resume",
            "Hold Down: Soft drop",
            "Space: Drop instantly",
            "Esc / Q: Quit",
            "Clear 15 lines to win!",
        )
        for i, instruction in enumerate(instructions):
            screen.blit(help_font.render(instruction, True, WHITE), [375, 235 + i * 31])

        # CHANGED: Both endings stop play and offer a simple restart.
        if State == "paused":
            title = font.render("Paused", True, WHITE)
            prompt = help_font.render("P: resume  R: restart  Esc/Q: quit", True, WHITE)
            title_rect = title.get_rect(center=(StartX + Width * Tzoom // 2, StartY + Height * Tzoom // 2 - 20))
            prompt_rect = prompt.get_rect(center=(StartX + Width * Tzoom // 2, StartY + Height * Tzoom // 2 + 20))
            screen.blit(title, title_rect)
            screen.blit(prompt, prompt_rect)
        elif State != "start":
            message = "You Win!" if State == "won" else "Game Over"
            title = font.render(message, True, WHITE)
            prompt = help_font.render("R: restart    Esc / Q: quit", True, WHITE)
            title_rect = title.get_rect(center=(StartX + Width * Tzoom // 2, StartY + Height * Tzoom // 2 - 20))
            prompt_rect = prompt.get_rect(center=(StartX + Width * Tzoom // 2, StartY + Height * Tzoom // 2 + 20))
            screen.blit(title, title_rect)
            screen.blit(prompt, prompt_rect)

        # refresh the screen
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
