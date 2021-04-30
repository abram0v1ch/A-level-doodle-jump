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

#-- Initialise pygame and clock
pygame.init()

#variables needed for classes
prev = None
highest = 0
up = False
pmh = 575
hd = None
kinds = ['regular', 'movable', 'ot']
mods = ['spring', 'helihat', 'rocket', 'none']

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

	def update(self, change, platforms):
		global up
		global hd
		if self.rect.y < 450:
			self.speed = 0
			self.rect.y += 20
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
	def __init__(self, x, y, number, kind):
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

	def update(self, player):
		global hd

		self.rect.y += abs(hd)/(10)
		if self.rect.y >= 800:
			self.kill()

	def move(self):
		if self.rect.x >= 490:
			self.speed = -3
		elif self.rect.x <= 0:
			self.speed = 3
		self.rect.x += self.speed


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

		self.rect.y += abs(hd)/(10)
		if self.rect.y >= 800:
			self.kill()

	def move(self):
		self.rect.x += self.change
		if self.rect.x - self.inx == 50:
			self.change *= -1
		if self.rect.x - self.inx == -50:
			self.change *= -1

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
	while len(platforms) < 14:
		if len(platforms) > 0:
			for x in platforms:
				if x.rect.y < max_h:
					max_h = x.rect.y
			kind = random.choice(kinds)
			x = random.randint(0, 490)
			platforms.add(Platform(x, max_h-115, platform_number, kind))
			if x < 250:
				platforms.add(Platform(x+200, max_h-175, platform_number, random.choice(['regular', 'ot'])))
			if x >= 250:
				platforms.add(Platform(x-200, max_h-175, platform_number, random.choice(['regular', 'ot'])))
			platform_enemy = random.choice(['platform', 'platform', 'platform', 'platfrom', 'platform', 'platform', 'platform', 'enemy', 'platform', 'platform'])
			enemy = random.choice(['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'])
			if kind == 'ot':
				if x < 250:
					if platform_enemy == 'platform':
						platforms.add(Platform(x+200, max_h-115, platform_number, 'regular'))
					elif len(enemies) == 0:
						enemies.add(Enemy(x+250, max_h-110))
				if x >= 250:
					if platform_enemy == 'platform':
						platforms.add(Platform(x-200, max_h-110, platform_number, 'regular'))
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
			platforms.add(Platform(240, 760, platform_number, 'regular'))
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
			player.up()

	print(player.score)

	#--flip display to reveal new position of objects
	pygame.display.flip()
	clock.tick(60)

###--End of game loop
pygame.quit()
	
