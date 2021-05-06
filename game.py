from datetime import datetime
import time
import pygame
import random
import math
#-- Global constants

#-- Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
GREEN = (75, 139, 59)
RED = (250, 10, 10)
PURPLE = (255, 0, 255)

#-- Initialise pygame and clock
pygame.init()

#variables needed for classes
prev = None
highest = 0
up = False
pmh = 575
hd = None
kinds = ['regular', 'movable', 'ot']
mods = ['none', 'spring', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'helihat', 'none', 'none', 'spring', 'none', 'none', 'none', 'none', 'spring', 'none', 'none', 'none', 'none', 'none', 'none', 'rocket', 'none']

platform_number = 0

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([40, 40])
		self.image.fill(BLACK)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = 260
		self.rect.y = 720
		self.score = 0
		self.speed = 40
		self.mod = None
		self.time = None

	def update(self, change, platforms):
		global up
		global hd
		if self.rect.y < 450:
			self.speed = 0
			self.rect.y += 20
		if self.mod == 'spring':
			if time.time() - self.time <= 0.75:
				self.rect.y -= 20
			else:
				self.time = 0
				self.mod = None
		elif self.mod == 'helihat':
			if time.time() - self.time <= 2:
				self.rect.y -= 20
			else:
				self.time = 0
				self.mod = None
		elif self.mod == 'rocket':
			if time.time() - self.time <= 4:
				self.rect.y -= 20
			else:
				self.time = 0
				self.mod = None
		else:
			self.rect.y -= self.speed/3
			if self.speed > 0:
				self.speed -= 2
			if self.speed == 0:
				up = False
				hd = self.rect.y - pmh
				self.speed = -40
			if self.speed < 0:
				self.speed += 3
		self.rect.x += change
		if self.rect.x == -40:
			self.rect.x = 540
		if self.rect.x == 550:
			self.rect.x = -30

	def up(self):
		self.speed = 40

	def powerup(self, mod):
		if mod == 'spring':
			self.speed = 80
		elif mod == 'helihat':
			self.speed = 100
		else:
			self.speed = 120
		self.mod = mod
		self.time = time.time()

	def scoreup(self, num):
		if num*50 > self.score:
			self.score = num*50


class Shot(pygame.sprite.Sprite):
	def __init__(self, player, enemies):
		super().__init__()
		self.image = pygame.Surface([10,10])
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.y = player.rect.y
		self.rect.x = player.rect.x + 15
		self.speed = 10
		try:
			y = 0
			for x in enemies:
				while y < 1:
					enemy = x
					y += 1
			if player.rect.y >= enemy.rect.y:
				self.enemy = enemy
				self.type = 'directed'
			else:
				self.type = 'straight'
		except UnboundLocalError:
			self.type = 'straight'

	def update(self):
		if self.type == 'directed':
			dx, dy = self.enemy.rect.x - self.rect.x, self.enemy.rect.y - self.rect.y
			dist = math.hypot(dx, dy)
			if dist != 0:
				dx, dy = dx / dist, dy / dist  # Normalize.
				# Move along this normalized vector towards the player at current speed.
				self.rect.x += dx * self.speed
				self.rect.y += dy * self.speed
			if pygame.sprite.collide_rect(self, self.enemy):
				self.enemy.kill()
				self.kill()
		else:
			self.rect.y -= self.speed
			if self.rect.y <= -5:
				self.kill()


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, number, kind, mod):
		super().__init__()
		self.image = pygame.Surface([60, 10])
		self.kind = kind
		if kind == 'ot':
			self.image.fill(RED)
		elif kind == 'movable':
			self.image.fill(BLUE)
			self.speed = 3
		else:
			self.image.fill(GREEN)
		self.time = time.time()
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.number = number
		if mod != 'none':
			self.powerup = Mod(mod, self)
		self.mod = mod

	def update(self, player):
		global hd
		if player.mod == 'spring':
			hm = (545-450)/(10-2)
		elif player.mod == 'helihat':
			hm = (545-450)/(10-4)
		elif player.mod == 'rocket':
			hm = (545-450)/(10-6)
		else:
			hm = abs(hd)/(10)
		if self.mod != 'none':
			self.powerup.update(hm)

		self.rect.y += hm
		if self.rect.y >= 800:
			if self.mod != 'none':
				self.powerup.kill()
			self.kill()

	def move(self):
		if self.rect.x >= 490:
			self.speed = -3
		elif self.rect.x <= 0:
			self.speed = 3
		self.rect.x += self.speed
		if self.mod != 'none':
			self.powerup.move(self.speed)


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface([40, 40])
		self.image.fill(BLACK)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.change = 5
		self.inx = x

	def update(self, player):
		global hd

		if player.mod == 'spring':
			hm = (545-450)/(10-2)
		elif player.mod == 'helihat':
			hm = (545-450)/(10-4)
		elif player.mod == 'rocket':
			hm = (545-450)/(10-6)
		else:
			hm = abs(hd)/(10)
		self.rect.y += hm
		if self.rect.y >= 800:
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
		if kind == 'spring':
			self.image = pygame.Surface([15, 15])
			self.rect = self.image.get_rect()
			self.rect.y = platform.rect.y - 15
			self.rect.x = platform.rect.x + 22.5
		elif kind == 'rocket':
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

