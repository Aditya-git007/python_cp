import pygame
import random

def breakout_play():  # <-- The single master function for your menu hub
    """Runs a complete 1-Player Breakout/Brick Breaker game."""
    
    # --- 1. CONFIGURATION ---
    WIDTH, HEIGHT = 800, 600
    PADDLE_WIDTH, PADDLE_HEIGHT = 120, 15
    BALL_SIZE = 12
    PADDLE_SPEED = 8

    COLOR_BLACK  = (10, 10, 10)
    COLOR_WHITE  = (255, 255, 255)
    COLOR_GREY   = (150, 150, 150)
    
    # Brick Row Colors
    BRICK_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]

    # --- 2. GAME VARIABLES ---
    # Bottom Paddle Setup
    paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = HEIGHT - 50
    score = 0
    lives = 3

    # Ball Trackers
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-4, 4])
    ball_dy = -4  # Head upwards toward the bricks at the start

    # --- 3. GENERATING THE BRICK WALL GRID ---
    # 5 rows of bricks, 10 bricks per row
    BRICK_ROWS = 5
    BRICK_COLS = 10
    BRICK_WIDTH = 76
    BRICK_HEIGHT = 20
    BRICK_PADDING = 4
    OFFSET_TOP = 60
    OFFSET_LEFT = 2

    def create_brick_wall():
        wall = []
        for r in range(BRICK_ROWS):
            row_bricks = []
            for c in range(BRICK_COLS):
                # Calculate coordinates for each individual brick bounding box
                b_x = OFFSET_LEFT + c * (BRICK_WIDTH + BRICK_PADDING)
                b_y = OFFSET_TOP + r * (BRICK_HEIGHT + BRICK_PADDING)
                # Store: [pygame.Rect object, color, is_visible (True/False)]
                brick_rect = pygame.Rect(b_x, b_y, BRICK_WIDTH, BRICK_HEIGHT)
                row_bricks.append([brick_rect, BRICK_COLORS[r], True])
            wall.append(row_bricks)
        return wall

    bricks_matrix = create_brick_wall()

    # --- 4. NESTED INTERNAL FUNCTIONS ---
    def reset_ball():
        """Resets ball to center field after losing a life."""
        nonlocal ball_x, ball_y, ball_dx, ball_dy
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = random.choice([-4, 4])
        ball_dy = -4

    def handle_physics_and_collisions():
        """Manages all wall bounces, paddle deflections, and brick destruction."""
        nonlocal ball_x, ball_y, ball_dx, ball_dy, score, lives, paddle_x
        
        # Apply physical movement steps
        ball_x += ball_dx
        ball_y += ball_dy

        # Side Wall Collisions (Left & Right margins)
        if ball_x <= 0 or ball_x >= WIDTH - BALL_SIZE:
            ball_dx *= -1
            
        # Top Ceiling Collision
        if ball_y <= 0:
            ball_dy *= -1

        # Bottom Border Drop (Player missed the ball)
        if ball_y >= HEIGHT:
            lives -= 1
            if lives > 0:
                reset_ball()

        # Create bounding rectangles for calculations
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

        # Paddle Collision deflection logic
        if ball_rect.colliderect(paddle_rect) and ball_dy > 0:
            ball_dy *= -1
            # Add subtle direction changes depending on where the ball lands on the board
            paddle_center = paddle_x + PADDLE_WIDTH // 2
            ball_center = ball_x + BALL_SIZE // 2
            ball_dx = (ball_center - paddle_center) * 0.15

        # Brick Collision Grid scanning
        for row in bricks_matrix:
            for brick in row:
                brick_rect, color, is_alive = brick
                if is_alive and ball_rect.colliderect(brick_rect):
                    brick[2] = False  # Break the brick (set is_alive to False)
                    ball_dy *= -1     # Reverse vertical bounce direction
                    score += 10
                    return            # Exit loop early to handle one impact per frame

    def draw_breakout_stage(screen):
        """Renders the game board layout on screen."""
        screen.fill(COLOR_BLACK)

        # Draw Player Paddle
        pygame.draw.rect(screen, COLOR_WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        
        # Draw Ball
        pygame.draw.circle(screen, COLOR_WHITE, (int(ball_x), int(ball_y)), BALL_SIZE // 2)

        # Draw Live Bricks
        for row in bricks_matrix:
            for brick in row:
                brick_rect, color, is_alive = brick
                if is_alive:
                    pygame.draw.rect(screen, color, brick_rect)

        # HUD Displays (Score and Lives remaining)
        font = pygame.font.SysFont("Arial", 24, bold=True)
        score_surface = font.render(f"SCORE: {score}", True, COLOR_WHITE)
        lives_surface = font.render(f"LIVES: {lives}", True, COLOR_WHITE)
        
        screen.blit(score_surface, (20, 15))
        screen.blit(lives_surface, (WIDTH - 130, 15))
        pygame.display.flip()

    # --- 5. RUNTIME PYGAME WINDOW ENGINE ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout Brick Module")
    clock = pygame.time.Clock()

    game_running = True
    while game_running:
        clock.tick(60)

        # Keyboard checks for horizontal board movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle_x > 0:
            paddle_x -= PADDLE_SPEED
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += PADDLE_SPEED

        # Window closing check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Update and Draw positions
        handle_physics_and_collisions()
        draw_breakout_stage(screen)

        # Check for game ending states
        if lives <= 0:
            print(f"Game Over! Final Score: {score}")
            game_running = False
            
        # Check if all bricks are smashed (Win condition check)
        all_destroyed = True
        for row in bricks_matrix:
            for brick in row:
                if brick[2]: # If even one brick is still alive
                    all_destroyed = False
        if all_destroyed:
            print(f"Victory! Clean sweep! Score: {score}")
            game_running = False

    pygame.quit()
    print("Exited Breakout. Returning to Main Menu...")

breakout_play()