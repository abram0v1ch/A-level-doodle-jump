import pygame
#-- Global constants

#-- Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

#-- Initialise pygame and clock
pygame.init()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([40, 40])
		self.image.fill(YELLOW)
		#set the position of the sprite
		self.rect = self.image.get_rect()
		self.rect.x = 260
		self.rect.y = 760
		self.speed = 66

	def update(self, change):
		self.rect.y -= self.speed/3
		if self.speed > 0:
			self.speed -= 3
		if self.speed == 0:
			self.speed = -33
		if self.speed < 0:
			self.speed += 3
		if self.rect.y >= 760:
			self.speed = 66
		self.rect.x += change
		if self.rect.x == -40:
			self.rect.x = 540
		if self.rect.x == 550:
			self.rect.x = -30

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
group.add(player)

###-- Game Loop
while not done:
    #-- User inputs here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -5
            elif event.key == pygame.K_RIGHT:
                change = 5
             #endif
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                change = 0
            #endif
        #endif
    # Game logic goes after this comment

    # Screen background is BLACK
    screen.fill(BLACK)

    group.draw(screen)
    player.update(change)

    #--flip display to reveal new position of objects
    pygame.display.flip()
    clock.tick(60)

###--End of game loop
pygame.quit()
    
