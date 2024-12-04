import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter Game")
# Load background image

background_image = pygame.image.load("D:\Downloads\gala.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Colors
SPACE_COLOR = (135,  206, 235)          # Deep black space background
STAR_COLOR = (255,255,255)       # White stars
ASTEROID_COLOR = (44, 132, 9)     # Bright orange asteroid for visibility
PLANET_COLOR =(205, 133, 63)   # Aqua-colored planet for contrast
STARLIGHT_COLOR = (0, 0, 0)  # Light blue starlight for gun
BULLET_COLOR = (169, 66, 63)       # Yellow bullets
SCORE_COLOR = (255, 140, 0)        # Orange score and lives

# Game variables
lives = 10
score = 0
asteroid_speed = 5
bullet_speed = 10
gun_x = WIDTH // 2
gun_speed = 7
max_asteroid_speed = 15  # Set a maximum speed for the asteroid

# Asteroid settings
asteroid_x = random.randint(20, WIDTH - 20)
asteroid_y = 0
asteroid_radius = 20

# Planet settings
planet_x = random.randint(20, WIDTH - 20)
planet_y = -50  # Start above the screen
planet_radius = 30
planet_speed = 3
planet_spawn_counter = 0  # Counter for planet appearance

# Bullet list
bullets = []

# Font for displaying score and lives
font = pygame.font.Font(None, 36)

# Function to draw a starlight gun
def draw_starlight_gun(x, y):
    pygame.draw.rect(screen, STARLIGHT_COLOR, (x - 20, y, 40, 10))
    pygame.draw.circle(screen, STARLIGHT_COLOR, (x, y + 5), 15, 3)  # Starlight effect

# Function to draw a random asteroid shape
def draw_asteroid(x, y, radius):
    points = [
        (x + random.randint(-radius, radius), y + random.randint(-radius, radius)) for _ in range(6)
    ]
    pygame.draw.polygon(screen, ASTEROID_COLOR, points)

# Main game loop
running = True
while running:
    screen.fill(SPACE_COLOR)
    
    # Draw stars for the space effect
    for _ in range(30):  # Random stars on the background
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, STAR_COLOR, (star_x, star_y), 2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot a bullet from the gun's current position
                bullets.append([gun_x, HEIGHT - 30])

    # Gun movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and gun_x > 0:
        gun_x -= gun_speed
    if keys[pygame.K_RIGHT] and gun_x < WIDTH:
        gun_x += gun_speed

    # Asteroid movement
    asteroid_y += asteroid_speed
    if asteroid_y > HEIGHT:
        # Asteroid missed; reset position, lose a life, and increase speed
        asteroid_x = random.randint(20, WIDTH - 20)
        asteroid_y = 0
        lives -= 1
        asteroid_speed = min(asteroid_speed + 1, max_asteroid_speed)  # Increase speed with a cap

    # Planet movement and appearance
    planet_spawn_counter += 1
    if planet_spawn_counter > 300:  # Spawn planet every few seconds
        planet_y += planet_speed
        pygame.draw.circle(screen, PLANET_COLOR, (planet_x, planet_y), planet_radius)
        if planet_y > HEIGHT:
            # Reset planet position and counter
            planet_y = -50
            planet_x = random.randint(20, WIDTH - 20)
            planet_spawn_counter = 0

    # Bullet movement
    for bullet in bullets:
        bullet[1] -= bullet_speed  # Move bullet up
        if bullet[1] < 0:
            bullets.remove(bullet)  # Remove bullet if it goes off-screen

    # Collision detection with asteroid
    for bullet in bullets:
        if (asteroid_x - bullet[0]) ** 2 + (asteroid_y - bullet[1]) ** 2 < asteroid_radius ** 2:
            bullets.remove(bullet)
            asteroid_x = random.randint(20, WIDTH - 20)
            asteroid_y = 0
            score += 1
            break

    # Collision detection with planet
    for bullet in bullets:
        if (planet_x - bullet[0]) ** 2 + (planet_y - bullet[1]) ** 2 < planet_radius ** 2:
            bullets.remove(bullet)
            planet_y = -50
            planet_x = random.randint(20, WIDTH - 20)
            lives -= 1  # Lose a life if the planet is hit
            planet_spawn_counter = 0
            break

    # Draw the asteroid
    draw_asteroid(asteroid_x, asteroid_y, asteroid_radius)
    
    draw_starlight_gun(gun_x, HEIGHT - 20)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, bullet, 5)

    # Display lives and score
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    lives_text = font.render(f"Lives: {lives}", True, SCORE_COLOR)
    screen.blit(score_text, (WIDTH - 150, 20))
    screen.blit(lives_text, (WIDTH - 150, 50))

    # End game if lives are 0
    if lives <= 0:
        game_over_text = font.render("Game Over!", True, STAR_COLOR)
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update display and set frame rate
    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
