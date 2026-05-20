import pygame
import random

def frogger_play():  # <-- The single master function for your menu hub
    """Runs a complete 1-Player Frogger/Street Crosser game."""
    
    # --- 1. CONFIGURATION ---
    WIDTH, HEIGHT = 600, 600
    TILE_SIZE = 40  # Everything moves on a perfect 40x40 pixel grid

    COLOR_BLACK  = (15, 15, 15)
    COLOR_GREEN  = (50, 220, 50)
    COLOR_RED    = (255, 50, 50)
    COLOR_WHITE  = (255, 255, 255)
    COLOR_BLUE   = (30, 144, 255)
    COLOR_GREY   = (60, 60, 60)
    COLOR_YELLOW = (230, 230, 0)

    # --- 2. GAME VARIABLES ---
    # Frog position (Starts at bottom center)
    frog_x = WIDTH // 2 - TILE_SIZE // 2
    frog_y = HEIGHT - TILE_SIZE
    
    score = 0
    lives = 3
    game_over = False
    victory = False

    # --- 3. GENERATING THE TRAFFIC LANES ---
    # We define 5 dangerous road rows. Each row has its own speed, direction, and car positions.
    # Structure: {'y_position': int, 'speed': int, 'direction': 1 or -1, 'cars': [x_positions]}
    lanes = [
        {'y': 120, 'speed': 4, 'dir': 1,  'cars': [40, 240, 440], 'color': COLOR_RED},
        {'y': 200, 'speed': 3, 'dir': -1, 'cars': [100, 350, 500], 'color': COLOR_YELLOW},
        {'y': 280, 'speed': 5, 'dir': 1,  'cars': [0, 300], 'color': COLOR_BLUE},
        {'y': 360, 'speed': 2, 'dir': -1, 'cars': [80, 280, 480], 'color': COLOR_RED},
        {'y': 440, 'speed': 4, 'dir': 1,  'cars': [150, 400], 'color': COLOR_YELLOW}
    ]
    CAR_WIDTH = 60
    CAR_HEIGHT = 30

    # --- 4. NESTED INTERNAL FUNCTIONS ---
    def reset_frog():
        """Sends the frog back to the safe starting line."""
        nonlocal frog_x, frog_y
        frog_x = WIDTH // 2 - TILE_SIZE // 2
        frog_y = HEIGHT - TILE_SIZE

    def handle_traffic_movement():
        """Scrolls all cars across the lanes and loops them around the edges."""
        for lane in lanes:
            for i in range(len(lane['cars'])):
                # Move the car based on its direction and speed
                lane['cars'][i] += lane['speed'] * lane['dir']
                
                # If a car goes completely off screen to the right, wrap it around to the left
                if lane['dir'] == 1 and lane['cars'][i] > WIDTH:
                    lane['cars'][i] = -CAR_WIDTH
                # If a car goes completely off screen to the left, wrap it around to the right
                elif lane['dir'] == -1 and lane['cars'][i] < -CAR_WIDTH:
                    lane['cars'][i] = WIDTH

    def check_collisions():
        """Checks if the frog's bounding box overlaps with any active vehicle."""
        nonlocal lives, game_over
        frog_rect = pygame.Rect(frog_x, frog_y, TILE_SIZE, TILE_SIZE)

        for lane in lanes:
            for car_x in lane['cars']:
                # Create a rectangle for each car on the fly
                car_rect = pygame.Rect(car_x, lane['y'] + 5, CAR_WIDTH, CAR_HEIGHT)
                
                if frog_rect.colliderect(car_rect):
                    lives -= 1
                    print(f"Ouch! Hit by a car. Lives left: {lives}")
                    if lives <= 0:
                        game_over = True
                    else:
                        reset_frog()
                    return

    def draw_frogger_stage(screen):
        """Renders the safe zones, road grid lines, moving cars, and the frog."""
        screen.fill(COLOR_BLACK)

        # Draw Top Safety Goal Zone
        pygame.draw.rect(screen, COLOR_GREEN, (0, 0, WIDTH, 80))
        # Draw Bottom Starting Safe Zone
        pygame.draw.rect(screen, COLOR_GREEN, (0, HEIGHT - TILE_SIZE, WIDTH, TILE_SIZE))

        # Draw Road Lanes background (Grey stripes)
        for lane in lanes:
            pygame.draw.rect(screen, COLOR_GREY, (0, lane['y'], WIDTH, TILE_SIZE))

        # Draw Moving Cars
        for lane in lanes:
            for car_x in lane['cars']:
                pygame.draw.rect(screen, lane['color'], (car_x, lane['y'] + 5, CAR_WIDTH, CAR_HEIGHT), border_radius=5)

        # Draw Player Frog (A happy little bright green square)
        pygame.draw.rect(screen, COLOR_WHITE, (frog_x, frog_y, TILE_SIZE, TILE_SIZE), border_radius=4)
        pygame.draw.rect(screen, (0, 180, 0), (frog_x + 4, frog_y + 4, TILE_SIZE - 8, TILE_SIZE - 8), border_radius=2)

        # HUD Text Display
        font = pygame.font.SysFont("Courier", 24, bold=True)
        hud_surface = font.render(f"SCORE: {score}  LIVES: {lives}", True, COLOR_WHITE)
        screen.blit(hud_surface, (15, 25))
        
        pygame.display.flip()

    # --- 5. ENGINE RUNTIME EXECUTION ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Frogger Crosser Arcade")
    clock = pygame.time.Clock()

    active_loop = True
    while active_loop:
        clock.tick(60)

        # 1. Event Handling (Using KEYDOWN for strict, one-hop-per-click movement)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active_loop = False
                
            elif event.type == pygame.KEYDOWN and not game_over and not victory:
                if event.key in [pygame.K_UP, pygame.K_w] and frog_y > 0:
                    frog_y -= TILE_SIZE
                    score += 10  # Reward moving forward!
                elif event.key in [pygame.K_DOWN, pygame.K_s] and frog_y < HEIGHT - TILE_SIZE:
                    frog_y += TILE_SIZE
                    score -= 10  # Deduct if they retreat
                elif event.key in [pygame.K_LEFT, pygame.K_a] and frog_x > 0:
                    frog_x -= TILE_SIZE
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and frog_x < WIDTH - TILE_SIZE:
                    frog_x += TILE_SIZE

        # 2. Game Logic Updates
        if not game_over and not victory:
            handle_traffic_movement()
            check_collisions()

            # Win Condition Check: Did the frog reach the top green zone?
            if frog_y <= 40:
                score += 500  # Big victory bonus!
                victory = True

        # 3. Rendering Phase
        draw_frogger_stage(screen)

        # 4. End State Exits
        if game_over:
            print(f"Game Over! Squished. Final Score: {score}")
            active_loop = False
        elif victory:
            print(f"Victory! You crossed safely! Total Score: {score}")
            active_loop = False

    pygame.quit()
    print("Exited Frogger. Returning to Main Menu...")

