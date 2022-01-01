import pygame
from button import Button

class Screens:

    def __init__(self, screen):

        self.screen = screen
        self.menu_image = pygame.image.load("assets/menu/menu.jpg")
        self.exit_image = pygame.image.load("assets/menu/exit.png")
        self.play_image = pygame.image.load("assets/menu/play.png")
        #self.defeat_image = pygame.image.load("assets/menu/defeat.png")
        #self.victory_image = pygame.image.load("assets/menu/victory.png")



    def defeat(self):

        self.play_button = Button((400,400), self.play_image, self.screen)
        self.exit_button = Button((120,200), self.exit_image, self.screen)

        while True:
            
            self.screen.blit(self.defeat_image, (0,0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False


            if self.play_button.draw():
                return True

            if self.exit_button.draw():
                return False
            

            pygame.display.flip()



    def victory(self):

        self.play_button = Button((400,400), self.play_image, self.screen)
        self.exit_button = Button((120,200), self.exit_image, self.screen)

        while True:
            
            self.screen.blit(self.victory_image, (0,0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False


            if self.play_button.draw():
                return True

            if self.exit_button.draw():
                return False
            

            pygame.display.flip()



    def menu(self):

        self.exit_button = Button((400,400), self.exit_image, self.screen)
        self.play_button = Button((120,200), self.play_image, self.screen)

        while True:

            self.screen.blit(self.menu_image, (0,0))

            if self.play_button.draw():
                return True

            if self.exit_button.draw():
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

            pygame.display.flip()



    def load_game(self):
        pass