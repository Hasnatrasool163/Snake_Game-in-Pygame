#To allow moving between colors using arrow keys inside the shop and to add more colors, we need to make some modifications to the code. Here's the updated version:


import pygame
import random,os,sys


# Initialize Pygame
pygame.init()
pygame.mixer.init()

# FUNCTION ADDED TO MAKE EXE FILE USING PYINSTALLER AND TO ADD IMAGES SAFELY
# root.wm_overrideredirect(True)
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running as a script, use the current working directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# Load sound effect
eating_sound = pygame.mixer.Sound(resource_path('food.wav')) 
end_sound = pygame.mixer.Sound(resource_path('gameover.wav')) 
# Set up the game window
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Snake initial position and size
BLOCK_SIZE = 20
player_snake = {
    'pos': [(WIDTH / 2, HEIGHT / 2)],
    'direction': (1, 0),
    'color': GREEN,
    'growth': 0
}

# Foods
foods = []

# Single food variable
food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
        random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

# Coins
coins = 0

# Font initialization
font = pygame.font.Font(None, 36)

# Set up the clock to control the game speed
clock = pygame.time.Clock()

# Start screen
start_screen = pygame.image.load(resource_path('snake_background.jpg'))  # Load start screen image
start_screen = pygame.transform.scale(start_screen, (WIDTH, HEIGHT))

# Game background
game_background = pygame.image.load(resource_path('back1.png'))  # Load game background image
game_background = pygame.transform.scale(game_background, (WIDTH, HEIGHT))

# Shop button
shop_button = pygame.image.load(resource_path('button.jpg'))  # Load shop button image
shop_button = pygame.transform.scale(shop_button, (100, 50))

# Shop screen
shop_screen = pygame.image.load(resource_path('back2.png'))  # Load shop screen image
shop_screen = pygame.transform.scale(shop_screen, (WIDTH, HEIGHT))

# Available snake colors in the shop
shop_colors = [RED, BLUE, YELLOW, PURPLE, ORANGE]

# Visual indicator for selected color
color_indicator = pygame.Surface((110, 60), pygame.SRCALPHA)
pygame.draw.rect(color_indicator, (255, 255, 255, 100), color_indicator.get_rect(), border_radius=8)

# Game over screen
game_over_screen = pygame.image.load(resource_path('over1.jpg'))  # Load game over screen image
game_over_screen = pygame.transform.scale(game_over_screen, (WIDTH, HEIGHT))

# Main game loop
startup = True
running = False
shop_open = False
paused = False
selected_color_index = 0  # Index of the currently selected color in the shop

def reset_game():
    global player_snake, coins, foods, food
    player_snake = {
        'pos': [(WIDTH / 2, HEIGHT / 2)],
        'direction': (1, 0),
        'color': GREEN,
        'growth': 0
    }
    coins = 0
    foods.clear()
    food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
            random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

