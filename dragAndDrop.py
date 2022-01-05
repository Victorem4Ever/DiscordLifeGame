import pygame

class DragAndDrop:

    def __init__(self, button):
        self.stop = False
        self.x, self.y = button.rect.topleft
        self.screen = button.screen
        self.button = button
        self.drag = False

    
    def update(self, events):

        clicked = (False, False)

        if self.button.draw():
            self.drag = True
            clicked = (True, False)


        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.drag = False


            elif event.type == pygame.MOUSEMOTION and self.drag:
                self.button.rect.x, self.button.rect.y = event.pos

            elif not clicked[0] and event.type == pygame.MOUSEBUTTONDOWN:
                clicked = (False, True)

        return clicked