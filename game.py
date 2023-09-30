import pygame
import os
from pygame.locals import *

class Cubert(pygame.sprite.Sprite):
    def __init__(self, initial_position, cubert_size):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.size = cubert_size

        unscaled_image = pygame.image.load(os.path.join(".", "art", "cubert.png")).convert()
        self.image = pygame.transform.scale(unscaled_image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position  # This sets the initial position.
        self.is_circle = False

    def calc_cell_coords(self):
        room_coords = [
            (self.rect.topleft[0]-(screen_size[0]-room_size)/2),
            (self.rect.topleft[1]-(screen_size[1]-room_size)/2)
        ]
        return (room_coords[0]/(room_size/10)+1, room_coords[1]/(room_size/10)+1)

    def check_cell(self, cell):
        print(int(cell[0]))
        if (cell[0] > len(cells) or cell[0]<=0):
            return False
        if (cell[1] > len(cells[int(cell[0])-1]) or cell[1]<=0):
            return False
        # print(len(cells), len(cells[0]))
        # print(cell[1], len(cells[int(cell[0])]))
        # print(cell[0], len(cells))
        return True

    def move_to(self, dir):
        if dir=="right":
            if(self.check_cell((self.calc_cell_coords()[0]+1, self.calc_cell_coords()[1]))):
                self.rect.move_ip(cell_size, 0)
        if dir=="left":
            if(self.check_cell((self.calc_cell_coords()[0]-1, self.calc_cell_coords()[1]))):
                self.rect.move_ip(-cell_size, 0)
        if dir=="up":
            if(self.check_cell((self.calc_cell_coords()[0], self.calc_cell_coords()[1]-1))):
                self.rect.move_ip(0, -cell_size)
        if dir=="down":
            if(self.check_cell((self.calc_cell_coords()[0], self.calc_cell_coords()[1]+1))):
                self.rect.move_ip(0, cell_size)


    def update(self, event):
        keys = pygame.key.get_pressed()
        
        if event.type == KEYUP:
            if event.key ==K_RIGHT:
                self.move_to("right")
            if event.key ==K_LEFT:
                self.move_to("left")
            if event.key ==K_UP:
                self.move_to("up")
            if event.key ==K_DOWN:
                self.move_to("down")
            if keys[pygame.K_SPACE]:
                self.is_circle = True
                self.image = pygame.image.load(os.path.join(".", "art", "cubert-circle.png")).convert()
                self.rect = self.image.get_rect(center=self.rect.center)
        if event.type == KEYUP:
            if event.key == K_SPACE:
                self.is_circle = False
                self.image = pygame.image.load(os.path.join(".", "art", "cubert.png")).convert()
                self.rect = self.image.get_rect(center=self.rect.center)

white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)


cubert_size = [50, 50]
cell_size = cubert_size[0]

obstacle_img = pygame.image.load(os.path.join(".", "art", "obstacle.png"))
obstacles = [
    {"image": obstacle_img, "rect": pygame.Rect(200, 200, 50, 50)},
    {"image": obstacle_img, "rect": pygame.Rect(400, 400, 50, 50)},
]
floor_img = pygame.image.load(os.path.join(".", "art", "floor.png"))
wall_img = pygame.image.load(os.path.join(".", "art", "wall.png"))

room_size = 500

cells = []

for i in range(10):
    cells.append([])
    for j in range(10):
        cells[i].append("none")

screen_size = (800, 600)


def game_main():
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.music.load(os.path.join(".", "sounds", "game.ogg"))
    pygame.mixer.music.play(loops=-1)
    # sound = pygame.mixer.Sound(os.path.join(".", "sounds", "game.ogg"))
    # sound.play(loops=5)

    screen = pygame.display.set_mode(screen_size)
    pygame.key.set_repeat(35)

    cubert = Cubert([screen_size[0]-room_size+150, screen_size[1]-room_size+500/10*3], cubert_size=cubert_size)  # Initialize Cubert.

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
