#!/usr/bin/python3
import pygame
import os
from pygame.locals import *
from cutils import set_cells_to_value

pygame.init()
pygame.mixer.init()
pygame.font.init()

MARKER_BLOCK = "B"
MARKER_OBSCALETE = "X"
MARKER_COIN = "M"
MARKER_EMPTY = "O"

MARKER_BONUS_JUMP = "J"
MARKER_BONUS_SPEED = "S"

obstacle_img = pygame.image.load(os.path.join(".", "art", "obstacle.png"))
coin_img = pygame.image.load(os.path.join(".", "art", "coin.png"))
wail_img = pygame.image.load(os.path.join(".", "art", "wall.png"))
floor_img = pygame.image.load(os.path.join(".", "art", "floor.png"))
wall_img = pygame.image.load(os.path.join(".", "art", "wall.png"))
bonusJ_img = pygame.image.load(os.path.join(".", "art", "jump_bonus.png"))
bonusS_img = pygame.image.load(os.path.join(".", "art", "speed_bonus.png"))

death_snd = pygame.mixer.Sound(os.path.join(".", "sounds", "death.wav"))
coin_snd = pygame.mixer.Sound(os.path.join(".", "sounds", "coin.wav"))

cell_size = 50

boardXOffset = 150
boardYOffset = 50

screen_size = (800, 600)

class CoinCounter():
    def __init__(self, screen):
        self.screen = screen
        self.counter = 0
        self.font = pygame.font.Font('kongtext.ttf', 24)
        self.text = self.font.render('00:00', True, "#222034", "#cbdbfc")
        self.textRect = self.text.get_rect()
        self.textRect.center = (100, 55)

    def draw(self):
        rect = pygame.Rect(0, 30, cell_size, cell_size)
        self.screen.blit(coin_img, rect.topleft)
        self.text = self.font.render(str(self.counter), True, "#222034", "#cbdbfc")
        self.screen.blit(self.text, self.textRect)

    def addOne(self):
        self.counter += 1

