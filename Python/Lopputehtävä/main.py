import pgzrun
import random
import os
import sys
from pgzero.keyboard import keys, keyboard
from weapons import weapon_data
from meteors import meteor_data

# Define properties for different game stages
STAGE_PROPERTIES = [
    {"name": f"Stage {i+1}", "background_color": (250, 250, 250), "max_meteors_on_screen": 4 + i, "max_stars": i + 10, "required_score": i*20 + 20}
    for i in range(20)
]

WIDTH, HEIGHT = 500, 700
BACKGROUND_SPEED = 1
METEOR_SPAWN_DELAY = 2

MAX_STARS = 100

# Extract weapon names and images
weapon_names, weapon_images = zip(*[(name, data['image']) for name, data in weapon_data.items()])
meteor_images = list(meteor_data.keys())
meteors = []

# Initialize player's ship, bullets, and game variables
ship = Actor('playership1_blue')
ship.pos = (WIDTH // 2, HEIGHT // 2)
bullets = []
score = 0
game_over = False
max_meteors_on_screen = 3
meteor_spawn_timer = 0
current_weapon_index = 0
fire_cooldown = 0.0
space_held_down = False
player_speed_modifier = 1.0
lives = 3
invincibility_timer = 0.0
current_stage = 0

# Keep track of unlocked weapons
unlocked_weapons = set()

# Initialize stars for the background
stars = [Actor(random.choice(['star_med', 'star_small', 'star_tiny']), pos=(random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(MAX_STARS)]

# Function to unlock new weapons based on the player's score
def unlock_weapons():
    global unlocked_weapons
    for weapon_name, weapon_info in weapon_data.items():
        if score >= weapon_info['unlock_score'] and weapon_name not in unlocked_weapons:
            unlocked_weapons.add(weapon_name)
            current_weapon_index = weapon_names.index(weapon_name)

# Function to draw hearts indicating player lives
def draw_hearts():
    heart_image = 'heart'
    heart_spacing = 30
    for i in range(lives):
        heart_x = WIDTH // 2 - (lives * heart_spacing) // 2 + i * heart_spacing
        heart_y = HEIGHT - 30
        screen.blit(heart_image, (heart_x, heart_y))

# Function to draw stars in the background with a scrolling effect
def draw_stars():
    global stars
    max_stars = STAGE_PROPERTIES[current_stage]["max_stars"]

    for star in stars:
        star.y += BACKGROUND_SPEED
        if star.y > HEIGHT:
            star.y = 0
            star.x = random.randint(0, WIDTH)

    # Add new stars to reach the maximum allowed for the current stage
    while len(stars) < max_stars:
        stars.append(Actor(random.choice(['star_med', 'star_small', 'star_tiny']), pos=(random.randint(0, WIDTH), random.randint(0, HEIGHT))))

    for star in stars:
        star.draw()

# Function to reset the game state
def reset_game():
    global game_over, meteors, meteor_spawn_timer, current_stage, score
    game_over = False
    score = 0
    lives = 3
    meteors.clear()
    spawn_new_meteor()
    ship.pos = (WIDTH // 2, HEIGHT // 2)
    invincibility_timer = 0.0
    current_stage = 1

# Function to handle player shooting
def shoot():
    global fire_cooldown
    if fire_cooldown <= 0:
        bullet = Actor(weapon_images[current_weapon_index], pos=(ship.x, ship.y - 30))
        bullets.append(bullet)
        fire_cooldown = weapon_data[weapon_names[current_weapon_index]]['cooldown']

# Function to handle key press events
def on_key_down(key):
    global fire_cooldown, space_held_down, player_speed_modifier, current_weapon_index
    if key == keys.ESCAPE:
        sys.exit()
    if key == keys.SPACE:
        space_held_down = True
        if fire_cooldown <= 0:
            shoot()
            fire_cooldown = weapon_data[weapon_names[current_weapon_index]]['cooldown']
    if key in [keys.Q, keys.E]:
        direction = -1 if key == keys.Q else 1
        current_weapon_index = (current_weapon_index + direction) % len(weapon_names)
    if key == keys.LSHIFT:
        player_speed_modifier *= 1.5
    elif key == keys.LCTRL:
        player_speed_modifier *= 0.5

# Function to handle key release events
def on_key_up(key):
    global space_held_down, player_speed_modifier
    if key == keys.SPACE:
        space_held_down = False
    elif key in [keys.W, keys.S]:
        player_speed_modifier = 1.0

# Function to update game state
def update(dt):
    global WIDTH, HEIGHT, score, game_over, meteors, meteor_spawn_timer, fire_cooldown, space_held_down, player_speed_modifier, lives, invincibility_timer, stars, current_stage, current_weapon_index, screen

    WIDTH, HEIGHT = screen.width, screen.height

    speed = 5 * player_speed_modifier
    global meteor_speed
    meteor_speed = 5 + current_stage * 0.5
    ship.x -= speed if keyboard.a and ship.x > 20 else 0
    ship.x += speed if keyboard.d and ship.x < WIDTH - 20 else 0
    ship.y -= speed if keyboard.W and ship.y > 20 else 0
    ship.y += speed if keyboard.S and ship.y < HEIGHT - 20 else 0

    if space_held_down and fire_cooldown <= 0:
        shoot()
        fire_cooldown = weapon_data[weapon_names[current_weapon_index]]['cooldown']

    for meteor_info in meteors:
        if meteor_info['hp'] > 0:
            meteor_info['pos'] = (meteor_info['pos'][0], meteor_info['pos'][1] + meteor_speed)

    draw_stars()

    update_bullets()

    # Check if the player reached the required score for the next stage
    if current_stage < len(STAGE_PROPERTIES) - 1 and score >= STAGE_PROPERTIES[current_stage]["required_score"]:
        current_stage += 1
        screen.fill(STAGE_PROPERTIES[current_stage]["background_color"])

    # Check for player invincibility due to recent collision
    if invincibility_timer > 0:
        invincibility_timer -= dt
    else:
        # Check for collisions between the ship and meteors
        for meteor_info in meteors:
            meteor_actor = Actor(meteor_info['image'], pos=meteor_info['pos'])
            if ship.colliderect(meteor_actor):
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    ship.pos = (WIDTH // 2, HEIGHT // 2)
                    invincibility_timer = 3.0

    # Remove off-screen meteors and bullets
    meteors = [meteor_info for meteor_info in meteors if meteor_info['pos'][1] <= HEIGHT and meteor_info['hp'] > 0]
    bullets[:] = [bullet for bullet in bullets if bullet.y > 0]

    # Add new stars periodically to the background
    if score % 10 == 0 and score > 0:
        stars = [star for star in stars if star.y < HEIGHT]
        stars.append(Actor(random.choice(['star_med', 'star_small', 'star_tiny']), pos=(random.randint(0, WIDTH), random.randint(0, HEIGHT))))

    meteor_spawn_timer += dt
    fire_cooldown = max(0, fire_cooldown - dt)

    # Unlock new weapons based on the player's score
    unlock_weapons()

    # Spawn new meteors periodically
    if meteor_spawn_timer >= METEOR_SPAWN_DELAY and len(meteors) < max_meteors_on_screen:
        spawn_new_meteor()
        meteor_spawn_timer = 0

    # Reset the game if it's over and the player presses 'R'
    if game_over and keyboard.r:
        reset_game()
        stars = [Actor(random.choice(['star_med', 'star_small', 'star_tiny']), pos=(random.randint(0, WIDTH), random.randint(0, HEIGHT))) for _ in range(MAX_STARS)]
        screen.fill(STAGE_PROPERTIES[current_stage]["background_color"])
        game_over = False

# Function to update the state of bullets and handle collisions with meteors
def update_bullets():
    global score
    bullets_to_remove = []
    for bullet in bullets:
        bullet.y -= 10
        for meteor_info in meteors:
            meteor_actor = Actor(meteor_info['image'], pos=meteor_info['pos'])
            if bullet.colliderect(meteor_actor):
                damage = weapon_data[weapon_names[current_weapon_index]]['damage']
                meteor_info['hp'] -= damage
                if meteor_info['hp'] <= 0:
                    meteor_info['hp'] = 0
                    score += 1
                    spawn_new_meteor()
                bullets_to_remove.append(bullet)
    bullets[:] = [bullet for bullet in bullets if bullet not in bullets_to_remove]

# Function to get the health of a meteor based on its image
def get_meteor_health(meteor_image):
    return meteor_data.get(meteor_image, {'health': 1})['health']

# Function to spawn a new meteor at the top of the screen
def spawn_new_meteor():
    global meteors
    meteor_image = random.choice(meteor_images)
    meteor_info = {'image': meteor_image, 'pos': (random.randint(20, WIDTH - 20), 0),
                   'hp': get_meteor_health(meteor_image)}
    meteors.append(meteor_info)

# Function to draw the game elements on the screen
def draw():
    global WIDTH, HEIGHT, game_over, invincibility_timer, current_stage
    screen.fill((0, 0, 0))
    draw_stars()

    if game_over:
        # Display game over message and options
        game_over_text = 'Game Over'
        score_text = 'Score: ' + str(score)
        continue_text = 'Press R to Continue'
        quit_text = 'ESC to quit'

        text_size1 = 60
        text_x = WIDTH // 2 - len(game_over_text) * text_size1 // 5
        text_y = HEIGHT // 2 - text_size1
        screen.draw.text(game_over_text, (text_x, text_y), color=(255, 255, 255), fontsize=text_size1)

        text_size2 = 30
        text_x = WIDTH // 2 - len(score_text) * text_size2 // 5
        text_y = HEIGHT // 2 + 50
        screen.draw.text(score_text, (text_x, text_y), color=(255, 255, 255), fontsize=text_size2)

        text_size3 = 20
        text_x = WIDTH // 2 - len(continue_text) * text_size3 // 5
        text_y = HEIGHT // 2 + 100
        screen.draw.text(continue_text, (text_x, text_y), color=(255, 255, 255), fontsize=text_size3)

        text_x = WIDTH // 2 - len(quit_text) * text_size3 // 5
        text_y = HEIGHT // 2 + 150
        screen.draw.text(quit_text, (text_x, text_y), color=(255, 255, 255), fontsize=text_size3)
    else:
        # Draw game elements during active gameplay
        if invincibility_timer <= 0 or int(invincibility_timer * 10) % 2 == 0:
            ship.draw()

        for bullet in bullets:
            bullet.draw()

        screen.draw.text('Score: ' + str(score), (15, 10), color=(255, 255, 255), fontsize=30)
        screen.draw.text('Weapon: ' + weapon_names[current_weapon_index], (WIDTH - 200, HEIGHT - 30),
                        color=(255, 255, 255), fontsize=20)
        draw_hearts()

        for meteor_info in meteors:
            meteor_actor = Actor(meteor_info['image'], pos=meteor_info['pos'])
            meteor_actor.draw()

        if not game_over:
            screen.draw.text('Ship Cooldown: {:.1f}'.format(fire_cooldown), (15, 50), color=(255, 255, 255), fontsize=20)

        screen.draw.text(STAGE_PROPERTIES[current_stage]['name'], (WIDTH - 150, 10), color=(255, 255, 255), fontsize=20)

# Set environment variable to center the game window
os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
