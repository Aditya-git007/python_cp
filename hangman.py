import pygame
import random
import sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Hangman"

# Colours  (R, G, B)
COL_BG = (15,15,25)
COL_GALLOWS = (200,200,200)
COL_BODY = (230,230,230)
COL_TEXT = (240,240,240)
COL_LETTER_BOX  = (40,40,60)
COL_CORRECT = (80,200,120)
COL_WRONG = (220,60,60)
COL_HINT = (160,160,200)
COL_WIN_TEXT = (80,220,120)
COL_LOSE_TEXT = (220,60,60)
COL_OVERLAY = (0,0,0,160)   # RGBA -- used on end screen

FONT_WORD = None
FONT_ALPHA = None
FONT_UI = None

FONT_WORD_SIZE = 42
FONT_ALPHA_SIZE = 28
FONT_UI_SIZE = 24

MAX_WRONG = 6 

WORD_LIST = [
    # Animals
    "elephant", "dolphin", "penguin", "crocodile", "giraffe",
    "leopard",  "hamster", "octopus", "flamingo",  "cheetah",
    # Technology
    "keyboard", "monitor", "software", "internet", "python",
    "algorithm","compiler","database","variable", "function",
    # Countries
    "brazil",   "canada",  "germany", "nigeria",  "thailand",
    "portugal", "ukraine", "vietnam", "denmark",  "finland",
    # Sports
    "cricket",  "football","swimming","badminton","volleyball",
    "archery",  "cycling", "fencing", "handball", "lacrosse",
    # Misc
    "umbrella", "blanket", "kitchen", "library",  "student",
    "lantern",  "compass", "journey", "mystery",  "village",
]


def draw_gallows(surface, ox, oy):
    """Draw the static gallows frame."""
    color = COL_GALLOWS
    lw = 4
    #pygame.draw.line(surface, color, start_pos, end_pos, width)
    # base
    pygame.draw.line(surface, color, (ox, oy + 280), (ox + 140, oy + 280),lw)
    # vertical pole
    pygame.draw.line(surface, color, (ox + 40,oy + 280), (ox + 40,  oy),lw)
    # horizontal beam
    pygame.draw.line(surface, color, (ox + 40,oy),(ox + 140, oy),lw)
    # rope
    pygame.draw.line(surface, color, (ox + 140,oy),(ox + 140, oy + 40),lw)


def draw_body(surface, wrong_count, ox, oy):
    """Draw hangman body parts based on wrong guess count."""
    color = COL_BODY
    lw = 4
    cx = ox + 140   # centre x of the hanging figure
    head_top = oy + 40

    if wrong_count >= 1:   # head
        pygame.draw.circle(surface, color, (cx, head_top + 25), 25, lw)

    if wrong_count >= 2:   # torso
        pygame.draw.line(surface, color,
                         (cx, head_top + 50), (cx, head_top + 130), lw)

    if wrong_count >= 3:   # left arm
        pygame.draw.line(surface, color,
                         (cx, head_top + 70), (cx - 40, head_top + 110), lw)

    if wrong_count >= 4:   # right arm
        pygame.draw.line(surface, color,
                         (cx, head_top + 70), (cx + 40, head_top + 110), lw)

    if wrong_count >= 5:   # left leg
        pygame.draw.line(surface, color,
                         (cx, head_top + 130), (cx - 35, head_top + 190), lw)

    if wrong_count >= 6:   # right leg
        pygame.draw.line(surface, color,
                         (cx, head_top + 130), (cx + 35, head_top + 190), lw)


def pick_word():
    return random.choice(WORD_LIST).upper()


def build_display(word, guessed):
    """Return list of chars: letter if guessed, '_' otherwise."""
    return [ch if ch in guessed else "_" for ch in word]


def all_guessed(word, guessed):
    return all(ch in guessed for ch in word)


