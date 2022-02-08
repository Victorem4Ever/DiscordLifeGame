import pygame, random

class Ball:

    def __init__(self, screen, pos, bottom, right):
        self.screen = screen
        self.x, self.y = pos
        self.bottom = bottom
        self.right = right

        self.x_velocity = 3
        self.y_velocity = 3


    def draw(self):
        pygame.draw.circle(self.screen, (255,255,255), (int(self.x), int(self.y)), 10)
    
    def move(self, y1, y2):

        self.x -= self.x_velocity
        self.y -= self.y_velocity

        if self.y <= 0 or self.y >= self.bottom:
            self.y_velocity = -self.y_velocity

        if (self.x <= 50 and y1 <= self.y <= y1 + 60) or (self.x >= self.right - 50 and y2 <= self.y <= y2 + 60):
            self.x_velocity = -self.x_velocity
            return True
        




class Minigame:

    def __init__(self, screen):

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.x, self.y = screen.get_size()
        self.font = pygame.font.Font("freesansbold.ttf", 50)


    def snake(self):


        def generate_food(snake_size):
            foodx = random.randint(0, (self.x - snake_size) // snake_size) * snake_size
            foody = random.randint(0, (self.y - snake_size) // snake_size) * snake_size
            return foodx, foody


        x = self.x // 2
        y = self.y // 2

        snake_size = 20
        snake_lenght = 1

        foodx, foody = generate_food(snake_size)

        x_change = 0
        y_change = 0

        running = True

        while running:

            self.screen.fill((69,69,69))

            for event in pygame.event.get():

                if event.type in (pygame.QUIT, pygame.K_ESCAPE):
                    running = False
                    return False

                elif event.type == pygame.KEYDOWN:

                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                        x_change, y_change = (0,0)

                    if event.key == pygame.K_UP:
                        y_change = snake_size

                    if event.key == pygame.K_DOWN:
                        y_change = - snake_size

                    if event.key == pygame.K_LEFT:
                        x_change = - snake_size

                    if event.key == pygame.K_RIGHT:
                        x_change = snake_size


            x += x_change
            y -= y_change

            if not x or not y or x >= 800 or y >= 800:
                running = False
                self.disp_score(snake_lenght)

            elif x == foodx and y == foody:
                foodx, foody = generate_food(snake_size)
                snake_lenght += 1

            pygame.draw.rect(self.screen, (255,0,0), [foodx, foody, snake_size, snake_size])
            pygame.draw.rect(self.screen, (50, 100, 255), [x, y, snake_size, snake_size])



            pygame.display.flip()
            self.clock.tick(15)


    def pong(self):

        pos = [
            [[50, self.y//2 - 30], [50, self.y//2 + 30]],
            [[self.x - 50, self.y//2 - 30], [self.x - 50, self.y//2 + 30]]     
        ]
        player = 0
        score = 0
        speed = 5
        y_change = 0
        ball = Ball(self.screen, (random.randint(400, self.x - 100), random.randint(0, self.y)), self.y, self.x)

        running = True
        while running:

            self.screen.fill((0,0,0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    return False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        y_change = -speed

                    elif event.key == pygame.K_DOWN:
                        y_change = speed


                elif event.type == pygame.KEYUP:

                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        y_change = 0

            if pos[player][0][1] + y_change >= 0 and pos[player][1][1] + y_change <= self.y:
                pos[player][0][1] += y_change
                pos[player][1][1] += y_change


            if self.y <= ball.x or ball.x < 0:
                self.disp_score(score)
                return

            if ball.move(pos[0][0][1], pos[1][0][1]):
                player = abs(player-1)
                score += 1
                ball.x_velocity += 0.1
                ball.y_velocity += 0.1
            
            ball.draw()
            pygame.draw.line(self.screen, (255, 255, 255), pos[0][0], pos[0][1], 5)
            pygame.draw.line(self.screen, (255,255,255), pos[1][0], pos[1][1], 5)

            pygame.display.flip()
            self.clock.tick(60)


    def disp_score(self, score):

        running = True
        while running:
            self.screen.fill((69,69,69))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    return

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return

            self.screen.blit(self.font.render(f"Score : {score}", True, (20, 150, 255)), (50, self.y//2))
            
            pygame.display.flip()
            self.clock.tick(60)



if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Snake")

    minigame = Minigame(screen)
    minigame.pong()