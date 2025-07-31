import pygame
import random
import os
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BIRD_SIZE = 30
CLOUD_WIDTH, CLOUD_HEIGHT = 100, 60
PIPE_WIDTH = 80
PIPE_GAP = 170
GRAVITY = 0.4
JUMP_VELOCITY = -5

background_img = pygame.image.load('background.png')
background_img2 = pygame.image.load('background2.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_img2 = pygame.transform.scale(background_img2, (WIDTH, HEIGHT))

# Load Images
bird_image = pygame.transform.scale(pygame.image.load('bird.png'), (int(BIRD_SIZE*1.3), int(BIRD_SIZE*1.3)))
cloud_image = pygame.transform.scale(pygame.image.load('cloud.png'), (CLOUD_WIDTH, CLOUD_HEIGHT))
pipe_image = pygame.image.load('pipe.png')
pipe_image_flipped = pygame.transform.flip(pipe_image, False, True)

# Load Music
menu_music = 'menu_music.mp3'
game_music = 'game_music.mp3'
gameover_music = 'gameover_music.mp3'

# Font
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# High Score file
HS_FILE = "highscore.txt"
if not os.path.exists(HS_FILE):
    with open(HS_FILE, "w") as f:
        f.write("0")

def load_high_score():
    with open(HS_FILE, "r") as f:
        return int(f.read())

def save_high_score(score):
    high = load_high_score()
    if score > high:
        with open(HS_FILE, "w") as f:
            f.write(str(score))

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rect = bird_image.get_rect(topleft=(self.x, self.y))

    def jump(self):
        self.velocity = JUMP_VELOCITY

    def update(self):
        self.y += self.velocity
        self.velocity += GRAVITY
        if self.y < 0:
            self.y = 0
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(bird_image, (int(self.x), int(self.y)))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)

        scaled_pipe_top = pygame.transform.scale(pipe_image_flipped, (PIPE_WIDTH, self.height))
        scaled_pipe_bottom = pygame.transform.scale(pipe_image, (PIPE_WIDTH, HEIGHT - (self.height + PIPE_GAP)))

        self.top_image = scaled_pipe_top
        self.bottom_image = scaled_pipe_bottom

        self.top_rect = self.top_image.get_rect(bottomleft=(self.x, self.height))
        self.bottom_rect = self.bottom_image.get_rect(topleft=(self.x, self.height + PIPE_GAP))

    def update(self):
        self.x -= 3
        self.top_rect.bottomleft = (self.x, self.height)
        self.bottom_rect.topleft = (self.x, self.height + PIPE_GAP)

    def draw(self, screen):
        screen.blit(self.top_image, self.top_rect)
        screen.blit(self.bottom_image, self.bottom_rect)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.x -= 1

    def draw(self, screen):
        screen.blit(cloud_image, (int(self.x), int(self.y)))

def draw_text(screen, text, x, y, color=(255,255,255), font_obj=font):
    txt = font_obj.render(text, True, color)
    screen.blit(txt, (x, y))

def main_menu(screen, music_on):
    pygame.mixer.music.load(menu_music)
    if music_on:
        pygame.mixer.music.play(-1)
    button_music_rect = pygame.Rect(WIDTH//2-100, HEIGHT//2+70, 200, 50)

    while True:
        screen.blit(background_img, (0, 0))

        draw_text(screen, "JD BIRD", WIDTH//2-95, HEIGHT//2-150, (255,255,0))
        draw_text(screen, "Press SPACE to Start", WIDTH//2-180, HEIGHT//2-20)
        draw_text(screen, "Music: ON" if music_on else "Music: OFF", WIDTH//2-80, HEIGHT//2+80, (0,0,0), small_font)
        draw_text(screen, "Developed by Aadhi Kabilan", WIDTH//2-200, HEIGHT-60, (255,255,255), small_font)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return music_on
            if event.type == MOUSEBUTTONDOWN:
                if button_music_rect.collidepoint(event.pos):
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()

def game_over(screen, score, music_on):
    pygame.mixer.music.load(gameover_music)
    if music_on:
        pygame.mixer.music.play(-1)
    high = load_high_score()
    if score > high:
        save_high_score(score)

    while True:
        screen.blit(background_img2, (0, 0))

        draw_text(screen, "GAME OVER!", WIDTH//2-100, HEIGHT//2-100, (255, 0, 0))
        draw_text(screen, f"Score: {score}", WIDTH//2-70, HEIGHT//2-30)
        draw_text(screen, f"High Score: {load_high_score()}", WIDTH//2-110, HEIGHT//2+20)
        draw_text(screen, "Press SPACE to Restart", WIDTH//2-200, HEIGHT//2+80)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return music_on

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    music_on = True
    music_on = main_menu(screen, music_on)

    pygame.mixer.music.load(game_music)
    if music_on:
        pygame.mixer.music.play(-1)

    bird = Bird(100, HEIGHT//2)
    clouds = [Cloud(WIDTH, HEIGHT/3.4)]
    pipes = [Pipe(WIDTH+200)]
    score = 0

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            bird.jump()

        bird.update()
        for cloud in clouds:
            cloud.update()
        for pipe in pipes:
            pipe.update()

        if pipes[-1].x < WIDTH - 300:
            pipes.append(Pipe(WIDTH))

        pipes = [p for p in pipes if not p.off_screen()]

        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                music_on = game_over(screen, score, music_on)
                main()

        if bird.y > HEIGHT-50:
            music_on = game_over(screen, score, music_on)
            main()

        for pipe in pipes:
            if pipe.x + PIPE_WIDTH < bird.x and not hasattr(pipe, 'scored'):
                score += 1
                pipe.scored = True

        screen.fill((0, 191, 255))
        for cloud in clouds:
            cloud.draw(screen)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        draw_text(screen, f"Score: {score}", 10, 10)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