class Level():
    cubert = None
    cells = None
    def __init__(self, screen, level="01"):
        self.screen = screen
        self.coinCounter = CoinCounter(screen)
        self.loadMap(level)

    def loadMap(self, mapName):
        with open(f'levels/level{mapName}.map', 'r') as f:
            room_ribVal = f.read(3)
            self.room_rib = int(f'0x{room_ribVal}', 0)
            self.room_size = cell_size * self.room_rib
            print(f"Setting up level size {self.room_rib}x{self.room_rib}")
            self.cells = []
            y = 0
            for i in range(self.room_rib):
                self.cells.append([])
                x = 0
                for j in range(self.room_rib):
                    cellVal = str(f.read(1))
                    if cellVal == "C":
                        self.cubert = Cubert(self, x, y)  # Initialize Cubert.
                    elif cellVal == "O":
                        cellVal = MARKER_COIN
                    x += 1
                    self.cells[i].append(cellVal)
                y += 1
                f.read(1) # \n

    def getCubert(self):
        return self.cubert

    def getCoords(self, x, y):
        return (boardXOffset + x * cell_size, boardYOffset + y * cell_size)

    def redraw(self):
        y = 0
        for row in self.cells:
            x = 0
            for cell in row:
                if cell == MARKER_OBSCALETE:
                  self.putObstacle("obstacle", x, y)
                elif cell == MARKER_COIN:
                    self.putCoin(x, y)
                elif cell in [MARKER_BONUS_JUMP, MARKER_BONUS_SPEED]:
                    self.putBonus(cell, x, y)
                elif cell == MARKER_BLOCK:
                    self.putBlock(x, y)
                x+=1
            y+=1

    def putObstacle(self, obType, x, y):
        rect = pygame.Rect(*self.getCoords(x, y), cell_size, cell_size)
        self.screen.blit(obstacle_img, rect.topleft)

    def putCoin(self, x, y):
        rect = pygame.Rect(*self.getCoords(x, y), cell_size, cell_size)
        self.screen.blit(coin_img, rect.topleft)

    def putBonus(self, bonusType, x, y):
        if bonusType == MARKER_BONUS_JUMP:
            rect = pygame.Rect(*self.getCoords(x, y), cell_size, cell_size)
            self.screen.blit(bonusJ_img, rect.topleft)
        elif bonusType == MARKER_BONUS_SPEED:
            rect = pygame.Rect(*self.getCoords(x, y), cell_size, cell_size)
            self.screen.blit(bonusS_img, rect.topleft)
            pass
    
    def putBlock(self, x, y):
        rect = pygame.Rect(*self.getCoords(x, y), cell_size, cell_size)
        self.screen.blit(wall_img, rect.topleft)

    def draw(self):
        # Draw walls
        for x in range(0, screen_size[0] + 1, cell_size):
            for y in range(0, screen_size[1] + 1, cell_size):
                self.screen.blit(wall_img, pygame.Rect(x, y, cell_size, cell_size))
        # Draw floor
        for x in range(int((800 - self.room_size)/2), int((800 - self.room_size)/2) + self.room_size, cell_size):
            for y in range(int((600 - self.room_size)/2), int((600 - self.room_size)/2) + self.room_size, cell_size):
                self.screen.blit(floor_img, pygame.Rect(x, y, cell_size, cell_size))
        pygame.draw.rect(self.screen, ("#ffffff"), ((800 - self.room_size)/2, (600 - self.room_size)/2, self.room_size, self.room_size), 3)

        self.coinCounter.draw()
        self.redraw()

    def canMove(self, x, y):
        if (x >= len(self.cells) 
            or x < 0
            or y >= len(self.cells[1])
            or y < 0
            ): return False
        if(self.cells[y][x] == MARKER_OBSCALETE):
                if(self.cubert.jumpBonusStart > 0):
                    return True
                return False
        if(self.cells[y][x] == MARKER_BLOCK):
            return False
        return True

    def isCoin(self, x, y):
        return self.cells[y][x] == MARKER_COIN

    def eatCoin(self, x, y):
        self.cells[y][x] = MARKER_EMPTY
        self.coinCounter.addOne()
        coin_snd.play()

    def isBonus(self, x, y):
        return self.cells[y][x] in [MARKER_BONUS_SPEED, MARKER_BONUS_JUMP]

    def eatBonus(self, x, y):
        bonus = self.cells[y][x]
        self.cells[y][x] = MARKER_EMPTY
        return bonus
    
    def block_fields(self, lvl):
        block_marker = MARKER_BLOCK
        new_matrix = set_cells_to_value(self.cells, lvl=lvl, value=block_marker)
        self.cells = new_matrix


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
        
        self.speedBonusStart = 0
        self.jumpBonusStart = 0

        self.lastTick = pygame.time.get_ticks()
        unscaled_cubert = pygame.image.load(os.path.join(".", "art", "cubert.png")).convert()
        unscaled_cubertCircle = pygame.image.load(os.path.join(".", "art", "cubert-speed-circle.png")).convert()
        unscaled_cubertYellowCircle = pygame.image.load(os.path.join(".", "art", "cubert-jump-circle.png")).convert()

        self.skins = {
            "cubert": pygame.transform.scale(unscaled_cubert, (cell_size, cell_size)),
            "speed-circle": pygame.transform.scale(unscaled_cubertCircle, (cell_size, cell_size)),
            "jump-circle": pygame.transform.scale(unscaled_cubertYellowCircle, (cell_size, cell_size)),
        }

        self.beCubert()
        initial_position = self.level.getCoords(startX, startY)
        self.rect.topleft = initial_position  # This sets the initial position.

    def move_to(self, dir):
        currentTick = pygame.time.get_ticks()
        if not self.speedBonusStart>0 and currentTick - 300 < self.lastTick:
            return
        else:
            self.lastTick = currentTick
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
        if self.level.isCoin(self.xPos, self.yPos):
            self.level.eatCoin(self.xPos, self.yPos)
        if (self.level.isBonus(self.xPos, self.yPos) and not self.is_circle):
            bonus = self.level.eatBonus(self.xPos, self.yPos)
            if bonus == MARKER_BONUS_SPEED: self.beCircle(MARKER_BONUS_SPEED)
            if bonus == MARKER_BONUS_JUMP: self.beCircle(MARKER_BONUS_JUMP)


    def beCircle(self, circleType="S"):
        self.is_circle = True
        if circleType == MARKER_BONUS_SPEED:
            self.image = self.skins["speed-circle"]
            self.speedBonusStart = int(pygame.time.get_ticks()/1000)
        elif circleType == MARKER_BONUS_JUMP:
            self.image = self.skins["jump-circle"]
            self.jumpBonusStart = int(pygame.time.get_ticks()/1000)

        self.rect = self.image.get_rect(center=self.rect.center)

    def beCubert(self):
        self.is_circle = False
        self.image = self.skins["cubert"]
        if not self.rect:
            self.rect = self.image.get_rect()
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, event):
        #keys = pygame.key.get_pressed()
        
        if event.type == KEYDOWN:
            if event.key ==K_RIGHT:
                self.move_to("right")
            if event.key ==K_LEFT:
                self.move_to("left")
            if event.key ==K_UP:
                self.move_to("up")
            if event.key ==K_DOWN:
                self.move_to("down")
            # if keys[pygame.K_SPACE]:
            #     self.beCircle()
        # if event.type == KEYUP:
        #     if event.key == K_SPACE:
        #         self.beCubert()
    def draw(self):
        if(self.speedBonusStart > 0):
            currentTick = int(pygame.time.get_ticks()/1000)
            if currentTick - 10 >= self.speedBonusStart:
                self.beCubert()
                self.speedBonusStart = 0
        elif(self.jumpBonusStart > 0):
            currentTick = int(pygame.time.get_ticks()/1000)
            if currentTick - 10 >= self.jumpBonusStart:
                self.beCubert()
                self.jumpBonusStart = 0

        self.level.screen.blit(self.image, self.rect)  # Draw Cubert to the screen.

