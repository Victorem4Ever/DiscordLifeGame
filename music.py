import pygame

class Music:

    def __init__(self):

        self.lobby_playing = False
        self.musics = {
            "lobby_intro" : pygame.mixer.Sound("assets/music/lobby_intro.wav"),
            "lobby_loop" : pygame.mixer.Sound("assets/music/lobby_loop.wav")#,
            #"house" : pygame.mixer.Sound("assets/music/house.mp3")
        }
        self.current_music = None

    
    def stop(self, fadeout=50):
        
        pygame.mixer.fadeout(fadeout)
        self.lobby_playing = False


    def lobby(self):
        
        if not self.lobby_playing:
            self.stop()
            self.lobby_playing = True

            self.current_music = "lobby_intro"
            self.musics["lobby_intro"].play()

        else:
            if not pygame.mixer.get_busy():
                self.current_music = "lobby_loop"
                self.musics["lobby_loop"].play(-1)

    
    def change_vol(self, volume=1):

        self.musics[self.current_music].set_volume(volume)