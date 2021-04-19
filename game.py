from datetime import datetime
import time
import pygame
import random
#-- Global constants

#-- Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
GREEN = (75, 139, 59)

#-- Initialise pygame and clock
pygame.init()

#variables needed for classes
prev = None
highest = 0
up = False
kinds = ['regular', 'movable', 'ot']
mods = ['spring', 'helihat', 'rocket', 'none']

platform_number = 0

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([40, 40])
		self.image.fill(YELLOW)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = 260
		self.rect.y = 720
		self.score = 0
		self.speed = 48

	def update(self, change, platforms):
		global up
		self.rect.y -= self.speed/3
		if self.speed > 0:
			self.speed -= 3
		if self.speed == 0:
			self.speed = -33
		if self.speed < 0:
			up = False
			self.speed += 3
		self.rect.x += change
		if self.rect.x == -40:
			self.rect.x = 540
		if self.rect.x == 550:
			self.rect.x = -30

	def up(self):
		self.speed = 48

	def down(self, hm):
		self.rect.y += hm

	def scoreup(self, num):
		if num*50 > self.score:
			self.score = num*50


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, number, kind):
		super().__init__()
		self.image = pygame.Surface([60, 10])
		self.kind = kind
		if kind == 'ot':
			self.image.fill(WHITE)
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
		if player.rect.y > 400:
			hm = player.speed/3
			self.rect.y += hm
		elif player.rect.y < 300 and player.rect.y > 200:
			hm = player.speed/2.5
			self.rect.y += hm
			# player.down(20)
		elif player.rect.y < 200 and player.rect.y > 100:
			hm = player.speed
			self.rect.y += hm
			# player.down(40)
		elif player.rect.y <= 100:
			hm = player.speed*2
			self.rect.y += hm
			player.down(hm)
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
		self.image.fill(WHITE)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, player):
		if player.speed > 0:
			if player.rect.y > 400:
				hm = player.speed/3
				self.rect.y += hm
			elif player.rect.y < 300 and player.rect.y > 200:
				hm = player.speed/2.5
				self.rect.y += hm
			elif player.rect.y < 200 and player.rect.y > 100:
				hm = player.speed
				self.rect.y += hm
			elif player.rect.y <= 100:
				hm = player.speed*2
				self.rect.y += hm
			if self.rect.y >= 800:
				self.kill()

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
			platforms.add(Platform(x, max_h-110, platform_number, kind))
			platform_enemy = random.choice(['platform', 'platform', 'platform', 'platfrom', 'platform', 'platform', 'platform', 'enemy', 'platform', 'platform'])
			enemy = random.choice(['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'])
			if kind == 'ot':
				if x < 250:
					if platform_enemy == 'platform':
						platforms.add(Platform(x+200, max_h-110, platform_number, 'regular'))
					elif len(enemies) == 0:
						enemies.add(Enemy(x+250, max_h-125))
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
	screen.fill(BLACK)

	platforms.draw(screen)
	group.draw(screen)
	enemies.draw(screen)
	player.update(change, platforms)
	if up:
		platforms.update(player)
		enemies.update(player)
	for x in platforms:
		if x.kind == 'movable':
			x.move()
		if player.speed < 0 and pygame.sprite.collide_rect(player, x):
			if prev != None:
				if highest-x.time < 0:
					up = True
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
	
