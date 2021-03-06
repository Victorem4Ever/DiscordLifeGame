import pygame, pytmx, pyscroll, json, time
from player import Player
from screens import Screens
from tasks import Tasks
from radar import Radar
from music import Music


class Game:

    def __init__(self):

        self.music = Music()

        self.screen = pygame.display.set_mode((800,800))

        self.screens = Screens(self.screen)
        self.screens.music = self.music

        pygame.display.set_caption("SocialNetwork Simulator")

        tmx_data = pytmx.load_pygame("assets/carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3.5

        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y, self.screen)

        self.map = "world"
        self.house = None

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


        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        self.task = Tasks(self.screen, self.music)
        self.task_panels = []

        self.house_rects = []
        for i in range(7):
            enter_house = tmx_data.get_object_by_name("enter_house" + str(i))
            self.house_rects.append((pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height), "house" + str(i)))
        
        self.radar = Radar(self.screen, side=1)
        self.stopped_since = time.time()

    


    def switch(self, house=None):

        self.house = house if house is not None else self.house

        self.map = "house" if self.map == "world" else "world"

        path = "assets/houses/" + house + ".tmx" if self.map == "house" else "assets/carte.tmx"

        tmx_data = pytmx.load_pygame(path)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3.5

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            elif obj.type == "task_panel":
                self.task_panels.append((pygame.Rect(obj.x, obj.y, obj.width, obj.height), self.task.tasks[self.player.infos["name"]][int(house[-1])]))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        house_objs = []
        self.house_rects = []
        if self.map == "house":
            house_objs.append((tmx_data.get_object_by_name("exit_house"), None))
        
        else:
            for i in range(7):
                house_objs.append((tmx_data.get_object_by_name("enter_house" + str(i)), "house" + str(i)))
        
        for house_obj, house in house_objs:
            self.house_rects.append((pygame.Rect(house_obj.x, house_obj.y, house_obj.width, house_obj.height), house))

        spawn = tmx_data.get_object_by_name("spawn_house") if self.map == "house" else tmx_data.get_object_by_name("exit_spawn_" + self.house)
        self.player.position = [spawn.x, spawn.y-20]

        if self.map == "world":
            self.radar.stop = False
            self.radar.switch("assets/map_radar.png")

        else:
            self.radar.stop = True
            self.music.stop(100)



    def handle_input(self):
        value = 2
        up, down, right, left = (False, False, False, False)
        self.player.old_position = self.player.position.copy()
        self.player.update()


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
        

        if pressed[pygame.K_ESCAPE]:
            
            if not self.screens.menu():
                self.save()
                pygame.quit()
                return False

        self.player.image.set_colorkey([0,0,0])


        if not up: self.frames["up"] = 0

        if not down: self.frames["down"] = 0

        if not right: self.frames["right"] = 0

        if not left: self.frames["left"] = 0

        if up or down or right or left:
            self.stopped_since = time.time()

        return True



    def save(self):
        
        if not self.player.infos: return

        with open(self.player.infos["path"], "w") as file:
            json.dump(self.player.infos, file)
            file.close()



    def run(self):


        if not self.player.started: return
        if not self.player.infos: return
        self.save()


        clock = pygame.time.Clock()
        running = True
        while running:

            if self.map == "world": self.music.lobby()

            if not self.handle_input(): return

            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)




            for rec, house in self.house_rects:
                if self.player.feet.colliderect(rec):
                    self.switch(house)
                    break


            for sprite in self.group.sprites():
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()


            if time.time() - self.stopped_since < 3:
                self.radar.update(self.player.position)


            for rec, task in self.task_panels:
                if self.player.feet.colliderect(rec):
                    if task():
                        self.player.infos["wins"] += 1
                    
                    else:
                        self.player.infos["defeats"] += 1

                    self.player.position[0] += 5
                    self.player.position[1] +=5


            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()