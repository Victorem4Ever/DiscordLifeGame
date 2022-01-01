import pygame, time, random, pygame_textinput
from button import Button
from screens import Screens

class Tasks:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bots = []
        self.screens = Screens(screen)
        self.x, self.y = self.screen.get_size()
        self.bot_image = pygame.image.load("assets/bot.png")
        self.font = pygame.font.Font("freesansbold.ttf", 20)

        self.tasks = {
            "raider" : [
                self.raid_bot
            ],
            "dev" : [

            ],
            "hacker" : [
                self.bruteforce
            ],
            "modo" : [

            ],
            "fonda" : [

            ],
            "membre" : [

            ],
            "egirl" : [
                self.uwu
            ]
        }


    def raid_bot(self, duration=60, nb=200):
        start = time.time()
        s = time.time()
        bg = pygame.image.load("assets/raid.jpg")
        hitted = 0

        self.create_bots(10)

        while time.time() - start <= duration and hitted < nb:
            
            self.screen.blit(bg, (0,0))


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            for i in range(len(self.bots)):
                if self.bots[i] is not None and self.bots[i].draw():
                    self.bots[i] = None
                    hitted += 1
                    print(hitted)
                    print(time.time()-start)


            if time.time() - s >= 1:
                s = time.time()
                self.create_bots(5)



            self.screen.blit(self.font.render(f"TIME LEFT : {'{0:.1f}'.format(duration-(time.time()-start))}s", True, (255,0,0)), (20,30))
            self.screen.blit(self.font.render(f"BOT(S) LEFT : {nb-hitted} bot(s)", True, (255,0,0)), (20,80))

            pygame.display.flip()
            self.clock.tick(60)

        self.bots = []

        if hitted < nb:
            self.screens.defeat()
            return False

        else:
            self.screens.victory()
            return True


    def create_bots(self, nb):

        for _ in range(nb):
            pos = (random.randint(0, self.x-20), random.randint(0, self.y-20))
            self.bots.append(Button(pos, self.bot_image, self.screen))





    def bruteforce(self, duration=600, nb=10):

        start = time.time()
        bg = pygame.image.load("assets/bruteforce.png")

        while time.time() - start <= duration:
            
            self.screen.blit(bg, (0,0))
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

            self.screen.blit(self.font.render(f"TIME LEFT : {'{0:.1f}'.format(duration-(time.time()-start))}s", True, (255,0,0)), (20,30))
            

            pygame.display.flip()


    
    def socialNetworkUI(self, duration=60, max_chars=50, messages_color=(255,255,255), specific_color=("uwu", (205,96,190))):

        start = time.time()
        manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= max_chars)
        textinput = pygame_textinput.TextInputVisualizer(manager=manager)
        textinput.font_color = (255,255,255)

        messages = []

        while time.time() - start <= duration:

            self.screen.fill((69,69,69))

            events = pygame.event.get()

            textinput.update(events)
            self.screen.blit(textinput.surface, (20,750))



            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and textinput.value:
                    messages.append(textinput.value)
                    yield textinput.value
                    textinput.value = ""
                    textinput.update(events)


            for i in range(1, len(messages)+1):
                if specific_color[0] in messages[-i].lower():
                    self.screen.blit(self.font.render(messages[-i], True, specific_color[1]), (40, 700-20*i))
                else:
                    self.screen.blit(self.font.render(messages[-i], True, messages_color), (40, 700-20*i))


            pygame.display.flip()
            self.clock.tick(60)



    def uwu(self, duration=60, nb=30):

        uwu_nb = 0

        for message in self.socialNetworkUI(duration=duration, messages_color=(255,255,255)):
            if "uwu" in message.lower():
                uwu_nb += 1

                if uwu_nb == nb:
                    self.screens.victory()
                    return True
        
        self.screens.defeat()
        return False