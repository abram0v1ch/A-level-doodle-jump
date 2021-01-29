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

#-- Initialise pygame and clock
pygame.init()

#variables needed for classes
prev = None
highest = 0
up = False

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([40, 40])
		self.image.fill(YELLOW)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = 260
		self.rect.y = 720
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


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface([60, 10])
		self.image.fill(BLUE)
		self.time = time.time()
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, player):
		if player.rect.y > 400:
			self.rect.y += player.speed/3
		elif player.rect.y < 300 and player.rect.y > 200:
			self.rect.y += player.speed/2.5
		elif player.rect.y < 200 and player.rect.y > 100:
			self.rect.y += player.speed
		elif player.rect.y <= 100:
			self.rect.y += player.speed*2
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
	while len(platforms) < 7:
		if len(platforms) > 0:
			for x in platforms:
				if x.rect.y < max_h:
					max_h = x.rect.y
			platforms.add(Platform(random.randint(0, 490), max_h-110))
			time.sleep(0.000001)
		else:
			platforms.add(Platform(240, 760))
			time.sleep(0.000001)

	# Screen background is BLACK
	screen.fill(BLACK)

	platforms.draw(screen)
	group.draw(screen)
	player.update(change, platforms)
	if up:
		platforms.update(player)
	for x in platforms:
		if player.speed < 0 and pygame.sprite.collide_rect(player, x):
			if prev != None:
				if highest-x.time < 0:
					up = True
			prev = x.time
			if prev > highest:
				highest = prev
			player.up()

	#--flip display to reveal new position of objects
	pygame.display.flip()
	clock.tick(60)

###--End of game loop
pygame.quit()
	
