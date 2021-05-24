from datetime import datetime
import time
import pygame
import random
import math
import os
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
prev2 = None
highest = 0
highest2 = 0
up = False
player2 = None
up2 = False
pmh = 575
hd = None
hd2 = None
kinds = ('regular', 'movable', 'ot')
mods = ('none', 'spring', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'helihat', 'none', 'none', 'spring', 'none', 'none', 'none', 'none', 'spring', 'none', 'none', 'none', 'none', 'none', 'none', 'rocket', 'none')

platform_number = 0

BASE_PATH = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_PATH, 'fonts')
font = pygame.font.Font(os.path.join(FONT_PATH, 'space_invaders.ttf'), 26)

class Player(pygame.sprite.Sprite):
	def __init__(self, second=None):
		super().__init__()
		self.image = pygame.Surface([40, 40])
		self.image.fill(BLACK)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		if second != True:
			self.rect.x = 260
			self.second = False
		else:
			self.rect.x = 260+650
			self.second = True
		self.rect.y = 720
		self.score = 0
		self.speed = 40
		self.mod = None
		self.time = None

	def update(self, change, platforms):
		global up
		global hd

		global up2
		global hd2

		if self.rect.y < 450:
			self.speed = 0
			self.rect.y = 450
		if self.mod == 'spring':
			if time.time() - self.time <= 0.75:
				self.rect.y -= 20
				self.score += 8
			else:
				self.time = 0
				self.mod = None
		elif self.mod == 'helihat':
			if time.time() - self.time <= 2:
				self.rect.y -= 20
				self.score += 9
			else:
				self.time = 0
				self.mod = None
		elif self.mod == 'rocket':
			if time.time() - self.time <= 4:
				self.rect.y -= 20
				self.score += 11
			else:
				self.time = 0
				self.mod = None
		else:
			self.rect.y -= self.speed/3
			if self.speed > 0:
				self.speed -= 2
			if self.speed == 0:
				if self.second == False:
					up = False
					hd = self.rect.y - pmh
				else:
					up2 = False
					hd2 = self.rect.y - pmh
				self.speed = -40
			if self.speed < 0:
				self.speed += 3
		if not self.second:
			self.rect.x += change
			if self.rect.x == -40:
				self.rect.x = 540
			if self.rect.x == 550:
				self.rect.x = -30
		else:
			self.rect.x += change_second
			if self.rect.x == 610:
				self.rect.x = 1190
			if self.rect.x == 1200:
				self.rect.x = -620

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
	def __init__(self, x, y, number, kind, mod, second=None):
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
		self.second = second

	def update(self, player):
		global hd
		global hd2

		pl = player
		if self.rect.x > 550:
			hed = hd2
		else:
			hed = hd
		if pl.mod == 'spring':
			hm = (545-450)/(10-2)
		elif pl.mod == 'helihat':
			hm = (545-450)/(10-4)
		elif pl.mod == 'rocket':
			hm = (545-450)/(10-6)
		else:
			hm = abs(hed)/(10)
		if self.mod != 'none':
			self.powerup.update(hm)

		self.rect.y += hm
		if self.rect.y >= 800:
			if self.mod != 'none':
				self.powerup.kill()
			self.kill()

	def move(self):
		if self.second == None:
			if self.rect.x >= 490:
				self.speed = -3
			elif self.rect.x <= 0:
				self.speed = 3
		else:
			if self.rect.x >= 1140:
				self.speed = -3
			elif self.rect.x <= 650:
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

		if pl.mod == 'spring':
			hm = (545-450)/(10-2)
		elif pl.mod == 'helihat':
			hm = (545-450)/(10-4)
		elif pl.mod == 'rocket':
			hm = (545-450)/(10-6)
		else:
			hm = abs(hed)/(10)
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
change_second = 0

#-- Manages how fast clock refreshes
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
		text = font.render('Jumpy\nPress [S] to start single player game', False, PURPLE)
		screen.blit(text,(50,1))
		pygame.display.flip()
		clock.tick(60)

