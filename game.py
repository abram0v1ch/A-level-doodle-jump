from datetime import datetime
import time
import pygame
import random
import math
import os

# -- Global constants

# -- Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
GREEN = (75, 139, 59)
RED = (250, 10, 10)
PURPLE = (255, 0, 255)

# -- Initialise pygame and clock
pygame.init()

# variables needed for classes
prev = None  # records previous platform for player 1
prev2 = None  # records previous platform for player 2
highest = 0  # records highest platform for player 1
highest2 = 0  # records highest platform for player 2
up = False  # states if platforms should move down for player 1
player2 = None  # defines player2
score1 = 0  # defines score for player1
score2 = None  # defines score for player2
up2 = False  # states if platforms should move down for player 2
pmh = 575  # player's maximum height
hd = None  # defines by how much platforms should move down for player 1
hd2 = None  # defines by how much platforms should move down for player 2
kinds = ("regular", "movable", "ot")  # defines types of platforms
mods = (
    "none",
    "spring",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "helihat",
    "none",
    "none",
    "spring",
    "none",
    "none",
    "none",
    "none",
    "spring",
    "none",
    "none",
    "none",
    "none",
    "none",
    "none",
    "rocket",
    "none",
)  # helps in randomizing powerups for players

platform_number = 0  # records number of platforms

BASE_PATH = os.path.dirname(__file__)  # defines base path
FONT_PATH = os.path.join(BASE_PATH, "fonts")  # defines path to font directory
font = pygame.font.Font(
    os.path.join(FONT_PATH, "space_invaders.ttf"), 26
)  # defines font


class Player(pygame.sprite.Sprite):  # define player class
    def __init__(self, second=None):  # constructor
        super().__init__()  # initialize super class
        self.image = pygame.Surface([40, 40])  # define image
        self.image.fill(BLACK)  # fill figure
        # set the position of the sprite
        self.rect = self.image.get_rect()  # define shape
        if second != True:  # if not constructing second player
            self.rect.x = 260  # set this initial x position
            self.second = False  # set attribute of being a second player to false
        else:  # else
            self.rect.x = 260 + 650  # set this initial x position
            self.second = True  # set attribute of being a second player to true
        self.rect.y = 720  # set this initial y position
        self.score = 0  # zero the score
        self.speed = 40  # set initial speed
        self.mod = None  # remove all mods
        self.time = None  # remove time while used mod

    def update(self, change, platforms):  # update method
        # import global variables
        global up
        global hd

        global up2
        global hd2

        if (
            self.rect.y < 450
        ):  # if the player is higher than 450px from the upper boundary
            self.speed = 0  # stop the player
            self.rect.y = 450  # set its position
        if self.mod == "spring":  # if the player used string powerup
            if (
                time.time() - self.time <= 0.75
            ):  # if the player has been using it for less than 0.75s
                self.rect.y -= 20  # take the player up
                self.score += 8  # increse its score
            else:  # if the spring was used for more than 0.75s
                self.time = 0  # zero time while used powerup
                self.mod = None  # remove the powerup
        elif self.mod == "helihat":  # if the player is using helicopter hat
            if time.time() - self.time <= 2:  # if it's been for less than 2 seconds
                self.rect.y -= 20  # move player up
                self.score += 9  # add to the score
            else:  # else if it's been used for more than 2s
                self.time = 0  # zero time while using the powerup
                self.mod = None  # remove powerup
        elif self.mod == "rocket":  # if the player is using rocket powerup
            if time.time() - self.time <= 4:  # if it's been for less than 4s
                self.rect.y -= 20  # raise player
                self.score += 11  # add to the score
            else:  # else if it's been used more than 4s
                self.time = 0  # zero time while using powerup
                self.mod = None  # remove powerup
        else:  # if there are no poweups
            self.rect.y -= self.speed / 3  # update player's position
            if self.speed > 0:  # if moving up
                self.speed -= 2  # deccelerate
            if self.speed == 0:  # if stationary
                if self.second == False:  # if it's player1
                    up = False  # platforms for this player shouldn't move up
                    hd = self.rect.y - pmh  # update height difference value
                else:  # same for player2
                    up2 = False
                    hd2 = self.rect.y - pmh
                self.speed = -40  # define new speed for player
            if self.speed < 0:  # if player is moving down
                self.speed += 3  # deccelerate
        if not self.second:  # for player1
            self.rect.x += change  # process horizontal movements
            if (
                self.rect.x == -40
            ):  # if player1's almost gone to through the left boundary
                self.rect.x = 540  # leteport the player to the right boundary
            if self.rect.x == 550:  # same for left boundary
                self.rect.x = -30
        else:  # same for player 2
            self.rect.x += change_second
            if self.rect.x == 610:
                self.rect.x = 1190
            if self.rect.x == 1200:
                self.rect.x = -620

    def up(self):  # make player jump
        self.speed = 40

    def powerup(
        self, mod
    ):  # if got powerup, define new speed according to the type, set attribute mod to the type, start counting time
        if mod == "spring":
            self.speed = 80
        elif mod == "helihat":
            self.speed = 100
        else:
            self.speed = 120
        self.mod = mod
        self.time = time.time()

    def scoreup(
        self, num
    ):  # update the score based on the number of the highest platform reached
        if num * 50 > self.score:
            self.score = num * 50


