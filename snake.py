import pygame
import random

# --- 1. SETUP AND GRID CONFIGURATION ---
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 30  # Each grid square is 30x30 pixels

COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)   # Snake Head/Body
COLOR_RED   = (255, 0, 0)   # Apple/Food
COLOR_WHITE = (255, 255, 255)

# --- 2. INITIALIZING DATA STRUCTURES ---
def create_snake():
    """
    Creates the starting snake.
    Represented as a list of coordinate blocks: [X, Y].
    The first element index [0] is ALWAYS the head.
    """
    return [
        [10, 10], # Head
        [9, 10],  # Body segment 1
        [8, 10]   # Body segment 2
    ]

def spawn_food(snake_body):
    """Picks a random grid position for the food that isn't inside the snake."""
    cols_limit = WIDTH // GRID_SIZE
    rows_limit = HEIGHT // GRID_SIZE
    
    while True:
        food_pos = [random.randint(0, cols_limit - 1), random.randint(0, rows_limit - 1)]
        # Make sure the food didn't spawn on top of the snake's body
        if food_pos not in snake_body:
            return food_pos

# --- 3. MOVEMENT & GAME REASONING ---
def calculate_next_head(snake_body, direction):
    """Takes the current head position and applies the direction math."""
    current_head = snake_body[0]
    dir_x = direction[0]
    dir_y = direction[1]
    
    # Calculate next grid coordinate position
    new_head = [current_head[0] + dir_x, current_head[1] + dir_y]
    return new_head

def check_self_collision(snake_body, new_head):
    """Checks if the snake ran into its own tail segments."""
    # If the new head coordinate matches any coordinate already in the body list
    if new_head in snake_body:
        return True
    return False

def check_wall_collision(new_head):
    """Checks if the head stepped past the screen boundaries."""
    cols_limit = WIDTH // GRID_SIZE
    rows_limit = HEIGHT // GRID_SIZE
    
    if new_head[0] < 0 or new_head[0] >= cols_limit:
        return True
    if new_head[1] < 0 or new_head[1] >= rows_limit:
        return True
    return False

# --- 4. GRAPHICS AND RENDERING ---
def draw_game(screen, snake_body, food, score):
    """Clears the screen and draws objects block-by-block based on grid positions."""
    screen.fill(COLOR_BLACK)

    # Draw Snake segments
    for segment in snake_body:
        pixel_x = segment[0] * GRID_SIZE
        pixel_y = segment[1] * GRID_SIZE
        # Draw snake square
        rect = pygame.Rect(pixel_x, pixel_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, COLOR_GREEN, rect)
        # Draw a dark frame border around segments so you can see joints
        pygame.draw.rect(screen, (0, 100, 0), rect, 1)

    # Draw Food Apple
    food_pixel_x = food[0] * GRID_SIZE
    food_pixel_y = food[1] * GRID_SIZE
    pygame.draw.rect(screen, COLOR_RED, (food_pixel_x, food_pixel_y, GRID_SIZE, GRID_SIZE))

    # Score Text Render
    font = pygame.font.SysFont("Arial", 24)
    score_surface = font.render("SCORE: " + str(score), True, COLOR_WHITE)
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()

# --- 5. MAIN ENGINE LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Modular Snake")
    
    # Initializing variables
    snake_body = create_snake()
    food = spawn_food(snake_body)
    
    # Starting direction: right [X movement=1, Y movement=0]
    direction = [1, 0] 
    
    score = 0
    game_running = True
    
    # Movement clock timers (keeps the snake ticking step-by-step)
    move_timer = 0
    move_delay = 150 # Snake takes 1 step every 150 milliseconds
    clock = pygame.time.Clock()

    while game_running:
        dt = clock.tick(60) # Run system tick checks at 60 FPS
        move_timer += dt

        # --- Handle User Inputs Keyboard ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                
            elif event.type == pygame.KEYDOWN:
                # We check direction checks so players cannot turn directly backward into themselves
                if event.key == pygame.K_LEFT and direction[0] != 1:
                    direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and direction[0] != -1:
                    direction = [1, 0]
                elif event.key == pygame.K_UP and direction[1] != 1:
                    direction = [0, -1]
                elif event.key == pygame.K_DOWN and direction[1] != -1:
                    direction = [0, 1]

        # --- Timed Movement Logic Updates ---
        if move_timer >= move_delay:
            move_timer = 0 # Reset delay timer
            
            # Predict where the head goes next
            next_head = calculate_next_head(snake_body, direction)
            
            # Check for failures before performing list shifting updates
            if check_wall_collision(next_head) or check_self_collision(snake_body, next_head):
                print("Game Over! Final Score:", score)
                game_running = False
            else:
                # Add the new head to the front of our list structure
                snake_body.insert(0, next_head)
                
                # Check if we ate the apple food piece
                if next_head == food:
                    score += 10
                    food = spawn_food(snake_body) # Make a new food block
                    # Note: We DO NOT pop the tail here! That's how the snake gets longer.
                else:
                    # Pop/remove the last element of the list tail to simulate standard crawl forward
                    snake_body.pop()

        # --- Render Display ---
        draw_game(screen, snake_body, food, score)

    pygame.quit()

# Run the program directly
main()