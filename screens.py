import pygame, json, os
from button import Button

class Screens:

    def __init__(self, screen):

        self.screen = screen
        self.menu_image = pygame.image.load("assets/menu/menu.jpg")
        self.exit_image = pygame.image.load("assets/menu/exit.png")
        self.play_image = pygame.image.load("assets/menu/play.png")
        self.defeat_image = pygame.image.load("assets/menu/defeat.jpg")
        self.victory_image = pygame.image.load("assets/menu/victory.png")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("freesansbold.ttf", 30)



    def defeat(self):

        self.stop_music()

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
            self.clock.tick(60)



    def victory(self):

        self.stop_music()

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
            self.clock.tick(60)



    def menu(self):

        self.stop_music()

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
            self.clock.tick(60)



    def load_game(self):
        
        with open("setting_files.json", "r") as file:
            try:
                data = json.load(file)
            except ValueError:
                file.close()
                return self.create_game()
            file.close()
        
        if not len(data): return self.create_game()

        files = []
        new_button = Button((350, 700), pygame.image.load("assets/menu/new.png"), self.screen)
        load_image = pygame.image.load("assets/menu/load.png")
        load_buttons = []

        for i in range(1, len(data)+1):
            load_buttons.append((Button((650,70*i), load_image, self.screen), i-1))
        
        for i in data:
            files.append((i, data[i]))

        while True:

            self.screen.fill((69,69,69))

            for i in range(len(files)):
                self.screen.blit(self.font.render(files[i][0], True, (255,255,255)), (30, i*70))
            
            for btn, i in load_buttons:
                
                if btn.draw():
                    with open(files[i][1], "r") as file:
                        data = json.load(file)
                        file.close()

                    return data

            if new_button.draw():
                return self.create_game()

            if pygame.QUIT in pygame.event.get():
                pygame.quit()
                return False

            pygame.display.flip()
            self.clock.tick(60)

    
    def create_game(self):

        btn = []

        btn.append((Button((10,10), pygame.image.load("assets/players_logo/raider.png"), self.screen), "raider"))
        btn.append((Button((10,110), pygame.image.load("assets/players_logo/dev.png"), self.screen), "dev"))
        btn.append((Button((10,210), pygame.image.load("assets/players_logo/hacker.png"), self.screen), "hacker"))
        btn.append((Button((110,10), pygame.image.load("assets/players_logo/egirl.png"), self.screen), "egirl"))
        btn.append((Button((110,110), pygame.image.load("assets/players_logo/modo.png"), self.screen), "modo"))
        btn.append((Button((210,10), pygame.image.load("assets/players_logo/fonda.png"), self.screen), "fonda"))
        btn.append((Button((210,110), pygame.image.load("assets/players_logo/member.png"), self.screen), "member"))

        while True:

            for button, name in btn:
                if button.draw():
                    x = 1
                    while os.path.isfile("setting_files/" + name + str(x) + ".json"): x += 1
                    path = "setting_files/" + name + str(x) + ".json"
                    game = {
                        "name" : name,
                        "path" : path,
                        "wins" : 0,
                        "defeats" : 0,
                        "old_players" : [],
                        "easter_egg" : True
                    }
                    with open("setting_files.json", "r") as read_file:
                        try:
                            data = json.load(read_file)
                        except ValueError:
                            data = {}
                        read_file.close()

                    data[name + str(x)] = path
                    with open("setting_files.json", "w") as write_file:
                        json.dump(data, write_file)

                    return game

            if pygame.QUIT in pygame.event.get():
                pygame.quit()
                return False


            pygame.display.flip()
            self.clock.tick(60)


    def stop_music(self):

        self.music.stop()