class Timer():
    def __init__(self, screen, seconds=0):
        self.screen = screen
        self.font = pygame.font.Font('kongtext.ttf', 24)
        self.text = self.font.render('00:00', True, "#222034", "#cbdbfc")
        self.textRect = self.text.get_rect()
        self.textRect.center = (75, 25)

        self.seconds = seconds
        self.left_time = self.seconds

    def start(self):
        self.running = True
        self.startTime=pygame.time.get_ticks()

    def stop(self, win=False):
        self.running = False
        pygame.mixer.music.stop()
        if win:
            pass
        else:
            channel = death_snd.play()

    def draw(self):
        timePast = int((pygame.time.get_ticks() - self.startTime)/1000)
        if self.seconds-timePast < 0:
            self.stop()
            message = "Game Over"
        else:
            self.left_time = self.seconds-timePast
            minutes, seconds = divmod(self.seconds-timePast, 60)
            message = "%02d:%02d" % (minutes, seconds)
        self.text = self.font.render(message, True, "#222034", "#cbdbfc")
        self.screen.blit(self.text, self.textRect)

class Menu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font('kongtext.ttf', 24)
        self.text = self.font.render('00:00', True, "#222034", "#cbdbfc")
        self.textRect = self.text.get_rect()
        self.wait = False

    def main_menu(self):
        ...
    
    def end_game_menu(self):
        self.wait = True
        self.message = "press < Enter > for retry game"

        self.text = self.font.render(self.message, True, "#222034", "#cbdbfc")
        self.textRect = self.text.get_rect()
        self.textRect.center = (400, 300)
    
    def pause_menu():
        ...
    
    def scores_table():
        ...

    def get_status():
        ...

    def draw(self):
        self.screen.blit(self.text, self.textRect)


def game_main(music=True):
    pygame.display.set_caption('Horror Cube')
    icon = pygame.image.load('art/cubert-speed-circle.png')
    pygame.display.set_icon(icon)
    
    sound = pygame.mixer.music.load(os.path.join(".", "sounds", "game.wav"))
    #sound = pygame.mixer.Sound(os.path.join(".", "sounds", "game.ogg"))
    if music:
        pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode(screen_size)
    pygame.key.set_repeat(200)

    menu = Menu(screen)
    level = Level(screen, "01")
    cubert = level.getCubert()

    start_seconds = 30
    timer = Timer(screen, start_seconds)

    timer.start()
    if not cubert:
        print("Cubert is missing!")
        return

    running = True

    seconds_for_block = 10
    block_lvl=0
    last_block_time = 0

    while running:
        if (timer.left_time != start_seconds) and (timer.left_time != last_block_time) and (timer.left_time % seconds_for_block == 0):
            last_block_time = timer.left_time
            level.block_fields(lvl=block_lvl)
            block_lvl+=1

        level.draw()
        timer.draw()

        if menu.wait:
            menu.draw()

        for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    break
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                    break
                elif(timer.running):
                    cubert.update(event)  # Update Cubert.
                    cubert.draw()
                elif(menu.wait and event.type == KEYDOWN and event.key == K_RETURN):
                    game_main(True)


        if(not timer.running and not menu.wait):
            menu.end_game_menu()

        cubert.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game_main(True)