class Shot(pygame.sprite.Sprite):  # define shot class
    def __init__(self, player, enemies):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # set position relative to player
        self.rect.y = player.rect.y
        self.rect.x = player.rect.x + 15
        self.speed = 10
        try:  # tryout for enemies
            y = 0
            # get the closest enemy
            for x in enemies:
                while y < 1:
                    enemy = x
                    y += 1
            if (
                player.rect.y >= enemy.rect.y
            ):  # if the closest enemy is higher than player
                self.enemy = enemy
                self.type = "directed"  # direct the shot at the enemy
            else:
                self.type = "straight"  # make the shot direct
        except UnboundLocalError:  # if no enemies are there
            self.type = "straight"  # mekt the shot direct

    def update(self):
        if self.type == "directed":  # if the shot is directed
            # calculate the shortest path to the enemy
            dx, dy = self.enemy.rect.x - self.rect.x, self.enemy.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist  # Normalize.
                # Move along this normalized vector towards the player at current speed.
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            if pygame.sprite.collide_rect(
                self, self.enemy
            ):  # if shot and enemy collide, kill both
                self.enemy.kill()
                self.kill()
        else:  # if the shot is direct, move it up
            self.rect.y -= self.speed
            if self.rect.y <= -5:  # if the shot is not seen, kill it
                self.kill()


class Platform(pygame.sprite.Sprite):  # define platform class
    def __init__(self, x, y, number, kind, mod, second=None):
        super().__init__()
        # define attributs
        self.image = pygame.Surface([60, 10])
        self.kind = kind
        if kind == "ot":  # if it's one time platform
            self.image.fill(RED)  # make it appear like this
        elif kind == "movable":  # if it's movable
            self.image.fill(BLUE)  # make it appear like this
            self.speed = 3  # define speed
        else:  # if it's a regular platform
            self.image.fill(GREEN)  # make it appear like this
        self.time = time.time()  # define creation time
        # set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = number
        if mod != "none":  # if the platform has a powerup
            self.powerup = Mod(mod, self)  # instantiate a powerup
        self.mod = mod
        self.second = second  # define if the platfrom is for player2

    def update(self, player):  # update method
        # import global variables
        global hd
        global hd2

        pl = player  # set temporaty variable for player
        if self.rect.x > 550:  # if the platform is on the right side of the screen
            hed = hd2  # treat it as a platform for player 2
        else:  # else it's for player 1
            hed = hd
        if pl.mod == "spring":  # if the player uses spring
            hm = (545 - 450) / (
                10 - 2
            )  # that's how much the platfrom should go down by
        elif pl.mod == "helihat":  # same for helicopter hat
            hm = (545 - 450) / (10 - 4)
        elif pl.mod == "rocket":  # same for rocket
            hm = (545 - 450) / (10 - 6)
        else:  # same while not using powerups
            hm = abs(hed) / (10)
        if self.mod != "none":  # if a platform has a powerup
            self.powerup.update(hm)  # move powerup by the same number of pixels

        self.rect.y += hm  # move platfrom
        if (
            self.rect.y >= 820
        ):  # if it's not seen, kill it and its powerupd (if present)
            if self.mod != "none":
                self.powerup.kill()
            self.kill()

    def move(self):  # define moving function (for movable platforms)
        if self.second == None:  # if the platfrom is for player1, move it in this range
            if self.rect.x >= 490:
                self.speed = -3
            elif self.rect.x <= 0:
                self.speed = 3
        else:  # if the platform is for player2, move it in this range
            if self.rect.x >= 1140:
                self.speed = -3
            elif self.rect.x <= 650:
                self.speed = 3
        self.rect.x += self.speed  # update position
        if self.mod != "none":  # if there's a powerup, move it too
            self.powerup.move(self.speed)