def draw_word_display(surface, display_chars, font, y_center):
    spacing = 38
    total_w = len(display_chars) * spacing
    start_x = (WINDOW_WIDTH - total_w) // 2

    for i, ch in enumerate(display_chars):
        x = start_x + i * spacing
        color = COL_CORRECT if ch != "_" else COL_TEXT
        letter_surf = font.render(ch, True, color)
        surface.blit(letter_surf, (x, y_center))
        # underline
        pygame.draw.line(surface, COL_HINT,
                         (x, y_center + FONT_WORD_SIZE + 4),
                         (x + 26, y_center + FONT_WORD_SIZE + 4), 2)


def draw_alphabet(surface, guessed, word, font, y_start):
    """Draw A-Z buttons coloured by state: correct / wrong / unused."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cols = 13
    box_w, box_h = 44, 38
    gap = 6
    total_w  = cols * (box_w + gap) - gap
    start_x  = (WINDOW_WIDTH - total_w) // 2

    for i, letter in enumerate(alphabet):
        col_idx = i % cols
        row_idx = i // cols
        x = start_x + col_idx * (box_w + gap)
        y = y_start + row_idx * (box_h + gap)

        if letter in guessed:
            color = COL_CORRECT if letter in word else COL_WRONG
        else:
            color = COL_LETTER_BOX

        pygame.draw.rect(surface, color, (x, y, box_w, box_h), border_radius=6)
        surf = font.render(letter, True, COL_TEXT)
        #destination_surface.blit(source_surface, (x, y))
        surface.blit(surf, surf.get_rect(center=(x + box_w // 2, y + box_h // 2)))


def draw_wrong_count(surface, wrong, font):
    txt = font.render(f"Wrong: {wrong} / {MAX_WRONG}", True, COL_HINT)
    surface.blit(txt, (WINDOW_WIDTH - txt.get_width() - 20, 20))


def draw_end_screen(surface, won, word, font_big, font_small):
    """Semi-transparent overlay with result message."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(COL_OVERLAY)
    surface.blit(overlay, (0, 0))

    if won:
        msg = "You got it!"
        color = COL_WIN_TEXT
    else:
        msg = "Game over!"
        color = COL_LOSE_TEXT

    result_surf = font_big.render(msg, True, color)
    word_surf = font_small.render(f"The word was: {word}", True, COL_TEXT)
    hint_surf = font_small.render("Press R to play again  |  Press Q to quit", True, COL_HINT)

    surface.blit(result_surf, result_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)))
    surface.blit(word_surf,word_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
    surface.blit(hint_surf,hint_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)))


class HangmanGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.word = pick_word()
        self.guessed = set()
        self.wrong_count = 0
        self.game_over = False
        self.won = False

    def guess(self, letter):
        if self.game_over or letter in self.guessed:
            return
        self.guessed.add(letter)
        if letter not in self.word:
            self.wrong_count += 1
        if self.wrong_count >= MAX_WRONG:
            self.game_over = True
            self.won = False
        elif all_guessed(self.word, self.guessed):
            self.game_over = True
            self.won = True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # fonts
    font_word = pygame.font.SysFont(FONT_WORD,FONT_WORD_SIZE,bold=True)
    font_alpha = pygame.font.SysFont(FONT_ALPHA, FONT_ALPHA_SIZE)
    font_ui = pygame.font.SysFont(FONT_UI,FONT_UI_SIZE)
    font_big = pygame.font.SysFont(FONT_UI,48, bold=True)

    game = HangmanGame()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    # accept A-Z key presses as guesses
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        game.guess(letter)

        screen.fill(COL_BG)

        # gallows + body  (top-left area)
        draw_gallows(screen, ox=60, oy=30)
        draw_body(screen, game.wrong_count, ox=60, oy=30)

        # wrong counter (top right)
        draw_wrong_count(screen, game.wrong_count, font_ui)

        # word display
        display_chars = build_display(game.word, game.guessed)
        draw_word_display(screen, display_chars, font_word, y_center=310)

        # alphabet grid
        draw_alphabet(screen, game.guessed, game.word, font_alpha, y_start=400)

        # end screen overlay
        if game.game_over:
            draw_end_screen(screen, game.won, game.word, font_big, font_ui)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()