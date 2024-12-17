import pygame
import sys
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

# Background colors
coral = (255, 250, 55)
dodo= (219,79,79)
red = (0, 0, 255)
gray = (100, 100, 100)
green = (76, 208, 56)
yellow = (255, 232, 0)
white = (255, 255, 255)
steel_blue = (70, 130, 180)
black = (0, 0, 0)


#loading 
loading= pygame.image.load(r'dakdak\images\loading.png')

# Window dimensions
width = 500
height = 500
screen_size = (width, height)
pygame.display.set_caption('Bronya Lái Lụa')
icon = pygame.image.load(r'dakdak\images\icon.jpg')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(screen_size)

# Define fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Menu options
menu_options = ["Start Game", "Exit"]
selected_option = 0

def draw_menu():
    screen.blit(loading, (0, 0))
    title_text = font.render("Bronya lái xe", True, dodo)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 340))

    for index, option in enumerate(menu_options):
        color = dodo if index == selected_option else black
        option_text = small_font.render(option, True, color)
        screen.blit(option_text, (width // 2 - option_text.get_width() // 2, 250 + index * 50))

    pygame.display.flip()

def main_menu():
    global selected_option
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        start_game()
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()

        draw_menu()

def start_game():
    gameover = False
    speed = 2
    score = 0

    # Load game over image
    over = pygame.image.load(r'dakdak\images\gameover.png')
    over = pygame.transform.scale2x(over)
    over_rect = over.get_rect()

    #music
    pygame.mixer.music.load(r'dakdak\sound\background_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    # Road dimensions
    road_width = 300
    street_width = 10
    street_height = 50
    lane_left = 150
    lane_center = 250
    lane_right = 350
    lanes = [lane_left, lane_center, lane_right]
    lane_move_y = 0

    # Road and edges
    road = (100, 0, road_width, height)
    left_edge = (95, 0, street_width, height)
    right_edge = (395, 0, street_width, height)

    # Initial player position
    player_x = 250
    player_y = 400

    class Vehicle(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)
            image_scale = 45 / image.get_rect().width
            new_width = image.get_rect().width * image_scale
            new_height = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (new_width, new_height))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

    class PlayerVehicle(Vehicle):
        def __init__(self, x, y):
            image = pygame.image.load(r'dakdak\images\bronya.png')
            super().__init__(image, x, y)

    # Sprite groups
    player_group = pygame.sprite.Group()
    Vehicle_group = pygame.sprite.Group()
    player = PlayerVehicle(player_x, player_y)
    player_group.add(player)

    # Load enemy vehicles
    image_name = ['nho_con.png', 'ronglon.png', 'tay_ba.png']
    Vehicle_images = [pygame.image.load('dakdak\\images\\' + name) for name in image_name]

    # Load crash image
    crash = pygame.image.load(r'dakdak\images\boom.png')
    crash_rect = crash.get_rect()

    # Setup FPS
    clock = pygame.time.Clock()
    fps = 120
    running = True

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT and player.rect.center[0] > lane_left:
                    player.rect.x -= 100
                if event.key == K_RIGHT and player.rect.center[0] < lane_right:
                    player.rect.x += 100
                for vehicle in Vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle):
                        gameover = True

        if pygame.sprite.spritecollide(player, Vehicle_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

        # Draw terrain
        screen.fill(steel_blue)
        pygame.draw.rect(screen, gray, road)
        pygame.draw.rect(screen, yellow, left_edge)
        pygame.draw.rect(screen, yellow, right_edge)

        lane_move_y += speed * 2
        if lane_move_y >= street_height * 2:
            lane_move_y = 0
        for y in range(street_height * -2, height, street_height * 2):
            pygame.draw.rect(screen, white, (lane_left + 45, y + lane_move_y, street_width, street_height))
            pygame.draw.rect(screen, white, (lane_center + 45, y + lane_move_y, street_width, street_height))

        player_group.draw(screen)

        if len(Vehicle_group) < 2:
            add_vehicle = True
            for vehicle in Vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
            if add_vehicle:
                lane = random.choice(lanes)
                image = random.choice(Vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                Vehicle_group.add(vehicle)

        for vehicle in Vehicle_group:
            vehicle.rect.y += speed
            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1
                if score > 0 and score % 2 == 0: #gia toc
                    speed += 0.1

        Vehicle_group.draw(screen)

        # Display score
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'Score: {score}', True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 40)
        screen.blit(text, text_rect)

        if gameover:
            screen.blit(crash, crash_rect)
            screen.blit(over, over_rect)
            text = font.render(f'TRY AGAIN? UP(Y) DOWN(N)', True, coral)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 450)
            screen.blit(text, text_rect)

        pygame.display.update()

        while gameover:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover = False
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        gameover = False
                        score = 0
                        speed = 2
                        Vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                    elif event.key == K_DOWN:
                        gameover = False
                        running = False

    pygame.quit()

if __name__ == "__main__":
    main_menu()
