import pygame
#from cyb_ques import quiz
from sys import exit
from random import randint, choice



class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics\Player\pwalk1-removebg-preview.png').convert_alpha()
		player_walk_1 = pygame.transform.scale(player_walk_1, (68,72))
		player_walk_2 = pygame.image.load('graphics\Player\pwalk2-removebg-preview.png').convert_alpha()
		player_walk_2 = pygame.transform.scale(player_walk_2, (68,72))
		
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics\Player\pjump-removebg-preview.png').convert_alpha()
		self.player_jump= pygame.transform.scale(self.player_jump, (68,72))

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()


	def ans_input(self):
		keys = pygame.key.get_pressed()
		#if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
				

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/Fly/vup-removebg-preview.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/Fly/vdwn-removebg-preview.png').convert_alpha()
			fly_1 = pygame.transform.scale(fly_1, (50,50))
			fly_2 = pygame.transform.scale(fly_2, (50,50))
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics\snail\hdwn-removebg-preview.png').convert_alpha()
			snail_2 = pygame.image.load('graphics\snail\hup-removebg-preview.png').convert_alpha()
			snail_1 = pygame.transform.scale(snail_1, (80,80))
			snail_2 = pygame.transform.scale(snail_2, (80,80))
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()



def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(0,255,255))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def show_ques():
	count+=1
	



def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else:
		 return True











		 




pygame.init()

count=0
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption('cyberSpace')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics\starrybg.JPG').convert()
ground_surface = pygame.image.load('graphics\platfrm1.jpg').convert()
ground_surface = pygame.transform.scale(ground_surface, (600,100))

# Intro screen
intro_cs = pygame.image.load('graphics\intro_cybsp.JPG').convert_alpha()
intro_cs = pygame.transform.rotozoom(intro_cs,0,2)
intro_cs_rect = intro_cs.get_rect(center = (300,200))

game_name = test_font.render('cyberSPACE...will you survive?',False,(0,255,127))
game_name_rect = game_name.get_rect(center = (300,90))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (300,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		pygame.mixer.pause()
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		out_sound = pygame.mixer.Sound('audio/fai_cybsp.wav')
		out_sound.set_volume(0.5)
		pygame.mixer.unpause()
		screen.fill((94,129,162))
		screen.blit(intro_cs,intro_cs_rect)

		score_message = test_font.render(f'Your score: {score}',False,(0,255,255))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)