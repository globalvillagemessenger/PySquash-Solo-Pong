import pygame
import sys
import random
import math

#Initialize pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

#create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#title and icon
pygame.display.set_caption("PySquash: Solo Pong")
icon = pygame.image.load("racket.png")
pygame.display.set_icon(icon)


#sound effect
beep = pygame.mixer.Sound('beep.wav')


# colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#draw text function
font_name = pygame.font.match_font('courier')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#sprite classes
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 70))
        self.image.fill((WHITE))
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = HEIGHT/2
        self.speedx = 0
        self.speedy = 0
        
    def update(self):
        keystate = pygame.key.get_pressed()
        self.speedy = 0
        if keystate[pygame.K_w]:
            self.speedy = -4
        if keystate[pygame.K_s]:
            self.speedy = 4

        #player speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #player y-axis boundary
        if self.rect.top > HEIGHT - 70:
            self.rect.top = HEIGHT - 70
        if self.rect.bottom < 0 + 70:
            self.rect.bottom = 0 + 70
    


# lists of ball speed modifiers
ballspeedmodifier1 = [-1, 1]
ballspeedmodifier2 = [-1, 1]

            
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((WHITE))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = 0
        self.speedx = 1
        self.speedy = 1
        
    def update(self):
        #ball speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #ball movement
        if self.rect.y <= 0:
            self.speedy = abs(self.speedy)
            self.speedx = self.speedx * (random.choice(ballspeedmodifier2))
        elif self.rect.y >= HEIGHT - 20:
            self.speedy = self.speedy * -1
            self.speedx = self.speedx * (random.choice(ballspeedmodifier2))
        
        #penalty
        if self.rect.x <= 20:
            self.rect.x = WIDTH/2
            self.rect.y = 0
            global player1_score
            player1_score += -1
            self.speedx = 1
            self.speedy = 1
            print("Ball speed x: ", self.speedx)
            print ("Ball speed y: ", self.speedy)
            
        if self.rect.x >= WIDTH - 20:
            b.speedx = b.speedx * -1
            b.speedy = b.speedy * (random.choice(ballspeedmodifier1))
            

# create variable for player score, set initial score to zero
player1_score = 0
player2_score = 0     


# create sprites
all_sprites = pygame.sprite.Group()

player1 = Player1()
all_sprites.add(player1)

ball = pygame.sprite.Group()
for i in range(1):
    b = Ball()
    all_sprites.add(b)
    ball.add(b)



# game loop
game_over = False
running = True
while running:
    
    # update screen
    all_sprites.update()
    
    
    
    # checks to see if ball hits player1
    hits1 = pygame.sprite.spritecollide(player1, ball, False)
    if hits1:
        b.speedx = abs(b.speedx) + ((math.pow(b.speedx, 0))/10) + (random.uniform(0, 1))
        b.speedy = (random.choice(ballspeedmodifier2)) * (abs(b.speedy) + ((math.pow(b.speedy, 0))/10) + (random.uniform(0, 1)))
        beep.play()
        player1_score += 1
        print("Ball speed x: ", b.speedx)
        print("Ball speed y: ", b.speedy)
        
    # double points for higher ball speed
    if hits1 and b.speedx <= -3:
        player1_score += 1
    if hits1 and b.speedy <= -3:
        player1_score += 1
    if hits1 and b.speedy >= 3:
        player1_score += 1
        
    
    # draw screen, sprites, and player scores
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, "Score: " + str(player1_score), 18, WIDTH / 4, 10)

    
    pygame.display.flip()

    # quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
 