import pygame

class Button:

    def __init__(self, xy, image, screen):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.clicked = False
        self.screen = screen


    def draw(self):
        action = False
		
        pos = pygame.mouse.get_pos()
		
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            action = True
		
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        return action