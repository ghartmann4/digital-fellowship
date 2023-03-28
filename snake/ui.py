from enum import Enum
from tkinter import W
import pygame
import time

class Fruit_type:
    APPLE = 1
    SPICY_PEPPER = 2
    GOLDEN_APPLE = 3

class Coordinate:
    def __init__(self, *, row, column):
        self._row = row
        self._column = column
       
    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column


class Key_events(Enum):
    LEFT=1
    RIGHT=2
    UP=3
    DOWN=4
    QUIT=5



class Ui:
    """
    Renders shapes on a display window. Must call `init` before using
    """

    def __init__(self, *, height, width, grid_pixel_size=10, background_color="white"):
        self._height = height
        self._width = width
        self._grid_pixel_size = grid_pixel_size
        self._background_color = background_color
        pygame.init()
        self._font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = ""
        self.textRect = None
        self.pepper_image = pygame.image.load('pepper_20.png')
        self.green_apple_image = pygame.image.load('green_apple_20.png')
        self.golden_apple_image = pygame.image.load('golden_apple_20.png')


        self._display = pygame.display.set_mode((height, width))

    def write_text(self, given_text, x_pos=0, y_pos=0):

        # create a text surface object,
        # on which text is drawn on it.
        self.text = self._font.render(given_text, True, "black", "white")
        
        # create a rectangular object for the
        # text surface object
        self.textRect = self.text.get_rect()
        self.textRect.x = x_pos
        self.textRect.y = y_pos
        

    @staticmethod
    def get_relevant_keyevents(): 
        keypresses = []
        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN:
                continue 
            keypress = None
            if event.key == pygame.K_LEFT:
                keypress = Key_events.LEFT
            if event.key == pygame.K_RIGHT:
                keypress = Key_events.RIGHT
            if event.key == pygame.K_DOWN:
                keypress=  Key_events.DOWN
            if event.key == pygame.K_UP:
                keypress = Key_events.UP
            if event.key == pygame.QUIT:
                keypress=  Key_events.QUIT

            if keypress is not None:
                keypresses.append(keypress)
        return keypresses
        
    def init(self):
        pygame.init()
        pygame.display.set_mode((self._width * self._grid_pixel_size, self._height * self._grid_pixel_size))

    def _screen_pixel(self, *, row, column):
        pixel_row = row * self._grid_pixel_size
        pixel_column = column * self._grid_pixel_size
        return Coordinate(row=pixel_row, column=pixel_column)

    def render(self):
        """ Renders all the graphics drawn on the display """
        self._display.blit(self.text, self.textRect)
        pygame.display.update()
        
    def end_game(self):
        pygame.quit()
        self.clear()
        
    def clear(self):
        """ Clears the display window """
        self._display.fill(self._background_color)

    def fill_square(self,*, row, column, color='blue'):
        pixel = self._screen_pixel(row=row, column=column)
        row, column = pixel.row, pixel.column
        width = self._grid_pixel_size
        pygame.draw.rect(self._display, color, [row, column, width, width])

    def draw_circle(self, *, row, column, color='red'):
        pixel = self._screen_pixel(row=row, column=column)
        radius = self._grid_pixel_size // 2
        row = pixel.row + radius
        column = pixel.column + radius
        pygame.draw.circle(self._display, color, (row , column ), radius)

    def draw_fruit(self, type, *, row, column):
        if type == Fruit_type.APPLE:
            img = self.green_apple_image
        elif type == Fruit_type.GOLDEN_APPLE:
            img = self.golden_apple_image
        elif type == Fruit_type.SPICY_PEPPER:
            img = self.pepper_image
        row = row * self._grid_pixel_size
        column = column * self._grid_pixel_size
        self._display.blit(img, (row,column))
    




def run_example():
    """
    Move a circle and a square along a diagonal 
    """
    size = 20
    grid_pixel_size = 10
    sleep_seconds = 0.1
    ui = Ui(width=size, height=size, grid_pixel_size=grid_pixel_size)
    coord = 0
    ui.init()
    while True:
        last_key = ui.get_relevant_keyevents()
        print(last_key)
        ui.clear()
        ui.fill_square(row=coord, column=coord)
        ui.fill_square(row=coord + 1, column=coord + 1)
        ui.draw_circle(row=coord, column=coord)
        coord = (coord + 1) % size
        ui.render()
        time.sleep(sleep_seconds)


if __name__=="__main__":
    run_example()
        
        
