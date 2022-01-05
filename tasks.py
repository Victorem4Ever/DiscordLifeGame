import pygame, time, random, pygame_textinput, string, pyperclip
from button import Button
from screens import Screens
from dragAndDrop import DragAndDrop

class Tasks:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bots = []
        self.screens = Screens(screen)
        self.x, self.y = self.screen.get_size()
        self.bot_image = pygame.image.load("assets/bot.png")
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.font2 = pygame.font.Font("freesansbold.ttf", 30)
        self.tasks = {
            "raider" : [

            ],
            "dev" : [

            ],
            "hacker" : [
                self.bruteforce
            ],
            "modo" : [
                self.raid_bot
            ],
            "fonda" : [

            ],
            "membre" : [

            ],
            "egirl" : [
                self.uwu
            ]
        }

        self.pygame_images = {
            "if" : pygame.image.load("assets/dev_buttons/if.png"),
            "else" : pygame.image.load("assets/dev_buttons/else.png"),
            "variable" : pygame.image.load("assets/dev_buttons/variable.png"),
            "start" : pygame.image.load("assets/dev_buttons/start.png"),
            "end" : pygame.image.load("assets/dev_buttons/end.png"),
            "print" : pygame.image.load("assets/dev_buttons/print.png")
        }


    def raid_bot(self, duration=60, nb=200):
        """
        A task where the player needs to destroy a number of bot
        (200 as default) in a duration time of 60 as default.
        """


        start = time.time()
        s = time.time()
        bg = pygame.image.load("assets/raid.jpg")
        hit = 0

        # Generate 10 bots
        for _ in range(10):
            pos = (random.randint(0, self.x-20), random.randint(0, self.y-20))
            self.bots.append(Button(pos, self.bot_image, self.screen))

        while time.time() - start <= duration and hit < nb:
            
            self.screen.blit(bg, (0,0))

            # Event loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            for i in range(len(self.bots)):
                if self.bots[i] is not None and self.bots[i].draw():
                    self.bots[i] = None
                    hit += 1


            # Generate 5 bots all the 1 second
            if time.time() - s >= 1:
                s = time.time()

                for _ in range(5):
                    pos = (random.randint(0, self.x-20), random.randint(0, self.y-20))
                    self.bots.append(Button(pos, self.bot_image, self.screen))



            self.screen.blit(self.font.render(f"TIME LEFT : {'{0:.1f}'.format(duration-(time.time()-start))}s", True, (255,0,0)), (20,30))
            self.screen.blit(self.font.render(f"BOT(S) LEFT : {nb-hit} bot(s)", True, (255,0,0)), (20,80))

            pygame.display.flip()
            self.clock.tick(60)

        self.bots = []

        if hit < nb:
            return False

        else:
            return True



    def bruteforce(self, duration=600, nb=4):
        """
        A task where the player needs to bruteforce a password of a number of chars (4 as default)
        with simply an hashed version of this password.
        He has a maximum duration time (600 secondes as default)
        """


        start = time.time()
        bg = pygame.image.load("assets/bruteforce.jpg")
        copy_button = Button((50,120), pygame.image.load("assets/menu/copy.png"), self.screen)
        password = hash("".join(random.sample(list(string.printable), k=nb)))

        manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= nb)
        textinput = pygame_textinput.TextInputVisualizer(manager=manager,font_color=(255,255,255))


        while time.time() - start <= duration:
            
            self.screen.blit(bg, (0,0))
            
            events = pygame.event.get()

            textinput.update(events)

            for event in events:
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                    if hash(textinput.value) == password:
                        return True

                    else:
                        textinput.value = ""
                        textinput.update(events)

            if copy_button.draw():
                pyperclip.copy(str(password))


            self.screen.blit(self.font.render(f"TIME LEFT : {'{0:.1f}'.format(duration-(time.time()-start))}s", True, (255,0,0)), (20,30))
            self.screen.blit(self.font2.render("Hashed password : " + str(password), True, (255,0,0)), (50, 50))
            self.screen.blit(textinput.surface, (50,750))

            pygame.display.flip()

        return False


    
    def socialNetworkUI(self, duration=60, max_chars=50, messages_color=(255,255,255), specific_color=("uwu", (205,96,190))):
        """
        A generator that return the messages typed in the textinput.
        It's a simple social network user interface
        """
        start = time.time()
        manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= max_chars)
        textinput = pygame_textinput.TextInputVisualizer(manager=manager, font_color=(255,255,255))

        messages = []

        # Main loop
        while time.time() - start <= duration:

            self.screen.fill((69,69,69))

            events = pygame.event.get()

            textinput.update(events)
            self.screen.blit(textinput.surface, (20,750))


            # Event loop
            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and textinput.value:
                    messages.append(textinput.value)
                    yield textinput.value
                    textinput.value = ""
                    textinput.update(events)

            # Display the messages in the "chat"
            for i in range(1, len(messages)+1):
                if specific_color[0] in messages[-i].lower():
                    self.screen.blit(self.font.render(messages[-i], True, specific_color[1]), (40, 700-20*i))
                else:
                    self.screen.blit(self.font.render(messages[-i], True, messages_color), (40, 700-20*i))


            pygame.display.flip()
            self.clock.tick(60)



    def uwu(self, duration=60, nb=30):
        """
        A task where the player needs to type UwU a number of times
        (30 as default value) in a duration time (60 seconds as default value)
        """


        uwu_nb = 0

        for message in self.socialNetworkUI(duration=duration, messages_color=(255,255,255)):
            if "uwu" in message.lower():
                uwu_nb += 1

                if uwu_nb == nb:
                    return True
        
        return False


    
    def dev_bot(self):
        """
        A task where the player needs to create a script who do something
        when there is a too important number of messages
        """


        # create instruction buttons
        buttons = {}
        inst = ["if", "print", "else", "variable", "start", "end"]
        for i in range(len(inst)):
            buttons[inst[i]] = Button((10, 100 * i + 20), pygame.image.load("assets/dev_buttons/" + inst[i] + ".png"), self.screen)

        dragNdrops = []
        clicked_btn = False
        linked = []
        reset = False

        # main loop
        while 1:
            self.screen.fill((69,69,69))
            events = pygame.event.get()
            
            # update the drag & drop buttons
            reset = False
            for dnd, instruction in dragNdrops:
                click = dnd.update(events)
                if click[0]:

                    # Check to link buttons
                    if not clicked_btn:
                        clicked_btn = (dnd.button, instruction)
                        reset = False

                    else:
                        if clicked_btn[0] != dnd.button:
                            popped = False
                            for i in range(len(linked)):
                                if linked[i] in (((dnd.button, instruction), clicked_btn) in linked, (clicked_btn, (dnd.button, instruction)) in linked):
                                    linked.pop(i)
                                    popped = True

                            if not popped: linked.append((clicked_btn, (dnd.button, instruction)))

                        clicked_btn = False
                        

                elif click[1]:
                    
                    reset = True
            
            if reset: clicked_btn = False


            for i in inst:
                if buttons[i].draw():
                    x = Button((350,350), self.pygame_images[i], self.screen)
                    dragNdrops.append((DragAndDrop(x), i))


            # Edit the links
            for button1, button2 in linked:
                pygame.draw.line(self.screen, (255,0,0), button1[0].rect.midbottom, button2[0].rect.midtop)


            # Event loop
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            pygame.display.flip()
            self.clock.tick(60)