import pygame
import random

# --- 1. CONFIGURATION AND SETTINGS ---
# Defining colors based on ID numbers
COLORS = {
    0: (20, 20, 20),      # Dark gray background
    1: (255, 0, 0),       # Red (Z-shape)
    2: (0, 255, 0),       # Green (S-shape)
    3: (0, 0, 255),       # Blue (J-shape)
    4: (255, 165, 0),     # Orange (L-shape)
    5: (0, 255, 255),     # Cyan (I-shape)
    6: (255, 255, 0),     # Yellow (O-shape)
    7: (128, 0, 128)      # Purple (T-shape)
}

BLOCK_SIZE = 30  # Size of each square block in pixels
COLS = 10        # Grid width
ROWS = 20        # Grid height

# --- 2. BOARD INITIALIZATION ---
def create_empty_board():
    """Creates a 20x10 grid filled with 0s (empty spaces)."""
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(0)
        board.append(row)
    return board

# --- 3. SHAPE DEFINITIONS ---
def get_shapes_list():
    """Returns a list of all Tetris blocks, defined by numbers."""
    return [
        [[1, 1, 0], [0, 1, 1]], # Z
        [[0, 2, 2], [2, 2, 0]], # S
        [[3, 0, 0], [3, 3, 3]], # J
        [[0, 0, 4], [4, 4, 4]], # L
        [[5, 5, 5, 5]],         # I
        [[6, 6], [6, 6]],       # O
        [[0, 7, 0], [7, 7, 7]]  # T
    ]

def spawn_new_piece(shapes):
    """Picks a random shape and places it at the top-center of the board."""
    shape = random.choice(shapes)
    return {
        'matrix': shape,
        'row': 0,
        'col': COLS // 2 - len(shape[0]) // 2
    }

# --- 4. MOVEMENT & COLLISION LOGIC ---
def check_collision(board, piece, offset_row, offset_col):
    """
    Checks if a piece will hit the wall, floor, or another block.
    Loops through the shape grid using simple range numbers.
    """
    shape_matrix = piece['matrix']
    for r in range(len(shape_matrix)):
        for c in range(len(shape_matrix[r])):
            val = shape_matrix[r][c]
            if val != 0:
                next_r = piece['row'] + r + offset_row
                next_c = piece['col'] + c + offset_col
                
                # Check walls and floor boundaries
                if next_c < 0 or next_c >= COLS or next_r >= ROWS:
                    return True
                # Check if the grid cell is already occupied
                if next_r >= 0 and board[next_r][next_c] != 0:
                    return True
    return False

def lock_piece_to_board(board, piece):
    """Transfers the falling piece's numbers permanently into the board grid."""
    shape_matrix = piece['matrix']
    for r in range(len(shape_matrix)):
        for c in range(len(shape_matrix[r])):
            val = shape_matrix[r][c]
            if val != 0:
                board[piece['row'] + r][piece['col'] + c] = val

def rotate_matrix(matrix):
    """
    Rotates a 2D array 90 degrees clockwise manually.
    No advanced zip tricks here—just rebuilding it step-by-step.
    """
    total_rows = len(matrix)
    total_cols = len(matrix[0])
    
    # Create a fresh, empty matrix with swapped dimensions
    new_matrix = []
    for c in range(total_cols):
        new_row = []
        for r in range(total_rows):
            new_row.append(0)
        new_matrix.append(new_row)
        
    # Rearrange the numbers into their rotated positions
    for r in range(total_rows):
        for c in range(total_cols):
            new_matrix[c][total_rows - 1 - r] = matrix[r][c]
            
    return new_matrix

def try_rotate(board, piece):
    """Attempts to rotate the piece, but reverts if it causes a collision."""
    old_matrix = piece['matrix']
    piece['matrix'] = rotate_matrix(piece['matrix'])
    if check_collision(board, piece, 0, 0):
        piece['matrix'] = old_matrix # Undo rotation if it hits something

# --- 5. LINE CLEARING ---
def clear_full_lines(board):
    """Scans the board array row by row. If a row has no 0s, it deletes it."""
    new_board = []
    lines_cleared = 0
    
    for r in range(ROWS):
        # Check if 0 is in the row. If 0 is NOT there, the line is perfectly full!
        row_has_empty_space = False
        for c in range(COLS):
            if board[r][c] == 0:
                row_has_empty_space = True
        
        if row_has_empty_space:
            # Keep this line, copy it over
            new_board.append(board[r])
        else:
            # Skip this line (deletes it)
            lines_cleared += 1
            
    # Re-add fresh empty rows at the top to replace deleted ones
    for i in range(lines_cleared):
        empty_row = []
        for c in range(COLS):
            empty_row.append(0)
        new_board.insert(0, empty_row)
        
    return new_board, lines_cleared

# --- 6. GRAPHICS AND DRAWING ---
def draw_grid_cells(screen, board, current_piece):
    """
    The core rendering loop. Goes through the 2D arrays cell by cell 
    and draws squares on the screen based on the ID numbers found.
    """
    # Create a temporary copy of the board to overlay the active falling piece
    display_grid = []
    for r in range(ROWS):
        row_copy = []
        for c in range(COLS):
            row_copy.append(board[r][c])
        display_grid.append(row_copy)
    
    # Overlay the active piece onto our temporary display grid
    p_mat = current_piece['matrix']
    for r in range(len(p_mat)):
        for c in range(len(p_mat[r])):
            if p_mat[r][c] != 0:
                display_grid[current_piece['row'] + r][current_piece['col'] + c] = p_mat[r][c]

    # Loop through the grid row by row, column by column to draw the final pixels
    for r in range(ROWS):
        for c in range(COLS):
            cell_value = display_grid[r][c]
            color = COLORS[cell_value]
            
            # Draw the square block
            rect = pygame.Rect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, color, rect)
            # Draw a subtle border around blocks so you can see individual tiles
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

# --- 7. MAIN GAME LOOP ---
def tmain():
    pygame.init()
    screen = pygame.display.set_mode((COLS * BLOCK_SIZE, ROWS * BLOCK_SIZE))
    pygame.display.set_caption("Modular Array Tetris")
    clock = pygame.time.Clock()
    
    # Initialize data structures
    board = create_empty_board()
    shapes = get_shapes_list()
    current_piece = spawn_new_piece(shapes)
    
    game_over = False
    fall_time = 0
    fall_speed = 500 # Game ticks down every 500ms
    
    while not game_over:
        dt = clock.tick(60) # Run at 60 FPS
        fall_time += dt
        
        # --- Handle Inputs ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, current_piece, 0, -1):
                        current_piece['col'] -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, current_piece, 0, 1):
                        current_piece['col'] += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, current_piece, 1, 0):
                        current_piece['row'] += 1
                elif event.key == pygame.K_UP:
                    try_rotate(board, current_piece)

        # --- Automatic Gravity Tick ---
        if fall_time >= fall_speed:
            fall_time = 0
            if not check_collision(board, current_piece, 1, 0):
                current_piece['row'] += 1
            else:
                # If it hits something underneath, lock it down
                lock_piece_to_board(board, current_piece)
                board, cleared = clear_full_lines(board)
                current_piece = spawn_new_piece(shapes)
                
                # If new piece collides immediately, it's Game Over
                if check_collision(board, current_piece, 0, 0):
                    game_over = True

        # --- Draw Screen ---
        screen.fill((0, 0, 0))
        draw_grid_cells(screen, board, current_piece)
        pygame.display.flip()

    print("Game Over! Thanks for playing.")
    pygame.quit()

# Start the game directly
tmain()