import pygame
import random
import sys

pygame.init()

# -----------------------------
# Grundeinstellungen
# -----------------------------
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MURDER")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)

# Spielzustände
SERVANT = "servant"
KING = "king"
DEAD = "dead"

state = SERVANT

# -----------------------------
# Spieler & König
# -----------------------------
player = pygame.Rect(100, 250, 40, 60)
player_speed = 4

king = pygame.Rect(500, 250, 50, 70)

# -----------------------------
# Gegner
# -----------------------------
assassin = None
assassin_dir = None
assassin_delay = 120
difficulty = 1

# -----------------------------
# Hilfsfunktionen
# -----------------------------
def draw_text(text, y):
    t = font.render(text, True, WHITE)
    screen.blit(t, (WIDTH // 2 - t.get_width() // 2, y))

def spawn_assassin():
    global assassin, assassin_dir
    assassin_dir = random.choice(["left", "right"])
    x = -60 if assassin_dir == "left" else WIDTH + 60
    assassin = pygame.Rect(x, 250, 40, 60)

# -----------------------------
# Hauptloop
# -----------------------------
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mordversuch als Diener
        if state == SERVANT and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if abs(player.centerx - king.centerx) < 60:
                    state = KING
                    player.x = king.x
                    assassin = None
                    assassin_delay = 120
                    difficulty = 1
                else:
                    state = DEAD

        # Abwehr als König
        if state == KING and event.type == pygame.KEYDOWN and assassin:
            if event.key == pygame.K_a and assassin_dir == "left":
                assassin = None
                difficulty += 1
                assassin_delay = max(25, 90 - difficulty * 5)

            if event.key == pygame.K_d and assassin_dir == "right":
                assassin = None
                difficulty += 1
                assassin_delay = max(25, 90 - difficulty * 5)

    keys = pygame.key.get_pressed()

    # -----------------------------
    # Spielzustände
    # -----------------------------
    if state == SERVANT:
        if keys[pygame.K_LEFT]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player.x += player_speed

        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, RED, king)
        draw_text("Schleiche zum König und drücke LEERTASTE", 40)

    elif state == KING:
        pygame.draw.rect(screen, GREEN, player)
        draw_text(f"Du bist König! Schwierigkeit: {difficulty}", 30)
        draw_text("A = links abwehren | D = rechts abwehren", 60)

        assassin_delay -= 1
        if assassin_delay <= 0 and assassin is None:
            spawn_assassin()

        if assassin:
            speed = (5 + difficulty * 1.2)
            speed = speed if assassin_dir == "left" else -speed
            assassin.x += speed
            pygame.draw.rect(screen, RED, assassin)

            if assassin.colliderect(player):
                state = DEAD

    elif state == DEAD:
        draw_text("DU BIST TOT", 150)
        draw_text("ESC zum Beenden", 190)

    pygame.display.flip()

    if keys[pygame.K_ESCAPE]:
        running = False

pygame.quit()
sys.exit()
