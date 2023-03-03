"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random, itertools

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120

difficulty = 5 # Slowing game down

# Window size
frame_size_x = 720
frame_size_y = 480
cell_size = 30

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gray = pygame.Color(25, 25, 25)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [5 * cell_size, 5 * cell_size]
snake_body = [[5 * cell_size, 5 * cell_size], [5 * cell_size - cell_size, 5 * cell_size], [5 * cell_size - (2 * cell_size), 5 * cell_size]]
food_cells = set(itertools.product(range(cell_size, frame_size_x - cell_size, cell_size), range(cell_size, frame_size_y - cell_size, cell_size)))
possible = food_cells - set([tuple(x) for x in snake_body])
food_pos = random.choice(list(possible))
food_spawn = True
direction = 'RIGHT'
horizontal_dirs = ('LEFT', 'RIGHT')
vertical_dirs = ('UP', 'DOWN')
change_to = direction
# (current direction, change to)
dir_map = {
    ('LEFT', 'LEFT'): 'DOWN',
    ('LEFT', 'RIGHT'): 'UP',
    ('RIGHT', 'LEFT'): 'UP',
    ('RIGHT', 'RIGHT'): 'DOWN',
    ('UP', 'LEFT'): 'LEFT',
    ('UP', 'RIGHT'): 'RIGHT',
    ('DOWN', 'LEFT'): 'LEFT',
    ('DOWN', 'RIGHT'): 'RIGHT'
}
score = 0

def draw():
    # Draw background:
    game_window.fill(black)

    # Draw snake:
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], cell_size, cell_size))
    
    # Draw food:
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], cell_size, cell_size))

    # Draw the grid:
    for x in range(0, frame_size_x // cell_size):
        for y in range(0, frame_size_y // cell_size):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(game_window, gray, rect, 1)

    # Draw score:
    show_score(1, red, 'times', 20)
    
    # Refresh:
    pygame.display.update()
  
# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('GAME OVER', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(0.1)
    pygame.quit()
    sys.exit()

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x // 2, 15)
    else:
        score_rect.midtop = (frame_size_x // 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update snake position:
    snake_pos = snake_body[0]
    snake_pos = (
        snake_pos[0] + int(direction == "RIGHT") * cell_size - int(direction == "LEFT") * cell_size,
        snake_pos[1] + int(direction == "DOWN") * cell_size - int(direction == "UP") * cell_size
    )
    snake_body.insert(0, list(snake_pos))
    
    draw()

    # Check for food alignment on axis
    horizontal_alignment = snake_pos[0] == food_pos[0]
    vertical_alignment = snake_pos[1] == food_pos[1]
    awaiting_input = False

    if horizontal_alignment and vertical_alignment:
        score += 1
        food_spawn = False
    else:
        # Prompt turn on food alignment
        if (horizontal_alignment and direction in horizontal_dirs) or vertical_alignment and direction in vertical_dirs:
            awaiting_input = True
        # Prompt turn to prevent wall collision
        elif (snake_pos[0] in (0, frame_size_x - cell_size) and direction in horizontal_dirs) or (snake_pos[1] in (0, frame_size_y - cell_size) and direction in vertical_dirs):
            awaiting_input = True
        snake_body.pop()
    
    # Make turns:
    while awaiting_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print('Turning Left.')
                    direction = dir_map[(direction, 'LEFT')]
                    awaiting_input = False
                elif event.key == pygame.K_RIGHT:
                    print('Turning Right.')
                    direction = dir_map[(direction, 'RIGHT')]
                    awaiting_input = False
    
    if not food_spawn:
        possible = food_cells - set([tuple(x) for x in snake_body])
        food_pos = random.choice(list(possible))
    food_spawn = True

    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - cell_size:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - cell_size:
        game_over()
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
    
    fps_controller.tick(difficulty)