#-- Blank screen
size = (550,800)
screen = pygame.display.set_mode(size)

#-- Title of new window/screen
pygame.display.set_caption('My Window')

#-- Exit game flag set to false
done = False
change = 0

#-- Manages how fast clock refreshes
clock = pygame.time.Clock()

player = Player()
group = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
shots = pygame.sprite.Group()
powerups = pygame.sprite.Group()
group.add(player)

###-- Game Loop
while not done:
	#-- User inputs here
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				change = -10
			elif event.key == pygame.K_RIGHT:
				change = 10
			if event.key == pygame.K_SPACE:
				shots.add(Shot(player, enemies))
			 #endif
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				change = 0
			#endif
		#endif
	# Game logic goes after this comment
	max_h = 800
	while len(platforms) < 24:
		if len(platforms) > 0:
			for x in platforms:
				if x.rect.y < max_h:
					max_h = x.rect.y
			kind = random.choice(kinds)
			x = random.randint(0, 490)
			if kind == 'ot':
				mod = 'none'
			else:
				mod = random.choice(mods)
			platforms.add(Platform(x, max_h-115, platform_number, kind, mod))
			kd = random.choice(['regular', 'ot'])
			if kd == 'ot':
				md = 'none'
			else:
				md = random.choice(mods)
			if player.score < 10000:
				if x < 250:
					platforms.add(Platform(x+200, max_h+175, platform_number, kd, md))
				elif x >= 250:
					platforms.add(Platform(x-200, max_h+175, platform_number, kd, md))
			elif player.score > 10000 and player.score < 20000:
				if x < 250:
					platforms.add(Platform(x+200, max_h-175, platform_number, kd, md))
				elif x >= 250:
					platforms.add(Platform(x-200, max_h-175, platform_number, kd, md))
			else:
				pass
			platform_enemy = random.choice(['platform', 'platform', 'platform', 'platfrom', 'platform', 'platform', 'platform', 'enemy', 'platform', 'platform'])
			enemy = random.choice(['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'])
			if kind == 'ot':
				if x < 250:
					if platform_enemy == 'platform':
						platforms.add(Platform(x+200, max_h-115, platform_number, 'regular', random.choice(mods)))
					elif len(enemies) == 0:
						enemies.add(Enemy(x+250, max_h-110))
				if x >= 250:
					if platform_enemy == 'platform':
						platforms.add(Platform(x-200, max_h-110, platform_number, 'regular', random.choice(mods)))
					else:
						enemies.add(Enemy(x-250, max_h-125))
			if kind == 'regular':
				if x < 250:
					if enemy == 'yes' and len(enemies) == 0:
						enemies.add(Enemy(x+250, max_h-125))
				if x >= 250:
					if enemy == 'yes' and len(enemies) == 0:
						enemies.add(Enemy(x-250, max_h-125))
			platform_number += 1
			time.sleep(0.000001)
		else:
			platforms.add(Platform(240, 760, platform_number, 'regular', 'none'))
			platform_number += 1
			time.sleep(0.000001)

	# Screen background is BLACK
	screen.fill(WHITE)

	for x in range(40):
		pygame.draw.line(screen, (222,222,222), (x * 20, 0), (x * 20, 800))
		pygame.draw.line(screen, (222,222,222), (0, x * 20), (550, x * 20))

	for x in enemies:
		x.move()

	platforms.draw(screen)
	group.draw(screen)
	shots.draw(screen)
	enemies.draw(screen)
	powerups.draw(screen)
	player.update(change, platforms)
	shots.update()
	if player.rect.y < 500:
		up = True
	if up:
		platforms.update(player)
		enemies.update(player)
	for x in platforms:
		if x.kind == 'movable':
			x.move()
		if player.speed < 0 and pygame.sprite.collide_rect(player, x):
			if prev != None:
				if highest-x.time < 0:
					#up = True
					pass
			prev = x.time
			if prev > highest:
				highest = prev
				player.scoreup(x.number)
			if x.kind == 'ot':
				x.kill()
			if x.mod != 'none' and pygame.sprite.collide_rect(player, x.powerup):
				player.powerup(x.mod)
			else:
				player.up()

	print(player.score)

	#--flip display to reveal new position of objects
	pygame.display.flip()
	clock.tick(60)

###--End of game loop
pygame.quit()
	