class Enemy(pygame.sprite.Sprite):  # derine enemy class
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(BLACK)
        # set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        if self.rect.x >= 550:
            self.second = True
        else:
            self.second = False
        self.rect.y = y
        self.change = 2
        self.inx = x

    def update(self, player):
        global hd
        global hd2

        pl = player
        if self.second == False:
            hed = hd
        else:
            hed = hd2

        if pl.mod == "spring":
            hm = (545 - 450) / (10 - 2)
        elif pl.mod == "helihat":
            hm = (545 - 450) / (10 - 4)
        elif pl.mod == "rocket":
            hm = (545 - 450) / (10 - 6)
        else:
            hm = abs(hed) / (10)
        self.rect.y += hm
        if self.rect.y >= 820:
            self.kill()

    def move(self):
        self.rect.x += self.change
        if self.rect.x - self.inx == 50:
            self.change *= -1
        if self.rect.x - self.inx == -50:
            self.change *= -1


class Mod(pygame.sprite.Sprite):
    def __init__(self, kind, platform):
        super().__init__()
        if kind == "spring":
            self.image = pygame.Surface([15, 15])
            self.rect = self.image.get_rect()
            self.rect.y = platform.rect.y - 15
            self.rect.x = platform.rect.x + 22.5
        elif kind == "rocket":
            self.image = pygame.Surface([15, 25])
            self.rect = self.image.get_rect()
            self.rect.y = platform.rect.y - 25
            self.rect.x = platform.rect.x + 22.5
        else:
            self.image = pygame.Surface([25, 15])
            self.rect = self.image.get_rect()
            self.rect.y = platform.rect.y - 15
            self.rect.x = platform.rect.x + 17.5
        self.image.fill(PURPLE)
        self.kind = kind
        powerups.add(self)

    def update(self, hm):
        self.rect.y += hm

    def move(self, hm):
        self.rect.x += hm


# -- Blank screen
size = (550, 800)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("My Window")

# -- Exit game flag set to false
done = False
change = 0
change_second = 0

# -- Manages how fast clock refreshes
clock = pygame.time.Clock()

player = Player()
group = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
shots = pygame.sprite.Group()
powerups = pygame.sprite.Group()
group.add(player)


def main():
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game()
                if event.key == pygame.K_m:
                    local_multi()
        screen.fill(WHITE)
        text1 = font.render("Jumpy", False, PURPLE)
        text2 = font.render("[S] singleplayer game", False, PURPLE)
        text3 = font.render("[M] multiplayer game", False, PURPLE)
        screen.blit(text1, (50, 1))
        screen.blit(text2, (20, 31))
        screen.blit(text3, (20, 61))
        pygame.display.flip()
        clock.tick(60)


