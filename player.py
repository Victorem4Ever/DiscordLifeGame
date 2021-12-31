import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("assets/players/player.png")
        
        self.animations = {
            "down" : [
                self.get_image(0,0),
                self.get_image(32,0),
                self.get_image(64,0)
            ],

            "left" : [
                self.get_image(0,32),
                self.get_image(32,32),
                self.get_image(64,32)
            ],
            "right" : [
                self.get_image(0,64),
                self.get_image(32,64),
                self.get_image(64,64)
            ],
            "up" : [
                self.get_image(0,96),
                self.get_image(32,96),
                self.get_image(64,96)
            ]
        }

        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()
        self.position = [x,y]
        self.old_position = self.position.copy()



    def update(self):
        self.rect.topleft = self.position


    def get_image(self, x, y):
        image = pygame.Surface([96,128])
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image

    
    def move_back(self):
        self.position = self.old_position.copy()
        self.update()