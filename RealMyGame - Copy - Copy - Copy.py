import pygame
import random
pygame.init()


#To restart game click mouse button
W, H = 684, 480
win = pygame.display.set_mode((W, H)) #Size of window
pygame.display.set_caption("Its My Game!") #Name for game window

walkRight = [pygame.image.load("MarioRight.png"), pygame.image.load("MarioRight2.png"), pygame.image.load("MarioRight3.png"), pygame.image.load("MarioRight4.png")] #Sprites for right walk animation
walkLeft = [pygame.image.load("MarioLeft.png"), pygame.image.load("MarioLeft2.png"), pygame.image.load("MarioLeft3.png"), pygame.image.load("MarioLeft4.png"), pygame.image.load("MarioLeft5.png")] #Sprites for left walk animation

bg = pygame.image.load("mpbg.png") #Background for game
bg1 = 0
bg2 = bg.get_width()
char = pygame.image.load("BigMario.png") #Image for character
clock = pygame.time.Clock()

music = pygame.mixer.music.load("MaplestoryBGM.mp3")
deathsound = pygame.mixer.Sound("Deathsound.wav")
pygame.mixer.music.play(-1)

green = (0,200,0)
red = (200,0,0)
lightred = (255,0,0)
lightgreen =(0,255,0)


class player(object):  #Class is blueprint for code
    def __init__(self, x, y, width, height): #Init is what initializes the plan 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5 #Speed at which character travels
        self.isJump = False #Boolean value for jump
        self.left = False #Boolean value for walking left
        self.right = False #Boolean value for walking right
        self.jumpcount = 10
        self.walkcount = 0
        self.standing = True #Character starts off standing
        
    def draw(self,win): #Draws onto the output
        if self.walkcount + 1 >=20:
            
            self.walkcount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkcount//4], (self.x,self.y))
                self.walkcount += 1
            elif self.right:
                win.blit(walkRight[self.walkcount//5], (self.x,self.y))
                self.walkcount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x - 5,self.y,self.width-40,self.height-30)
##        pygame.draw.rect(win, (255,0,0), self.hitbox, 1)  - To see hitbox of player

        
class obstacle(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)

    def draw (self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x + 1, self.y, self.width -1, self.height)
##        pygame.draw.rect(win, (255,0,0), self.hitbox, 2) - To see hitbox of obstacles
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
        

def redrawGameWindow():
    win.blit(bg, (bg1,0)) #Draws the first background
    win.blit(bg, (bg2,0)) #Draws the second background
    person.draw(win)
    for objectss in objects:
        objectss.draw(win)
    font = pygame.font.SysFont("comicsans", 30)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (700, 10))
    pygame.display.update() #Refreshes the display


def endscreen():
    global person, pause, objects, speed, score
    person = player(20, 400, 64, 64)
    pause = 0
    objects = []
    speed = 30
    pygame.mixer.music.stop
    run = True
    
    while run:
        pygame.time.delay(100)#.1 sec delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse button
                run = False #Loop will end
                player.isJump= False
                player.left= False
                player.right= False
                pygame.mixer.music.stop
                player(20, 400, 64, 64)
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont("comicsans", 80)
        dead = largeFont.render("GAME OVER", 1, (255,255,255))
        win.blit(dead, (2,50))
        newScore = largeFont.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(newScore, (2, 200))
        restart = largeFont.render("Restart = Mouse Button ", 1, (255, 255, 255))
        win.blit(restart, (2, 350))
        pygame.display.update()
        
    score = 0
    
    
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    run = True
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ic,(x, y, w, h))
        if click[0] == 1 and action !=None:
            if action == "play":
                run = True
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(win, ac,(x, y, w, h))
        
    smallFont = pygame.font.SysFont("comicsans", 30)
    greentext = smallFont.render(msg, 1, (0,0,0))
    win.blit(greentext, ((x-25+(w/2)), (y-10+(h/2))))
    
    
def intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.fill((255, 255, 255))
        largeFont = pygame.font.SysFont("comicsans", 80)
        smallFont = pygame.font.SysFont("comicsans", 30)
        start = largeFont.render("Welcome To My Game", 1, (0,0,0))
        controls = smallFont.render("Arrow Keys = Move, Space = Jump", 1, (0,0,0))
        win.blit(start, (45, 50))
        win.blit(controls, (175, 150))
        button("Start", 450, 300, 100, 50, green, lightgreen, "play")
        button("Quit", 150, 300, 100, 50, red, lightred, "quit")
        
        pygame.display.update()
        clock.tick(15)
        
    
    
person = player(20, 400, 64, 64) #Coordinates for character position
speed = 35 #Speed variable for background
pygame.time.set_timer(pygame.USEREVENT+1, 500) # Sets a timer for 500 milliseconds
pygame.time.set_timer(pygame.USEREVENT+2, random.randrange(3000,6000))


run = True
pause = 0
objects = []

while run:
    score = speed//5 - 7
    if pause > 0:
        deathsound.play()
        pygame.time.delay(2500)
        endscreen()

    for objectss in objects: #For each item in object list
        if objectss.collide(person.hitbox): 

            if pause == 0:
                pause = 1
        objectss.x -= 1.7 #speed of obstacle spawn
        if objectss.x < -objectss.width * -1:
            objects.pop(objects.index(objectss))
    bg1 -= 1.7 #speed of background
    bg2 -= 1.7
    if bg1 < bg.get_width() * -1:
        bg1 = bg.get_width()
        
    if bg2 < bg.get_width() * -1:
        bg2 = bg.get_width()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #Program will end
         
        if event.type == pygame.USEREVENT+1: # Checks to see if the timer goes off
            speed += 1 # Increases speed by 1
        if event.type == pygame.USEREVENT+2: # Checks to see if the timer goes off
            objects.append(obstacle(810, 400, 64, 64))           
        
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and person.x > person.vel:
        person.x -= person.vel
        person.left = True  #Person will move left when user presses left key
        person.right = False
        person.standing = False
    elif keys[pygame.K_RIGHT] and person.x < 730 - person.width - person.vel:
        person.x += person.vel
        person.right = True
        person.left = False
        person.standing = False
    else:
        person.standing = True
        person.walkcount = 0
        
    if not(person.isJump):
        if keys[pygame.K_SPACE]: 
            person.isJump = True #Jump is true when space bar is pressed 
            person.right = False #Person will not walk right
            person.left = False#Character will not walk left
            person.walkcount = 0
    else:
        if person.jumpcount >= -10:
            person.y -= (person.jumpcount * abs(person.jumpcount)) * .25 #Formula for jump
            person.jumpcount -= 1
        else:
            person.isJump = False
            person.jumpcount = 10
    
    intro()        
    clock.tick(speed)
    redrawGameWindow() #calls function   
    clock.tick(60)#fps of game
    

pygame.quit() #Quits program
