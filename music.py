import pygame

class Music:

    def __init__(self):

        self.lobby_playing = False
        self.musics = {
            "lobby_intro" : pygame.mixer.Sound("assets/music/lobby_intro.wav"),
            "lobby_loop" : pygame.mixer.Sound("assets/music/lobby_loop.wav")#,
            #"house" : pygame.mixer.Sound("assets/music/house.mp3")
        }

    
    def stop(self):
        
        pygame.mixer.stop()
        self.lobby_playing = False


    def lobby(self):
        
        if not self.lobby_playing:
            self.stop()
            self.lobby_playing = True

            self.musics["lobby_intro"].play()

        else:
            if not pygame.mixer.get_busy():
                self.musics["lobby_loop"].play(-1)