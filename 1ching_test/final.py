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
            tmp = pygame.transform.scale(tmp, (40, 30))
            self.imagelist.append(tmp)

        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = [0, 0]
        self.live = 100

    def move(self):
        self.rect = self.rect.move(self.speed)
        self.live -= 0.1
        if self.rect.top > 750:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = 750
        if self.rect.left > 1020:
            self.rect.right = 0  
        if self.rect.right < 0:
            self.rect.left = 0  
    
    def die(self):
        self.kill()
            
class Wolf(pygame.sprite.Sprite):
    def __init__(self, filename, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.imagelist=[]
        wolfs_img = ['wolf/1.png', 'wolf/2.png', 'wolf/3.png', 'wolf/4.png', 'wolf/5.png', 'wolf/6.png']
        for wolf in wolfs_img:
            tmp = pygame.image.load(wolf)
            tmp = pygame.transform.scale(tmp, (70, 42))
            self.imagelist.append(tmp)

        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (70, 42))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = [0, 0]
        self.live = 100
        
    def move(self):
        self.rect = self.rect.move(self.speed)
        self.live -= 0.3
        if self.rect.top > 750:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = 750
        if self.rect.left > 1020:
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



window = pygame.display.set_mode([1020, 750])
window.fill([147, 211, 52])

sheep_img = 'sheep/1.png'
grassimg = 'grass.png'
wolf_img = 'wolf/1.png'
sheep_initial_num = 20
grass_initial_num = 150
wolf_initial_num = 1
locationGroup = []
grasslocation = []
wolflocation = []

for i in range(sheep_initial_num):
    locationGroup.append([random.randint(10, 1000), random.randint(10, 720)])

for i in range(grass_initial_num):
    grasslocation.append([random.randint(10, 1000), random.randint(10, 720)])

for i in range(wolf_initial_num):
    wolflocation.append([random.randint(10, 1000), random.randint(10, 720)])

SheepGroup = pygame.sprite.Group()
GrassGroup = pygame.sprite.Group()
WolfGroup = pygame.sprite.Group()

# walk direction
for l in locationGroup:
    SheepGroup.add(Sheep(sheep_img, l))

for l in grasslocation:
    GrassGroup.add(Grass(grassimg, l))

for l in wolflocation:
    WolfGroup.add(Wolf(wolf_img, l))

