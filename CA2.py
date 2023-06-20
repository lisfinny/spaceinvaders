import random
import sys

import pygame

pygame.init() # initialize pygame
score = 0
countdown = 4 # countdown before starting the game
clock = pygame.time.Clock() # clock will help track time which will be useful for cooldowns 

game_over = 0 # variable to keep track of if game has ended if it is 1, win if it is -1 lose
alien_missile_speed = 4 # how fast aliens missiles will travel
player_missile_speed = 13 #how fast players missiles will travel
fps = 60 # sets the number of frames per second
x_distance_alien = 60  #alien will move 60 pixels then change directions and drop 
life = 5 # sets players life a missile will remove one life

alien_objects = [] #creates a list of aliens this will allow us to access their coordinates 

alien_cooldown = 800 # cooldown on how fast the aliens can shoot

last_alien_shot = pygame.time.get_ticks()  # tells us how long ago the last alien shot was

size = width, height = 900, 900 
screen = pygame.display.set_mode(size)# sets size of window

pygame.display.set_caption('space invaders') # sets name of window to space invaders




            


class Aliens(pygame.sprite.Sprite):
    ''' a class to create the aliens that will appear at top of screen
    and move left to right and down
    '''
    def __init__(self, x, y,index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("aliens.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
        self.move_direction = 1 # sets direction aliens will move in
        self.move_counter = 0 # counts how many moves
        self.increase = 80 # number of pixels to go vertically down
        
        self.index = index # index that will be useful to store aliens

    def returnYPos(self):
        return self.rect.y # gives the y postion of the alien
    
    def returnIndex(self):
        return self.index # gives the index of the alien(inalien_objects list)

    def update(self):
        '''updates the postion of the alien'''
        
        move = False 
        self.rect.x += self.move_direction # moves alien in direction set above
        self.move_counter += 1 # increases counter by 1
        
    
       

        if (self.move_counter) > x_distance_alien :  #  if the counter goes above set number of pixels
            move = True
                 
            self.move_direction *= -1 # change direction
        
            self.move_counter = -x_distance_alien #
        if move == True : # if move is set to true
            self.rect.y += 80    # move down by 80 pixels
        if len(alien_group) < 20:
            create_aliens(1,random.randint(1,8)) # if there are less than 20 aliens create new ones
                  
        if pygame.sprite.spritecollide(self, missile_group, True):
            alien_objects.remove(alien_objects[self.index]) # if a player missile hits an alien remove that aliend from alien_objects     
             


class alien_missile(pygame.sprite.Sprite):
    '''a class to keep track of alien missiles'''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]  # creates image and rectangele for alien missiles

    def update(self):
        self.rect.y += alien_missile_speed
        if self.rect.top > height:
            self.kill() # if missile goes out of screen kill it
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            ship.life_remaining -= 1
            self.kill() # if a missile hits the player take one from player life and kill missile



class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, life):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ship.png") # loads the image of the ship
        self.rect = self.image.get_rect() # gets rectangle around ship
        self.rect.center = [x, y] # coordinates to know where to put centre of rectangle
        self.life_start = life
        self.life_remaining = life  # this will keep track of players life and sets remaining life to staring life
        self.mostrecent_shot = pygame.time.get_ticks() # gets the time from last shot of the ship

    def move(self):
        '''updates ships position'''
        
        speed = 8
        # set a cooldown
        cooldown = 400  # miliseconds
        # key will keep track of which keys are being pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed  # if the left key is pressed and the ship is not at the border move the ship left be value of speed
        if key[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += speed # this moves ship right

        time_now = pygame.time.get_ticks() # gets the current time
        
        if key[pygame.K_SPACE] and time_now - self.mostrecent_shot > cooldown:  # if space is pressed and the current time minus the time of the last shot is great
            #than the cooldown then a missile is created and shot upwards
            missiles = player_missile(self.rect.centerx, self.rect.top)
            missile_group.add(missiles)
            self.mostrecent_shot = time_now

        
    def life(self):
        '''creates a life bar under the ship '''
        pygame.draw.rect(screen, 'black', (self.rect.x,
                (self.rect.bottom + 7), self.rect.width, 20)) # creates a lifebar under the ship so players can see how many shots they can survive bar is 7 by 20 in area
        if self.life_remaining > 0: 
            pygame.draw.rect(screen, 'green', (self.rect.x, (self.rect.bottom + 7),
                int(self.rect.width * (self.life_remaining / self.life_start)), 20)) # creates a green bar over the black 
                # divide life remaing by lifestart to get ratio for size of the bar

    def die(self):
        ''' a function to kill the player'''
        self.life_remaining = 0


class player_missile(pygame.sprite.Sprite):
    ''' a class to create and track the players missiles'''
     
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png") # loads in png
        self.rect = self.image.get_rect() # creates a rectangle around bullet
        self.rect.center = [x, y] # coords of centre of bullet

    def update(self):
        global score
        self.rect.y -= player_missile_speed # send the bullet upwards by missle speed
        if self.rect.bottom < 0:
            self.kill() # if it goes off the screen kill/ remove the missile
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill() # if it collides with an aliend kill/remove the missile
            score += 100



def create_aliens(rows,cols):
    ''' a function that will itterate through a double for loop to create aliens in rows'''
    index = 0
     
    for row in range(rows):
        for item in range(cols):
            aliens = Aliens(100 + item * 100, 100+row * 100,index) # sets postion of aliens and give them an index
            alien_objects.append(aliens) #  create a list with aliens
            alien_group.add(aliens) # create a group with aliens
            index +=1
            

            

background = pygame.image.load("background.png")  # loads background


def create_background():
    screen.blit(background, (0, 0)) # creates background


ship = Ship(int(width/2), height-100, life) # creates the ship


last_count = pygame.time.get_ticks() # gets current time

font = pygame.font.SysFont('arial', 40) # creates font 

white = (255, 255, 255) # makes white
blue = (0,0,255)


def write_text(text, font, text_col, x, y):
    '''function used to draw text'''
    words = font.render(text, True, text_col)
    screen.blit(words, (x, y))


# all the groups of sprites
spaceship_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
aliens_missile_group = pygame.sprite.Group()

spaceship_group.add(ship) # add ship to the spaceship group

create_aliens(3,8) # creates 3 rows of 8 aliens

while True:
    clock.tick(fps) # used to limit frames per second
    

    
    

    create_background() #creates the background
    write_text(str(score), font, blue, int(width/22), int(height/22)) # displays score as blue in bottom right corner
    for i in range(len(alien_objects)):
        if (alien_objects[i].returnYPos()) >= 740:
            ship.die() # for every alien if any of them get below 740 ie ships position lose the game

    if countdown == 0: # when countdown ends
        time_now = pygame.time.get_ticks() # get current time
        
        

        if time_now - last_alien_shot > alien_cooldown and len(aliens_missile_group) < 10 and len(alien_group) > 0: 
            #if the time between last shot is greater than cooldown and there are less than 10 alien missiles and there are aliens on the board shoot a missile
            attacker = random.choice(alien_group.sprites())
            attack = alien_missile(attacker.rect.centerx, attacker.rect.bottom)
            aliens_missile_group.add(attack) # a random alien shoots a missile and it is added to the missilegroup
            last_alien_shot = time_now

        if len(alien_group) == 0:

            game_over = 1 # if all aliens are dead win the game
        else: 
            if ship.life_remaining < 1: #if the ship has no health lose the game
                game_over = -1

        
        if game_over == 0: #if game is still going

            ship.move()
            ship.life()
            missile_group.update()
            
            alien_group.update()
            aliens_missile_group.update() # update needed groups
        # draw sprite group

        elif game_over == -1:
            write_text('You Lose', font, white, int(width / 2 - 100), int(height / 2 + -100))
        elif game_over == 1:
            write_text('You Win!', font, white, int(width / 2 - 100), int(height / 2 + -100)) # draw texts for winning and losing

    if countdown > 0:

        write_text('begin in', font, white, int( width / 2 -100), int(height / 2 - 100))
        write_text(str(countdown), font, white, int( height / 2 - 50), int(height / 2 - 50))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer #if a second has passed decrease the time

    spaceship_group.draw(screen)
    missile_group.draw(screen)
    alien_group.draw(screen)
    aliens_missile_group.draw(screen) # create groups

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() # if the game closes quit the game
