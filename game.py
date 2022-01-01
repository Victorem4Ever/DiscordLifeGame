import pygame, pytmx, pyscroll
from player import Player
from screens import Screens
from tasks import Tasks


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((800,800))

        self.screens = Screens(self.screen)

        pygame.display.set_caption("SocialNetwork Simulator")

        tmx_data = pytmx.load_pygame("assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3.5

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        self.frames = {
            "up" : 0,
            "down" : 0,
            "right" : 0,
            "left" : 0
        }
        self.frame_value = 0.20

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        self.task = Tasks(self.screen)

    

    def handle_input(self):
        value = 2
        up, down, right, left = (False, False, False, False)
        self.player.old_position = self.player.position.copy()


        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z] or pressed[pygame.K_UP]:
            self.player.position[1] -= value

            if self.frames["up"] < len(self.player.animations["up"]):
                self.player.image = self.player.animations["up"][int(self.frames["up"])]
                self.frames["up"] += self.frame_value

            else:
                self.frames["up"] = 0
                self.player.image = self.player.animations["up"][self.frames["up"]]

            up = True

        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            self.player.position[1] += value

            if self.frames["down"] < len(self.player.animations["down"]):
                self.player.image = self.player.animations["down"][int(self.frames["down"])]
                self.frames["down"] += self.frame_value

            else:
                self.frames["down"] = 0
                self.player.image = self.player.animations["down"][self.frames["down"]]

            down = True


        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            self.player.position[0] += value

            if self.frames["right"] < len(self.player.animations["right"]):
                self.player.image = self.player.animations["right"][int(self.frames["right"])]
                self.frames["right"] += self.frame_value

            else:
                self.frames["right"] = 0
                self.player.image = self.player.animations["right"][self.frames["right"]]
            
            right = True


        if pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
            self.player.position[0] -= value

            if self.frames["left"] < len(self.player.animations["left"]):
                self.player.image = self.player.animations["left"][int(self.frames["left"])]
                self.frames["left"] += self.frame_value

            else:
                self.frames["left"] = 0
                self.player.image = self.player.animations["left"][self.frames["left"]]
            
            left = True
        
        self.player.image.set_colorkey([0,0,0])


        if not up: self.frames["up"] = 0

        if not down: self.frames["down"] = 0

        if not right: self.frames["right"] = 0

        if not left: self.frames["left"] = 0


    def run(self):

        if not self.screens.menu():
            return
        
        self.screens.load_game()


        clock = pygame.time.Clock()
        running = True
        while running:
            self.handle_input()

            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)

            #if self.player.rect.collidelist(self.walls) > -1:
                #self.player.move_back()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()