# load window
sheep_indx = 0
wolf_indx = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.time.delay(20)
    window.fill([147, 211, 52])

    # initial map
    sheep_map = []
    grass_map = []
    wolf_map = []
    count_SheepGrass_distance = []
    count_WolfSheep_distance = []
    count_sheepwolf_distance = []
    

    # draw grass
    for grass in GrassGroup.sprites():
        window.blit(grass.image, grass.rect)
        grass_map.append([grass.rect.centerx, grass.rect.centery])
        
        for sheep in SheepGroup.sprites():
            if([grass.rect.centerx, grass.rect.centery] in grass_map and [grass.rect[0], grass.rect[1]] in grasslocation):
                if [sheep.rect.centerx, sheep.rect.centery] == [grass.rect.centerx, grass.rect.centery]:
                        grass.die()
                        sheep.live += 10
                        grass_map.remove([grass.rect.centerx, grass.rect.centery])
                        grasslocation.remove([grass.rect[0], grass.rect[1]])
                        if(random.randint(1, 3)==3):
                            grasslocation.append([random.randint(10, 1000), random.randint(10, 720)])
                
    if(random.randint(1, 500) >= 450):
        grasslocation.append([random.randint(10, 1000), random.randint(10, 720)])
  
    # draw and move sheep
    time = 0
    
    for idx, sheep in enumerate(SheepGroup.sprites()):
        sheep.move()
        x = sheep.rect.centerx
        y = sheep.rect.centery
        if sheep.speed[0] < 0:
            window.blit(pygame.transform.flip(sheep.imagelist[sheep_indx], True, False), sheep.rect)
        else:
            window.blit(sheep.imagelist[sheep_indx], sheep.rect)
        sheep_map.append([sheep.rect.centerx, sheep.rect.centery])

        coming = 0                       
         # eaten
        for wolf in WolfGroup.sprites():
            wolf_map.append([wolf.rect.centerx, wolf.rect.centery])
            if([x, y] in sheep_map):
                    if pygame.Rect.colliderect(sheep.rect, wolf.rect):
                        wolf.live += sheep.live / 2
                        sheep.die()
                        locationGroup.remove(locationGroup[idx])
                        sheep_map.remove([x, y])
            distance = (wolf.rect.centerx - x)**2 + (wolf.rect.centery - y)**2
            count_sheepwolf_distance.append(distance)

            if(distance <= 50000):
                coming = 1

                # min_value = min(count_sheepwolf_distance)
                # min_index = count_sheepwolf_distance.index(min_value)
                # x, y = wolf_map[min_index]
                # nextstep = [(sheep.rect.centerx - x), (sheep.rect.centery - y)]

                # # nextstep = [(x - wolf.rect.centerx), (y - wolf.rect.centery)]
                # if nextstep[0] > 0: dx = 1
                # elif nextstep[0] < 0: dx = -1
                # else: dx = 0
                # if nextstep[1] > 0:dy = 1
                # elif nextstep[1] < 0: dy = -1
                # else: dy = 0
                # if((dx + dy) == 1 or (dx + dy) == -1):
                #     dx *= 1.4142
                #     dy *= 1.4142
        if coming:
            
            min_value = min(count_sheepwolf_distance)
            min_index = count_sheepwolf_distance.index(min_value)
            x, y = wolf_map[min_index]
            nextstep = [(sheep.rect.centerx - x), (sheep.rect.centery - y)]

            if nextstep[0] > 0: dx = 1
            elif nextstep[0] < 0: dx = -1
            else: dx = 0
            if nextstep[1] > 0:dy = 1
            elif nextstep[1] < 0: dy = -1
            else: dy = 0
            if((dx + dy) == 1 or (dx + dy) == -1):
                dx *= 1.4142
                dy *= 1.4142

        else:
            # calculate next(consider grass)
            for position in grass_map:
                x, y = position
                distance = (sheep.rect.centerx - x)**2 + (sheep.rect.centery - y)**2
                count_SheepGrass_distance.append(distance)

                min_value = min(count_SheepGrass_distance)
                min_index = count_SheepGrass_distance.index(min_value)
                x, y = grass_map[min_index]
                nextstep = [(x - sheep.rect.centerx), (y - sheep.rect.centery)]

                #next stop
                if nextstep[0] > 0: dx = 1
                elif nextstep[0] < 0: dx = -1
                else: dx = 0
                if nextstep[1] > 0:dy = 1
                elif nextstep[1] < 0: dy = -1
                else: dy = 0

                if((dx + dy) == 1 or (dx + dy) == -1):
                    dx *= 1.4142
                    dy *= 1.4142
            
        # send info
        sheep.speed = [dx, dy]

        if(sheep.live <= 0):
            sheep.die()
            locationGroup.remove(locationGroup[idx])
            
        if(sheep.live >= 120):
            sheep.live -= 50
            l = [random.randint(10, 1000), random.randint(10, 720)]
            locationGroup.append(l)
            SheepGroup.add(Sheep(sheep_img, l))

        count_SheepGrass_distance = []
        count_sheepwolf_distance = []

        
    # draw new grass
    GrassGroup = pygame.sprite.Group()
    for l in grasslocation:
        GrassGroup.add(Grass(grassimg, l))

    # iter sheep image
    sheep_indx += 1
    if sheep_indx >= 6:
        sheep_indx = 0

    # draw wolf
    for idx, wolf in enumerate(WolfGroup.sprites()):
        wolf.move() 

        if wolf.live <= 0:
            wolf.die()
            wolflocation.remove(wolflocation[idx])

        if wolf.live >= 200:
            wolf.live -= 80
            l = [random.randint(10, 1000), random.randint(10, 720)]
            wolflocation.append(l)
            WolfGroup.add(Wolf(wolf_img, l))

        if wolf.speed[0] < 0:
            window.blit(pygame.transform.flip(wolf.imagelist[wolf_indx], True, False), wolf.rect)
        else:
            window.blit(wolf.imagelist[wolf_indx], wolf.rect)

        for position in sheep_map:
            x, y = position
            distance = (wolf.rect.centerx - x)**2 + (wolf.rect.centery - y)**2
            count_WolfSheep_distance.append(distance)
        
        min_value = min(count_WolfSheep_distance)
        min_index = count_WolfSheep_distance.index(min_value)
        x, y = sheep_map[min_index]
        nextstep = [(x - wolf.rect.centerx), (y - wolf.rect.centery)]

        #next stop
        if (nextstep[0] < 2 and nextstep[0] > 0) or (nextstep[0] > -2 and nextstep[0] < 0):dx=nextstep[0]
        elif nextstep[0] > 0: dx = 2
        elif nextstep[0] < 0: dx = -2
        else: dx = 0

        if (nextstep[1] < 2 and nextstep[1] > 0) or (nextstep[1] > -2 and nextstep[1] < 0):dy=nextstep[1]
        elif nextstep[1] > 0:dy = 2
        elif nextstep[1] < 0: dy = -2
        else: dy = 0

        if((dx + dy) == 2 or (dx + dy) == -2):
            dx *= 1.4142
            dy *= 1.4142
        
        # send info
        wolf.speed = [dx, dy]

        
        count_WolfSheep_distance =[]

    # iter wolf image
    wolf_indx += 1
    if wolf_indx >=6:
        wolf_indx = 0



    # count sheep
    print('Total Sheep :{}'.format(len(sheep_map)))

    pygame.time.delay(80)
    pygame.display.update()