def end():
    global score1
    global score2
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game()
                    score1 = 0
                    score2 = None
                if event.key == pygame.K_m:
                    local_multi()
                    score1 = 0
                    score2 = None
                if event.key == pygame.K_q:
                    exit()
        screen.fill(WHITE)
        if score2 == None:
            text1 = font.render("Game over", False, PURPLE)
            text2 = font.render("Score:" + str(score1), False, PURPLE)
            text3 = font.render(
                "[Q] quit, [S] singleplayer, [M] multiplayer", False, PURPLE
            )
            screen.blit(text1, (50, 1))
            screen.blit(text2, (50, 31))
            screen.blit(text3, (20, 61))
        else:
            text1 = font.render("Game over", False, PURPLE)
            if score1 > score2:
                text2 = font.render(
                    "Player 1 won. Scores" + str(score1) + ":" + str(score2),
                    False,
                    PURPLE,
                )
            else:
                text2 = font.render(
                    "Player 2 won. Scores" + str(score1) + ":" + str(score2),
                    False,
                    PURPLE,
                )
            text3 = font.render("[Q] quit, [S] singleplayer, [M] multiplayer")
            screen.blit(text1, (450, 1))
            screen.blit(text2, (20, 31))
            screen.blit(text3, (300, 61))
        pygame.display.flip()
        clock.tick(60)


def pause():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    done = True
                if event.key == pygame.K_q:
                    exit()
        screen.fill(WHITE)
        text1 = font.render("Pause menu", False, PURPLE)
        text2 = font.render("[Q] quit, [S] continue", False, PURPLE)
        screen.blit(text1, (50, 1))
        screen.blit(text2, (40, 31))
        pygame.display.flip()
        clock.tick(60)