def end():
	global player
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					game()
				if event.key == pygame.K_m:
					local_multi()
				if event.key == pygame.K_q:
					exit()
		screen.fill(WHITE)
		text = font.render('Game over\nScore:' + str(player.score) + '\nPress [S] to play again \n or [Q] to exit', False, PURPLE)
		screen.blit(text,(50,1))
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
		text = font.render('Pause menu\n [S] to continue [q] to exit', False, PURPLE)
		screen.blit(text,(50,1))
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
				if event.key == pygame.K_ESCAPE:
					pause()
				if event.key == pygame.K_SPACE and player.mod != 'rocket' and player.mod != 'helihat':
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
				if player.score < 15000:
					if x < 250:
						platforms.add(Platform(x+200, max_h+175, platform_number, kd, md))
					elif x >= 250:
						platforms.add(Platform(x-200, max_h+175, platform_number, kd, md))
				elif player.score > 25000 and player.score < 40000:
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
			if x == 3:
				pygame.draw.line(screen, RED, (x * 20, 0), (x * 20, 800))
			elif x >= 0 and x <= 27:
				pygame.draw.line(screen, (222,222,222), (x * 20, 0), (x * 20, 800))
			pygame.draw.line(screen, (222,222,222), (0, x * 20), (550, x * 20))

		for x in enemies:
			x.move()
			if pygame.sprite.collide_rect(player, x):
				if player.mod != None and player.mod != 'spring':
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
		screen.blit(score_text,(460,1))
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
				if player.mod == None and x.mod != 'none' and pygame.sprite.collide_rect(player, x.powerup):
					player.powerup(x.mod)
					x.powerup.kill()
				else:
					player.up()

		if player.rect.y >= 760:
			done = True
			break

		#--flip display to reveal new position of objects
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

	size = (1200,800)
	screen = pygame.display.set_mode(size)

	player2 = Player(second=True)
	group.add(player2)
	platforms2 = pygame.sprite.Group()
	enemies2 = pygame.sprite.Group()
	shots2 = pygame.sprite.Group()
	powerups2 = pygame.sprite.Group()

	while not done:
		#-- User inputs here
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					change_second = -10
				elif event.key == pygame.K_RIGHT:
					change_second = 10
				if event.key == pygame.K_ESCAPE:
					pause()
				if event.key == pygame.K_RCTRL and player2.mod != 'rocket' and player2.mod != 'helihat':
					shots.add(Shot(player2, enemies2))
				if event.key == pygame.K_a:
					change = -10
				elif event.key == pygame.K_d:
					change = 10
				if event.key == pygame.K_LSHIFT and player.mod != 'rocket' and player.mod != 'helihat':
					shots.add(Shot(player, enemies))
				 #endif
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					change_second = 0
				if event.key == pygame.K_a or event.key == pygame.K_d:
					change = 0
				#endif
			#endif
		# Game logic goes after this comment
		max_h = 800
		max_h2 = 800
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
				if player.score < 15000:
					if x < 250:
						platforms.add(Platform(x+200, max_h+175, platform_number, kd, md))
					elif x >= 250:
						platforms.add(Platform(x-200, max_h+175, platform_number, kd, md))
				elif player.score > 25000 and player.score < 40000:
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

		while len(platforms2) < 24:
			if len(platforms2) > 0:
				for x in platforms2:
					if x.rect.y < max_h2:
						max_h2 = x.rect.y
				kind = random.choice(kinds)
				x = random.randint(0, 490)
				if kind == 'ot':
					mod = 'none'
				else:
					mod = random.choice(mods)
				platforms2.add(Platform(x+650, max_h2-115, platform_number2, kind, mod, second=True))
				kd = random.choice(['regular', 'ot'])
				if kd == 'ot':
					md = 'none'
				else:
					md = random.choice(mods)
				if player2.score < 15000:
					if x < 250:
						platforms2.add(Platform(x+200+650, max_h2+175, platform_number2, kd, md, second=True))
					elif x >= 250:
						platforms2.add(Platform(x-200+650, max_h2+175, platform_number2, kd, md, second=True))
				elif player2.score > 25000 and player2.score < 40000:
					if x < 250:
						platforms2.add(Platform(x+200+650, max_h2-175, platform_number2, kd, md, second=True))
					elif x >= 250:
						platforms2.add(Platform(x-200+650, max_h2-175, platform_number2, kd, md, second=True))
				else:
					pass
				platform_enemy = random.choice(['platform', 'platform', 'platform', 'platfrom', 'platform', 'platform', 'platform', 'enemy', 'platform', 'platform'])
				enemy = random.choice(['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no'])
				if kind == 'ot':
					if x < 250:
						if platform_enemy == 'platform':
							platforms2.add(Platform(x+200+650, max_h2-115, platform_number2, 'regular', random.choice(mods), second=True))
						elif len(enemies2) == 0:
							enemies2.add(Enemy(x+250+650, max_h2-110))
					if x >= 250:
						if platform_enemy == 'platform':
							platforms2.add(Platform(x-200+650, max_h2-110, platform_number2, 'regular', random.choice(mods), second=True))
						else:
							enemies2.add(Enemy(x-250+650, max_h2-125))
				if kind == 'regular':
					if x < 250:
						if enemy == 'yes' and len(enemies2) == 0:
							enemies2.add(Enemy(x+250+650, max_h2-125))
					if x >= 250:
						if enemy == 'yes' and len(enemies2) == 0:
							enemies.add(Enemy(x-250+650, max_h2-125))
				platform_number2 += 1
				time.sleep(0.000001)
			else:
				platforms2.add(Platform(240+650, 760, platform_number2, 'regular', 'none', second=True))
				platform_number2 += 1
				time.sleep(0.000001)

		# Screen background is BLACK
		screen.fill(WHITE)

		for x in range(40):
			if x == 3:
				pygame.draw.line(screen, RED, (x * 20, 0), (x * 20, 800))
			elif x >= 0 and x <= 27:
				pygame.draw.line(screen, (222,222,222), (x * 20, 0), (x * 20, 800))
			pygame.draw.line(screen, (222,222,222), (0, x * 20), (550, x * 20))

		for x in enemies:
			x.move()
			if pygame.sprite.collide_rect(player, x):
				if player.mod != None and player.mod != 'spring':
					x.kill()
				elif player.speed < 0 and player.rect.y < x.rect.y:
					x.kill()
					player.up()
				else:
					done = True

		for x in enemies2:
			x.move()
			if pygame.sprite.collide_rect(player2, x):
				if player2.mod != None and player2.mod != 'spring':
					x.kill()
				elif player2.speed < 0 and player2.rect.y < x.rect.y:
					x.kill()
					player2.up()
				else:
					done = True

		platforms.draw(screen)
		powerups.draw(screen)
		group.draw(screen)
		shots.draw(screen)
		enemies.draw(screen)
		player.update(change, platforms)
		shots.update()

		platforms2.draw(screen)
		powerups2.draw(screen)
		shots2.draw(screen)
		enemies2.draw(screen)
		player2.update(change, platforms2)
		shots2.update()

		score_text = font.render(str(player.score), False, PURPLE)
		screen.blit(score_text,(460,1))

		score_text2 = font.render(str(player2.score), False, PURPLE)
		screen.blit(score_text2,(460+650,1))

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
				if player.mod == None and x.mod != 'none' and pygame.sprite.collide_rect(player, x.powerup):
					player.powerup(x.mod)
					x.powerup.kill()
				else:
					player.up()

		if player2.rect.y < 500:
			up2 = True
		if up2:
			platforms2.update(player2)
			enemies2.update(player2)
		for x in platforms2:
			if x.kind == 'movable':
				x.move()
			if player2.speed < 0 and pygame.sprite.collide_rect(player2, x):
				if prev2 != None:
					if highest2-x.time < 0:
						#up = True
						pass
				prev2 = x.time
				if prev2 > highest2:
					highest2 = prev2
					player2.scoreup(x.number)
				if x.kind == 'ot':
					x.kill()
				if player2.mod == None and x.mod != 'none' and pygame.sprite.collide_rect(player2, x.powerup):
					player2.powerup(x.mod)
					x.powerup.kill()
				else:
					player2.up()

		if player.rect.y >= 760:
			done = True
			break

		#--flip display to reveal new position of objects
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
	
#150-2600 - travelled by rocket
#400-650 - travelled by spring
#2350-3250 - travelled by helihat