# Add the following function to handle mouse clicks
def handle_mouse_click():
    global shop_open, player_snake, selected_color_index, coins
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(WIDTH - 120, HEIGHT - 70, 100, 50)
    if button_rect.collidepoint(mouse_pos):
        shop_open = not shop_open
    else:
        for i, color in enumerate(shop_colors):
            color_rect = pygame.Rect(50 + i * 150, 200, 100, 50)
            if color_rect.collidepoint(mouse_pos):
                # Check if enough coins and not the current color
                if shop_colors[i] != player_snake['color'] and coins >= 10:
                    coins -= 10  # Deduct coins for purchase
                    player_snake['color'] = shop_colors[i]
                    coins=0
                    
                    # Display confirmation message (optional)
                    purchase_text = font.render("Purchased! New Color: " + str(shop_colors[i]), True, WHITE)
                    WINDOW.blit(purchase_text, (WIDTH // 2 - 150, HEIGHT // 2))
                    coins=0
                    pygame.display.update()
                    pygame.time.delay(1000)  # Briefly display message

                    # Add visual feedback (optional)
                    selected_color_index = i  # Update selected color index for highlighting
                    flash_surface = pygame.Surface(WINDOW.get_size())
                    flash_surface.fill((255, 255, 255, 128))  # Semi-transparent white flash
                    WINDOW.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(200)  # Briefly flash the screen

while startup:
    WINDOW.blit(start_screen, (0, 0))
    start_text = font.render("Press ENTER to Start Game", True, BLACK)
    guide_text = font.render("Press S for shop , P for pause", True, BLUE)
    WINDOW.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2 + 30))
    WINDOW.blit(guide_text, (WIDTH // 2 - 150, HEIGHT // 2 + 120))
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            startup = False
            running = True
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_snake['direction'] != (0, 1):
                player_snake['direction'] = (0, -1)  # Move up
            elif event.key == pygame.K_DOWN and player_snake['direction'] != (0, -1):
                player_snake['direction'] = (0, 1)  # Move down
            elif event.key == pygame.K_LEFT and player_snake['direction'] != (1, 0):
                player_snake['direction'] = (-1, 0)  # Move left
            elif event.key == pygame.K_RIGHT and player_snake['direction'] != (-1, 0):
                player_snake['direction'] = (1, 0)  # Move right
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_s:
                shop_open = not shop_open
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_LEFT:
                selected_color_index = (selected_color_index - 1) % len(shop_colors)
                player_snake['color'] = shop_colors[selected_color_index]
            elif event.key == pygame.K_RIGHT:
                selected_color_index = (selected_color_index + 1) % len(shop_colors)
                player_snake['color'] = shop_colors[selected_color_index]

        # Check for mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click()

    if paused:
        clock.tick(5)  # Adjust the speed while paused
        continue

    # If the shop is open, display the shop screen
    if shop_open:
        WINDOW.blit(shop_screen, (0, 0))
        # Display available snake colors in the shop
        for i, color in enumerate(shop_colors):
            color_rect = pygame.Rect(50 + i * 150, 200, 100, 50)
            pygame.draw.rect(WINDOW, color, color_rect)
            if i == selected_color_index:
                WINDOW.blit(color_indicator, (50 + i * 150 - 5, 200 - 5))
            price_text = font.render("Price: 10 coins", True, WHITE)
            WINDOW.blit(price_text, (50 + i * 150, 260))
        pygame.display.update()
        continue  # Skip the rest of the loop to avoid snake movement in the shop

    # Move the player snake
    new_head = (player_snake['pos'][0][0] + player_snake['direction'][0] * BLOCK_SIZE,
                player_snake['pos'][0

][1] + player_snake['direction'][1] * BLOCK_SIZE)
    player_snake['pos'].insert(0, new_head)

    # Check for collisions with food
    if player_snake['pos'][0] == food:
        food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
        player_snake['growth'] += 1
        coins += 1
        eating_sound.play()
    
    # Check for collisions with the snake's own body
    if len(player_snake['pos']) > 1 and player_snake['pos'][0] in player_snake['pos'][1:]:
        running = False  # Game over
    
    # Check for collisions with the walls
    if player_snake['pos'][0][0] < 0 or player_snake['pos'][0][0] >= WIDTH or \
            player_snake['pos'][0][1] < 0 or player_snake['pos'][0][1] >= HEIGHT:
        running = False  # Game over
        end_sound.play()

    # Move the snake's body
    if player_snake['growth'] > 0:
        player_snake['growth'] -= 1
    else:
        player_snake['pos'].pop()

    # Clear the window
    WINDOW.blit(game_background, (0, 0))

    # Draw the player snake
    for pos in player_snake['pos']:
        pygame.draw.rect(WINDOW, player_snake['color'], (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw the food
    pygame.draw.rect(WINDOW, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

    # Display the coins
    coin_text = font.render(f"Coins: {coins}", True, WHITE)
    WINDOW.blit(coin_text, (10, 10))

    # If game over, display game over screen and allow restart
    if not running:
        WINDOW.blit(game_over_screen, (0, 0))
        restart_text = font.render("Press ENTER to Restart", True, WHITE)
        WINDOW.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        pygame.display.update()
        # Wait for ENTER key to be pressed
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    reset_game()
                    running = True
                    break
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if running:
                break  # Break out of the loop if the game is restarted

    # Draw the shop button
    # WINDOW.blit(shop_button, (WIDTH - 120, HEIGHT - 70))

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(10)  # Adjust the speed

# Quit Pygame
pygame.quit()


#This version of the code adds functionality for navigating between colors in the shop using the left and right arrow keys. Additionally, it introduces more colors to the shop, allowing the player to choose from a wider range of options.