###-- Game function
def game():
    global platform_number
    global change
    global up
    global highest
    global pmh
    global prev
    global hd
    global kinds
    global mods
    global done
    global player
    global group
    global platforms
    global enemies
    global shots
    global powerups
    global score1

    size = (550, 800)
    screen = pygame.display.set_mode(size)

    while not done:
        # -- User inputs here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change = -10
                elif event.key == pygame.K_RIGHT:
                    change = 10
                if event.key == pygame.K_ESCAPE:
                    pause()
                if (
                    event.key == pygame.K_SPACE
                    and player.mod != "rocket"
                    and player.mod != "helihat"
                ):
                    shots.add(Shot(player, enemies))
                    # endif
            elif event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_RIGHT
                    or event.key == pygame.K_UP
                    or event.key == pygame.K_DOWN
                ):
                    change = 0
                # endif
            # endif
        # Game logic goes after this comment
        max_h = 800
        while len(platforms) < 24:
            if len(platforms) > 0:
                for x in platforms:
                    if x.rect.y < max_h:
                        max_h = x.rect.y
                kind = random.choice(kinds)
                x = random.randint(0, 490)
                if kind == "ot":
                    mod = "none"
                else:
                    mod = random.choice(mods)
                platforms.add(Platform(x, max_h - 115, platform_number, kind, mod))
                kd = random.choice(["regular", "ot"])
                if kd == "ot":
                    md = "none"
                else:
                    md = random.choice(mods)
                if player.score < 15000:
                    if x < 250:
                        platforms.add(
                            Platform(x + 200, max_h + 175, platform_number, kd, md)
                        )
                    elif x >= 250:
                        platforms.add(
                            Platform(x - 200, max_h + 175, platform_number, kd, md)
                        )
                elif player.score > 25000 and player.score < 40000:
                    if x < 250:
                        platforms.add(
                            Platform(x + 200, max_h - 175, platform_number, kd, md)
                        )
                    elif x >= 250:
                        platforms.add(
                            Platform(x - 200, max_h - 175, platform_number, kd, md)
                        )
                else:
                    pass
                platform_enemy = random.choice(
                    [
                        "platform",
                        "platform",
                        "platform",
                        "platfrom",
                        "platform",
                        "platform",
                        "platform",
                        "enemy",
                        "platform",
                        "platform",
                    ]
                )
                enemy = random.choice(
                    ["no", "no", "no", "no", "no", "no", "no", "no", "no", "yes", "no"]
                )
                if kind == "ot":
                    if x < 250:
                        if platform_enemy == "platform":
                            platforms.add(
                                Platform(
                                    x + 200,
                                    max_h - 115,
                                    platform_number,
                                    "regular",
                                    random.choice(mods),
                                )
                            )
                        elif len(enemies) == 0:
                            enemies.add(Enemy(x + 250, max_h - 110))
                    if x >= 250:
                        if platform_enemy == "platform":
                            platforms.add(
                                Platform(
                                    x - 200,
                                    max_h - 110,
                                    platform_number,
                                    "regular",
                                    random.choice(mods),
                                )
                            )
                        else:
                            enemies.add(Enemy(x - 250, max_h - 125))
                if kind == "regular":
                    if x < 250:
                        if enemy == "yes" and len(enemies) == 0:
                            enemies.add(Enemy(x + 250, max_h - 125))
                    if x >= 250:
                        if enemy == "yes" and len(enemies) == 0:
                            enemies.add(Enemy(x - 250, max_h - 125))
                platform_number += 1
                time.sleep(0.000001)
            else:
                platforms.add(Platform(240, 760, platform_number, "regular", "none"))
                platform_number += 1
                time.sleep(0.000001)

        # Screen background is BLACK
        screen.fill(WHITE)

        for x in range(40):
            if x == 3:
                pygame.draw.line(screen, RED, (x * 20, 0), (x * 20, 800))
            elif x >= 0 and x <= 27:
                pygame.draw.line(screen, (222, 222, 222), (x * 20, 0), (x * 20, 800))
            pygame.draw.line(screen, (222, 222, 222), (0, x * 20), (550, x * 20))

        for x in enemies:
            x.move()
            if pygame.sprite.collide_rect(player, x):
                if player.mod != None and player.mod != "spring":
                    x.kill()
                elif player.speed < 0 and player.rect.y < x.rect.y:
                    x.kill()
                    player.up()
                else:
                    done = True

        platforms.draw(screen)
        powerups.draw(screen)
        group.draw(screen)
        shots.draw(screen)
        enemies.draw(screen)
        player.update(change, platforms)
        shots.update()
        score_text = font.render(str(player.score), False, PURPLE)
        screen.blit(score_text, (460, 1))
        if player.rect.y < 500:
            up = True
        if up:
            platforms.update(player)
            enemies.update(player)
        for x in platforms:
            if x.kind == "movable":
                x.move()
            if player.speed < 0 and pygame.sprite.collide_rect(player, x):
                if prev != None:
                    if highest - x.time < 0:
                        # up = True
                        pass
                prev = x.time
                if prev > highest:
                    highest = prev
                    player.scoreup(x.number)
                if x.kind == "ot":
                    x.kill()
                if (
                    player.mod == None
                    and x.mod != "none"
                    and pygame.sprite.collide_rect(player, x.powerup)
                ):
                    player.powerup(x.mod)
                    x.powerup.kill()
                else:
                    player.up()

        if player.rect.y >= 760:
            score1 = player.score
            done = True
            break

        # --flip display to reveal new position of objects
        pygame.display.flip()
        clock.tick(60)
    if done == True:
        player = Player()
        group.empty()
        platforms.empty()
        enemies.empty()
        shots.empty()
        powerups.empty()
        group.add(player)
        prev = None
        highest = 0
        up = False
        pmh = 575
        hd = None
        platform_number = 0
        done = False
        change = 0
        end()


