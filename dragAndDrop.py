import pygame

class DragAndDrop:

    def __init__(self, button):
        self.stop = False
        self.x, self.y = button.rect.topleft
        self.screen = button.screen
        self.button = button
        self.drag = False

    
    def update(self, events):

        clicked = False

        if self.button.draw():
            self.drag = True
            clicked = True


        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.drag = False


            elif event.type == pygame.MOUSEMOTION and self.drag:
                self.button.rect.x, self.button.rect.y = event.pos

        return clicked