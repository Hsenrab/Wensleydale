import pygame
import OpenGL
import math
import os
os.environ['SDL_VIDEODRIVER'] = 'directx'

background_colour = (247, 231, 200)
(width, height) = (420, 300)
fps = 120


class Eye:
    def __init__(self, x , y, size):

        self.x = x
        self.y = y
        self.size = size

        self.pupil_x = x
        self.pupil_y = y
        self.pupil_ratio = 2
        self.pupil_size = int(size/self.pupil_ratio)

        self.eye_border_colour = (0,0,0)
        self.eye_colour = (255,255,255)
        self.eye_border_thickness = 1

        self.pupil_colour = (20, 20, 20)
        self.pupil_thickness = 0

        self.num_moves_remaining = 0
        self.x_step = 0
        self.y_step = 0


    def display(self):
        pygame.draw.circle(screen, self.eye_colour, (self.x, self.y), self.size, 0)
        pygame.draw.circle(screen, self.eye_border_colour, (self.x, self.y), self.size, self.eye_border_thickness)
        pygame.draw.circle(screen, self.pupil_colour, (int(self.pupil_x), int(self.pupil_y)), self.pupil_size, self.pupil_thickness)

    def move(self):
        if(self.num_moves_remaining != 0):
            self.pupil_x += self.x_step
            self.pupil_y += self.y_step
            self.num_moves_remaining -= 1

    def move_to(self, new_pupil_x, new_pupil_y, time):

        if(new_pupil_x < self.x - math.ceil(self.pupil_size/2)):
            new_pupil_x = self.x - math.ceil(self.pupil_size/2)

        if(new_pupil_x > self.x + math.ceil(self.pupil_size/2)):
            new_pupil_x = self.x + math.ceil(self.pupil_size/2)

        if(new_pupil_y < self.y - math.ceil(self.pupil_size/2)):
            new_pupil_y = self.y - math.ceil(self.pupil_size/2)
        
        if(new_pupil_y > self.y + math.ceil(self.pupil_size/2)):
            new_pupil_y = self.y + math.ceil(self.pupil_size/2)

        delta_x = new_pupil_x - self.pupil_x
        delta_y = new_pupil_y - self.pupil_y

        self.num_moves_remaining = fps*time
        self.x_step = delta_x/self.num_moves_remaining
        self.y_step = delta_y/self.num_moves_remaining




clock=pygame.time.Clock()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
pygame.display.set_caption('Virtual Eyes')
screen.fill(background_colour)

left_eye = Eye(140, 150, 70)
right_eye = Eye(280, 150, 70)

left_eye.display()
right_eye.display()

left_eye.move_to(40, 150, 1)
right_eye.move_to(180, 150, 2)

pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(fps)
    screen.fill(background_colour)

    left_eye.move()
    right_eye.move()
    left_eye.display()
    right_eye.display()

    pygame.display.flip()
    


