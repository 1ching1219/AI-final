import pygame, sys
from random import *

pygame.init()

class Sheep(pygame.sprite.Sprite):
    def __init__(self, filename, initial_position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.imagelist=[]
        sheeps_img = ['sheep/1.png', 'sheep/2.png', 'sheep/3.png', 'sheep/4.png', 'sheep/5.png', 'sheep/6.png']
        for sheep in sheeps_img:
            tmp = pygame.image.load(sheep)
            tmp = pygame.transform.scale(tmp, (70, 70))
            self.imagelist.append(tmp)

        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top > 480:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = 480
    
    def die(self):
        self.kill()
            

class Grass(pygame.sprite.Sprite):
    def __init__(self, filename, initial_position):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

    def die(self):
        self.kill()



window = pygame.display.set_mode([640, 480])
window.fill([147, 211, 52])

sheep_img = 'sheep/1.png'
grassimg = 'grass.png'
locationGroup = ([350, 300], [250, 300], [450, 260])
grasslocation = ([462, 272], [300, 400], [150, 220])
SheepGroup = pygame.sprite.Group()
GrassGroup = pygame.sprite.Group()

# walk direction
for l in locationGroup:
    x = 1   #左右
    y = 1  #上下
    speed = [1, choice([1, 2])]
    SheepGroup.add(Sheep(sheep_img, l, speed))

for l in grasslocation:
    GrassGroup.add(Grass(grassimg, l))

# load window
sheep_indx = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.time.delay(20)
    window.fill([147, 211, 52])

    # draw and move sheep
    for sheep in SheepGroup.sprites():
        sheep.move()
        window.blit(sheep.imagelist[sheep_indx], sheep.rect)
        

    # draw grass
    for grass in GrassGroup.sprites():
        window.blit(grass.image, grass.rect)
        
        for sheep in SheepGroup.sprites():
            if [sheep.rect[0], sheep.rect[1]] == [grass.rect[0], grass.rect[1]]:
                grass.die()
        
    sheep_indx += 1
    if sheep_indx >= 6:
        sheep_indx = 0
    


    pygame.time.delay(100)
    pygame.display.update()