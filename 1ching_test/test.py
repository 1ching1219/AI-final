import pygame, sys, math, random
import numpy as np
import threading

pygame.init()

class Sheep(pygame.sprite.Sprite):
    def __init__(self, filename, initial_position):
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
        self.speed = [0, 0]
        self.live = 50

    def move(self):
        self.rect = self.rect.move(self.speed)
        self.live -= 0.1
        if self.rect.top > 480:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = 480
        if self.rect.left > 640:
            self.rect.right = 0  
        if self.rect.right < 0:
            self.rect.left = 0  
    
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
sheep_initial_num = 5
grass_initial_num = 15
locationGroup = []
grasslocation = []

for i in range(sheep_initial_num):
    locationGroup.append([random.randint(10, 630), random.randint(10, 470)])

for i in range(grass_initial_num):
    grasslocation.append([random.randint(10, 630), random.randint(10, 470)])

SheepGroup = pygame.sprite.Group()
GrassGroup = pygame.sprite.Group()

# walk direction
for l in locationGroup:
    SheepGroup.add(Sheep(sheep_img, l))

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

    # initial map
    sheep_map = []
    grass_map = []
    count_SheepGrass_distance = []
    

    # draw grass
    for grass in GrassGroup.sprites():
        window.blit(grass.image, grass.rect)
        grass_map.append([grass.rect.centerx, grass.rect.centery])
        
        for sheep in SheepGroup.sprites():
            if([grass.rect.centerx, grass.rect.centery] in grass_map and [grass.rect[0], grass.rect[1]] in grasslocation):
                if [sheep.rect.centerx, sheep.rect.centery] == [grass.rect.centerx, grass.rect.centery]:
                        grass.die()
                        sheep.live += 12
                        grass_map.remove([grass.rect.centerx, grass.rect.centery])
                        grasslocation.remove([grass.rect[0], grass.rect[1]])
                        if(random.randint(1, 3)==3):
                            grasslocation.append([random.randint(10, 630), random.randint(10, 470)])
                

  
    # draw and move sheep
    time = 0
    for sheep in SheepGroup.sprites():
        sheep.move()
        print(sheep.live)
        window.blit(sheep.imagelist[sheep_indx], sheep.rect)
        sheep_map.append([sheep.rect.centerx, sheep.rect.centery])
        for i, position in enumerate(grass_map):
            x, y = position
            distance = (sheep.rect.centerx - x)**2 + (sheep.rect.centery - y)**2
            count_SheepGrass_distance.append(distance)

        min_value = min(count_SheepGrass_distance)
        min_index = count_SheepGrass_distance.index(min_value)
        x, y = grass_map[min_index]
        nextstep = [(x - sheep.rect.centerx), (y - sheep.rect.centery)]

        if nextstep[0] > 0: dx = 1
        elif nextstep[0] < 0: dx = -1
        else: dx = 0
        if nextstep[1] > 0:dy = 1
        elif nextstep[1] < 0: dy = -1
        else: dy = 0

        if((dx + dy) == 1 or (dx + dy) == -1):
            dx *= 1.4142
            dy *= 1.4142

        sheep.speed = [dx, dy]

        if(sheep.live <= 0):
            sheep.die()

        if(sheep.live >= 60):
            sheep.live -= 15
            l = [random.randint(10, 630), random.randint(10, 470)]
            locationGroup.append(l)
            SheepGroup.add(Sheep(sheep_img, l))

        count_SheepGrass_distance = []
        
  
    GrassGroup = pygame.sprite.Group()
    for l in grasslocation:
        GrassGroup.add(Grass(grassimg, l))


    
    
        
    sheep_indx += 1
    if sheep_indx >= 6:
        sheep_indx = 0


    pygame.time.delay(100)
    pygame.display.update()