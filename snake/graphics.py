from enum import Enum
from tkinter import W
import pygame
import time


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


class Ui:
    """
    Renders shapes on a display window. Must call `init` before using
    """

    def __init__(self, *, height, width, grid_pixel_size=10, background_color="white"):
        self._height = height
        self._width = width
        self._grid_pixel_size = grid_pixel_size
        self._background_color = background_color

        self._display = pygame.display.set_mode((height, width))
        
    def init(self):
        pygame.init()
        pygame.display.set_mode((self._width * self._grid_pixel_size, self._height * self._grid_pixel_size))

    def _screen_pixel(self, *, row, column):
        pixel_row = row * self._grid_pixel_size
        pixel_column = column * self._grid_pixel_size
        return Coordinate(row=pixel_row, column=pixel_column)

    def render(self):
        """ Renders all the graphics drawn on the display """
        pygame.display.update()

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
        ui.clear()
        ui.fill_square(row=coord, column=coord)
        ui.fill_square(row=coord + 1, column=coord + 1)
        ui.draw_circle(row=coord, column=coord)
        coord = (coord + 1) % size
        ui.render()
        time.sleep(sleep_seconds)


if __name__=="__main__":
    run_example()
        
        