def local_multi():
    global platform_number
    global change
    global up
    global up2
    global highest
    global pmh
    global prev
    global hd
    global kinds
    global mods
    global done
    global player
    global group
    global platforms
    global enemies
    global shots
    global powerups
    global change_second
    global highest2
    global prev2
    global hd2
    global player2

    platform_number2 = 0
    player1_end = False
    player2_end = False

    size = (1200, 800)
    screen = pygame.display.set_mode(size)

    player2 = Player(second=True)
    group.add(player2)
    platforms2 = pygame.sprite.Group()
    enemies2 = pygame.sprite.Group()
    shots2 = pygame.sprite.Group()
    powerups2 = pygame.sprite.Group()

    while not done:
        # -- User inputs here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player2_end == False:
                    change_second = -10
                elif event.key == pygame.K_RIGHT and player2_end == False:
                    change_second = 10
                if event.key == pygame.K_ESCAPE:
                    pause()
                if (
                    event.key == pygame.K_RCTRL
                    and player2.mod != "rocket"
                    and player2.mod != "helihat"
                    and player2_end == False
                ):
                    shots.add(Shot(player2, enemies2))
                if event.key == pygame.K_a and player1_end == False:
                    change = -10
                elif event.key == pygame.K_d and player1_end == False:
                    change = 10
                if (
                    event.key == pygame.K_LSHIFT
                    and player.mod != "rocket"
                    and player.mod != "helihat"
                    and player1_end == False
                ):
                    shots.add(Shot(player, enemies))
                    # endif
            elif event.type == pygame.KEYUP:
                if (
                    event.key == pygame.K_LEFT
                    or event.key == pygame.K_RIGHT
                    and player2_end == False
                ):
                    change_second = 0
                if (
                    event.key == pygame.K_a
                    or event.key == pygame.K_d
                    and player1_end == False
                ):
                    change = 0
                # endif
            # endif

        # Screen background is BLACK
        screen.fill(WHITE)

        for x in range(40):
            if x == 3:
                pygame.draw.line(screen, RED, (x * 20, 0), (x * 20, 800))
            elif x >= 0 and x <= 27:
                pygame.draw.line(screen, (222, 222, 222), (x * 20, 0), (x * 20, 800))
            pygame.draw.line(screen, (222, 222, 222), (0, x * 20), (550, x * 20))

        # Game logic goes after this comment
        max_h = 800
        max_h2 = 800
        if player1_end == False:
            while len(platforms) < 24:
                if len(platforms) > 0:
                    for x in platforms:
                        if x.rect.y < max_h:
                            max_h = x.rect.y
                    kind = random.choice(kinds)
                    x = random.randint(0, 490)
                    if kind == "ot":
                        mod = "none"
                    else:
                        mod = random.choice(mods)
                    platforms.add(Platform(x, max_h - 115, platform_number, kind, mod))
                    kd = random.choice(["regular", "ot"])
                    if kd == "ot":
                        md = "none"
                    else:
                        md = random.choice(mods)
                    if player.score < 15000:
                        if x < 250:
                            platforms.add(
                                Platform(x + 200, max_h + 175, platform_number, kd, md)
                            )
                        elif x >= 250:
                            platforms.add(
                                Platform(x - 200, max_h + 175, platform_number, kd, md)
                            )
                    elif player.score > 25000 and player.score < 40000:
                        if x < 250:
                            platforms.add(
                                Platform(x + 200, max_h - 175, platform_number, kd, md)
                            )
                        elif x >= 250:
                            platforms.add(
                                Platform(x - 200, max_h - 175, platform_number, kd, md)
                            )
                    else:
                        pass
                    platform_enemy = random.choice(
                        [
                            "platform",
                            "platform",
                            "platform",
                            "platfrom",
                            "platform",
                            "platform",
                            "platform",
                            "enemy",
                            "platform",
                            "platform",
                        ]
                    )
                    enemy = random.choice(
                        [
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "yes",
                            "no",
                        ]
                    )
                    if kind == "ot":
                        if x < 250:
                            if platform_enemy == "platform":
                                platforms.add(
                                    Platform(
                                        x + 200,
                                        max_h - 115,
                                        platform_number,
                                        "regular",
                                        random.choice(mods),
                                    )
                                )
                            elif len(enemies) == 0:
                                enemies.add(Enemy(x + 250, max_h - 110))
                        if x >= 250:
                            if platform_enemy == "platform":
                                platforms.add(
                                    Platform(
                                        x - 200,
                                        max_h - 110,
                                        platform_number,
                                        "regular",
                                        random.choice(mods),
                                    )
                                )
                            else:
                                enemies.add(Enemy(x - 250, max_h - 125))
                    if kind == "regular":
                        if x < 250:
                            if enemy == "yes" and len(enemies) == 0:
                                enemies.add(Enemy(x + 250, max_h - 125))
                        if x >= 250:
                            if enemy == "yes" and len(enemies) == 0:
                                enemies.add(Enemy(x - 250, max_h - 125))
                    platform_number += 1
                    time.sleep(0.000001)
                else:
                    platforms.add(
                        Platform(240, 760, platform_number, "regular", "none")
                    )
                    platform_number += 1
                    time.sleep(0.000001)

            for x in enemies:
                x.move()
                if pygame.sprite.collide_rect(player, x):
                    if player.mod != None and player.mod != "spring":
                        x.kill()
                    elif player.speed < 0 and player.rect.y < x.rect.y:
                        x.kill()
                        player.up()
                    else:
                        done = True

            platforms.draw(screen)
            powerups.draw(screen)
            group.draw(screen)
            shots.draw(screen)
            enemies.draw(screen)
            player.update(change, platforms)
            shots.update()

            score_text = font.render(str(player.score), False, PURPLE)
            screen.blit(score_text, (460, 1))

            if player.rect.y < 500:
                up = True
            if up:
                platforms.update(player)
                enemies.update(player)
            for x in platforms:
                if x.kind == "movable":
                    x.move()
                if player.speed < 0 and pygame.sprite.collide_rect(player, x):
                    if prev != None:
                        if highest - x.time < 0:
                            # up = True
                            pass
                    prev = x.time
                    if prev > highest:
                        highest = prev
                        player.scoreup(x.number)
                    if x.kind == "ot":
                        x.kill()
                    if (
                        player.mod == None
                        and x.mod != "none"
                        and pygame.sprite.collide_rect(player, x.powerup)
                    ):
                        player.powerup(x.mod)
                        x.powerup.kill()
                    else:
                        player.up()
        else:
            p1et = font.render("Game over, score:" + str(player.score), False, PURPLE)
            screen.blit(p1et, (250, 200))

        if player2_end == False:
            while len(platforms2) < 24:
                if len(platforms2) > 0:
                    for x in platforms2:
                        if x.rect.y < max_h2:
                            max_h2 = x.rect.y
                    kind = random.choice(kinds)
                    x = random.randint(0, 490)
                    if kind == "ot":
                        mod = "none"
                    else:
                        mod = random.choice(mods)
                    platforms2.add(
                        Platform(
                            x + 650,
                            max_h2 - 115,
                            platform_number2,
                            kind,
                            mod,
                            second=True,
                        )
                    )
                    kd = random.choice(["regular", "ot"])
                    if kd == "ot":
                        md = "none"
                    else:
                        md = random.choice(mods)
                    if player2.score < 15000:
                        if x < 250:
                            platforms2.add(
                                Platform(
                                    x + 200 + 650,
                                    max_h2 + 175,
                                    platform_number2,
                                    kd,
                                    md,
                                    second=True,
                                )
                            )
                        elif x >= 250:
                            platforms2.add(
                                Platform(
                                    x - 200 + 650,
                                    max_h2 + 175,
                                    platform_number2,
                                    kd,
                                    md,
                                    second=True,
                                )
                            )
                    elif player2.score > 25000 and player2.score < 40000:
                        if x < 250:
                            platforms2.add(
                                Platform(
                                    x + 200 + 650,
                                    max_h2 - 175,
                                    platform_number2,
                                    kd,
                                    md,
                                    second=True,
                                )
                            )
                        elif x >= 250:
                            platforms2.add(
                                Platform(
                                    x - 200 + 650,
                                    max_h2 - 175,
                                    platform_number2,
                                    kd,
                                    md,
                                    second=True,
                                )
                            )
                    else:
                        pass
                    platform_enemy = random.choice(
                        [
                            "platform",
                            "platform",
                            "platform",
                            "platfrom",
                            "platform",
                            "platform",
                            "platform",
                            "enemy",
                            "platform",
                            "platform",
                        ]
                    )
                    enemy = random.choice(
                        [
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "no",
                            "yes",
                            "no",
                        ]
                    )
                    if kind == "ot":
                        if x < 250:
                            if platform_enemy == "platform":
                                platforms2.add(
                                    Platform(
                                        x + 200 + 650,
                                        max_h2 - 115,
                                        platform_number2,
                                        "regular",
                                        random.choice(mods),
                                        second=True,
                                    )
                                )
                            elif len(enemies2) == 0:
                                enemies2.add(Enemy(x + 250 + 650, max_h2 - 110))
                        if x >= 250:
                            if platform_enemy == "platform":
                                platforms2.add(
                                    Platform(
                                        x - 200 + 650,
                                        max_h2 - 110,
                                        platform_number2,
                                        "regular",
                                        random.choice(mods),
                                        second=True,
                                    )
                                )
                            else:
                                enemies2.add(Enemy(x - 250 + 650, max_h2 - 125))
                    if kind == "regular":
                        if x < 250:
                            if enemy == "yes" and len(enemies2) == 0:
                                enemies2.add(Enemy(x + 250 + 650, max_h2 - 125))
                        if x >= 250:
                            if enemy == "yes" and len(enemies2) == 0:
                                enemies.add(Enemy(x - 250 + 650, max_h2 - 125))
                    platform_number2 += 1
                    time.sleep(0.000001)
                else:
                    platforms2.add(
                        Platform(
                            240 + 650,
                            760,
                            platform_number2,
                            "regular",
                            "none",
                            second=True,
                        )
                    )
                    platform_number2 += 1
                    time.sleep(0.000001)

            for x in enemies2:
                x.move()
                if pygame.sprite.collide_rect(player2, x):
                    if player2.mod != None and player2.mod != "spring":
                        x.kill()
                    elif player2.speed < 0 and player2.rect.y < x.rect.y:
                        x.kill()
                        player2.up()
                    else:
                        done = True

            platforms2.draw(screen)
            powerups2.draw(screen)
            shots2.draw(screen)
            enemies2.draw(screen)
            player2.update(change, platforms2)
            shots2.update()

            score_text2 = font.render(str(player2.score), False, PURPLE)
            screen.blit(score_text2, (460 + 650, 1))

            if player2.rect.y < 500:
                up2 = True
            if up2:
                platforms2.update(player2)
                enemies2.update(player2)
            for x in platforms2:
                if x.kind == "movable":
                    x.move()
                if player2.speed < 0 and pygame.sprite.collide_rect(player2, x):
                    if prev2 != None:
                        if highest2 - x.time < 0:
                            # up = True
                            pass
                    prev2 = x.time
                    if prev2 > highest2:
                        highest2 = prev2
                        player2.scoreup(x.number)
                    if x.kind == "ot":
                        x.kill()
                    if (
                        player2.mod == None
                        and x.mod != "none"
                        and pygame.sprite.collide_rect(player2, x.powerup)
                    ):
                        player2.powerup(x.mod)
                        x.powerup.kill()
                    else:
                        player2.up()
        else:
            p2et = font.render("Game over, score:" + str(player2.score), False, PURPLE)
            screen.blit(p2et, (250 + 650, 200))

        if player.rect.y >= 780:
            player1_end = True
            score1 = player.score

        if player2.rect.y >= 780:
            player2_end = True
            score2 = player2.score

        if player1_end == True and player2_end == True:
            done = True
            break

        # --flip display to reveal new position of objects
        pygame.display.flip()
        clock.tick(60)
    if done == True:
        player = Player()
        group.empty()
        platforms.empty()
        enemies.empty()
        shots.empty()
        powerups.empty()
        group.add(player)
        prev = None
        player2 = None
        player1_end = False
        player2_end = False
        highest = 0
        up = False
        pmh = 575
        hd = None
        platform_number = 0
        done = False
        change = 0
        change_second = 0
        platform_number2 = 0
        platforms2.empty()
        enemies2.empty()
        shots2.empty()
        powerups2.empty()
        up2 = 0
        highest2 = 0
        prev2 = 0
        hd2 = 0
        end()


main()

###--End of game loop
pygame.quit()

# 150-2600 - travelled by rocket
# 400-650 - travelled by spring
# 2350-3250 - travelled by helihat
