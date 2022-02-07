import pygame
from player import Player

class Radar:

    def __init__(self, screen, player_position, side=0, pos=None, size=(800, 800), map="assets/map_radar.png"):
        """
        1 Means topright
        2 Means bottomleft
        3 Means bottomright
        0 or other means topleft
        """
        self.screen = screen
        self.radar_pos = pos

        self.map = pygame.image.load(map)

        if self.radar_pos is None:
            if side == 1:
                self.radar_pos = (700, 20)

            elif side == 2:
                self.radar_pos = (20, 700)

            elif side == 3:
                self.radar_pos = (700, 700)

            else:
                self.radar_pos = (20, 20)


    def switch(self, map):
        self.map = pygame.image.load(map)


    def update(self, pos):
        position = [5 + self.radar_pos[0] + pos[0] // 5, 5 + self.radar_pos[1] + pos[1] // 5]
        self.screen.blit(self.map, self.radar_pos)
        pygame.draw.circle(self.screen, (0, 0, 0), position, 2)
        
        pygame.display.flip()