#!/usr/bin/python3
import pygame
import os
from pygame.locals import *

obstacle_img = pygame.image.load(os.path.join(".", "art", "obstacle.png"))
floor_img = pygame.image.load(os.path.join(".", "art", "floor.png"))
wall_img = pygame.image.load(os.path.join(".", "art", "wall.png"))

cell_size = 50
room_rib = 10
room_size = cell_size * room_rib

boardXOffset = 150
boardYOffset = 50

screen_size = (800, 600)

class Level():
    cubert = None
    cells = None
    def __init__(self, screen, level="01"):
        self.screen = screen
        self.obstacles = []
        self.loadMap(level)

    def loadMap(self, mapName):
        with open(f'level{mapName}.map', 'r') as f:
            room_ribVal = f.read(3)
            room_rib = int(f'0x{room_ribVal}', 0)
            print(f"Setting up level size {room_rib}x{room_rib}")
            self.cells = []
            y = 0
            for i in range(room_rib):
                self.cells.append([])
                x = 0
                for j in range(room_rib):
                    cellVal = str(f.read(1))
                    if cellVal == "C":
                        self.cubert = Cubert(self, x, y)  # Initialize Cubert.
                    elif cellVal == "X":
                        self.putObstacle("obstacle", x, y)
                    x += 1
                    self.cells[i].append(cellVal)
                y += 1
                f.read(1) # \n

    def getCubert(self):
        return self.cubert

    def getCoords(self, x, y):
        return (boardXOffset + x * cell_size, boardYOffset + y * cell_size)

    def putObstacle(self, type, x, y):
        rect = pygame.Rect(*self.getCoords(x, y), cell_size, cell_size)
        self.obstacles.append({"image": obstacle_img, "rect": rect})

    def draw(self):
        # Draw walls
        for x in range(0, screen_size[0] + 1, cell_size):
            for y in range(0, screen_size[1] + 1, cell_size):
                self.screen.blit(wall_img, pygame.Rect(x, y, cell_size, cell_size))
        # Draw floor
        for x in range(int((800 - room_size)/2), int((800 - room_size)/2) + room_size, cell_size):
            for y in range(int((600 - room_size)/2), int((600 - room_size)/2) + room_size, cell_size):
                self.screen.blit(floor_img, pygame.Rect(x, y, cell_size, cell_size))
        pygame.draw.rect(self.screen, ("#ffffff"), ((800 - room_size)/2, (600 - room_size)/2, room_size, room_size), 3)

        for obstacle in self.obstacles:
            self.screen.blit(obstacle["image"], obstacle["rect"].topleft)

    def canMove(self, x, y):
        if (x == len(self.cells) or x<0 or self.cells[y][x] == 'X'):
            return False
        if (y == len(self.cells[y-1]) or y<0 or self.cells[y][x] == 'X'):
            return False
        return True
class Cubert(pygame.sprite.Sprite):
    rect = None
    skins = None
    def __init__(self, level, startX, startY):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.size = cell_size
        self.xPos = startX
        self.yPos = startY
        self.level = level
        #unscaled_image = pygame.image.load(os.path.join(".", "art", "cubert.png")).convert()
        #self.image = pygame.transform.scale(unscaled_image, self.size)
        self.skins = {
            "cubert": pygame.image.load(os.path.join(".", "art", "cubert.png")).convert(),
            "circle": pygame.image.load(os.path.join(".", "art", "cubert-circle.png")).convert(),
        }

        self.beCubert()
        initial_position = self.level.getCoords(startX, startY)
        self.rect.topleft = initial_position  # This sets the initial position.

    def move_to(self, dir):
        if dir=="right":
            if(self.level.canMove(self.xPos + 1, self.yPos)):
                self.xPos += 1
                self.rect.move_ip(cell_size, 0)
        if dir=="left":
            if(self.level.canMove(self.xPos - 1, self.yPos)):
                self.xPos -= 1
                self.rect.move_ip(-cell_size, 0)
        if dir=="up":
            if(self.level.canMove(self.xPos, self.yPos - 1)):
                self.yPos -= 1
                self.rect.move_ip(0, -cell_size)
        if dir=="down":
            if(self.level.canMove(self.xPos, self.yPos + 1)):
                self.yPos += 1
                self.rect.move_ip(0, cell_size)

    def beCircle(self):
        self.is_circle = True
        self.image = self.skins["circle"]
        self.rect = self.image.get_rect(center=self.rect.center)

    def beCubert(self):
        self.is_circle = False
        self.image = self.skins["cubert"]
        if not self.rect:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, event):
        keys = pygame.key.get_pressed()
        
        if event.type == KEYDOWN:
            if event.key ==K_RIGHT:
                self.move_to("right")
            if event.key ==K_LEFT:
                self.move_to("left")
            if event.key ==K_UP:
                self.move_to("up")
            if event.key ==K_DOWN:
                self.move_to("down")
            if keys[pygame.K_SPACE]:
                self.beCircle()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                self.beCubert()


def game_main(music=True):
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.music.load(os.path.join(".", "sounds", "game.ogg"))
    if music:
        pygame.mixer.music.play(loops=-1)
    # sound = pygame.mixer.Sound(os.path.join(".", "sounds", "game.ogg"))
    # sound.play(loops=5)

    screen = pygame.display.set_mode(screen_size)
    pygame.key.set_repeat(200)

    level = Level(screen, "01")
    cubert = level.getCubert()
    if not cubert:
        print("Cubert is missing!")
        return

    running = True

    while running:
        level.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
                break

            previous_position = cubert.rect.topleft
            cubert.update(event)  # Update Cubert.

        screen.blit(cubert.image, cubert.rect)  # Draw Cubert to the screen.

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game_main(False)
