import pygame
import os
from pygame.locals import *

class Cubert(pygame.sprite.Sprite):
    def __init__(self, initial_position, cubert_size):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface([25, 25])  # Cubert's size. Adjust as needed.
        # self.image.fill((255, 0, 0))  # A deliciously devilish shade of red.
        self.health = 3
        self.size = cubert_size

        self.image = pygame.image.load(os.path.join(".", "art", "cubert.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position  # This sets the initial position.
        self.is_circle = False
        self.turned = True

    def update(self, event):
        keys = pygame.key.get_pressed()
        
        if event.type == KEYDOWN:
            if keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)
            if keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
            if keys[pygame.K_UP]:
                self.rect.move_ip(0, -5)
            if keys[pygame.K_DOWN]:
                self.rect.move_ip(0, 5)
            if keys[pygame.K_SPACE] and self.turned:
                self.is_circle = not self.is_circle
                self.turned = False
                if self.is_circle:
                    self.image = pygame.image.load(os.path.join(".", "art", "cubert-circle.png")).convert()
                    pygame.draw.circle(self.image, (255, 0, 0), (13, 13), 13)  # A delightful circle
                    self.rect = self.image.get_rect(center=self.rect.center)
                else:
                    self.image.fill((255, 0, 0))  # Back to a delightful square.
        if event.type == KEYUP:
            if keys[pygame.K_SPACE]:
                self.turned = True

white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)

cubert_size = [30, 30]

obstacle_img = pygame.image.load(os.path.join(".", "art", "obstacle.png"))
obstacles = [
    {"image": obstacle_img, "rect": pygame.Rect(200, 200, 50, 50)},
    {"image": obstacle_img, "rect": pygame.Rect(400, 400, 50, 50)},
]
floor_img = pygame.image.load(os.path.join(".", "art", "floor.png"))
wall_img = pygame.image.load(os.path.join(".", "art", "wall.png"))

room_size = 500

def game_main():
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.music.load(os.path.join(".", "sounds", "game.ogg"))
    pygame.mixer.music.play(loops=-1)
    # sound = pygame.mixer.Sound(os.path.join(".", "sounds", "game.ogg"))
    # sound.play(loops=5)

    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.key.set_repeat(35)

    cubert = Cubert([screen_size[0]/2-(cubert_size[0]/2), screen_size[1]/2-(cubert_size[1]/2)+screen_size[1]/3], cubert_size=cubert_size)  # Initialize Cubert.

    running = True
    while running:
        screen.fill(("#878787"))
        # Draw walls
        for x in range(0, screen_size[0]+1, 50):
            for y in range(0, screen_size[1]+1, 50):
                screen.blit(wall_img, pygame.Rect(x, y, 50, 50))
        # Draw floor
        for x in range(int((800-room_size)/2), int((800-room_size)/2)+room_size, 50):
            for y in range(int((600-room_size)/2), int((600-room_size)/2)+room_size, 50):
                screen.blit(floor_img, pygame.Rect(x, y, 50, 50))
        pygame.draw.rect(screen, ("#ffffff"), ((800-room_size)/2, (600-room_size)/2, room_size, room_size), 3)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                break

            previous_position = cubert.rect.topleft
            cubert.update(event)  # Update Cubert.
            for obstacle in obstacles:
                if cubert.rect.colliderect(obstacle["rect"]):
                    cubert.rect.topleft = previous_position  # If Cubert hits an obstacle, move him back.

        screen.blit(cubert.image, cubert.rect)  # Draw Cubert to the screen.

        for obstacle in obstacles:
            screen.blit(obstacle["image"], obstacle["rect"].topleft)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game_main()
