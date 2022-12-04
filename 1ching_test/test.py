import pygame, sys

pygame.init()

class Sheep(pygame.sprite.Sprite):
    def __init__(self, filename, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.position = initial_position
      

window = pygame.display.set_mode([640, 480])
window.fill([147, 211, 52])

sheep_img = 'sheep.png'
locationGroup = ([350, 300], [250, 300], [450, 260])
SheepGroup = pygame.sprite.Group()

for l in locationGroup:
    SheepGroup.add(Sheep(sheep_img, l))

for sheep in SheepGroup.sprites():
    window.blit(sheep.image, sheep.rect)

pygame.display.update()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()