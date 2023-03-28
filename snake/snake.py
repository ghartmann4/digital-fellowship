from itertools import count
import random
import time 
from enum import Enum
from ui import Ui, Key_events, Fruit_type

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Color_scheme():
    # (head, body)
    SPICY = ("black", "red")
    NORMAL = ("red", "blue")
    GOLD = ("black", "yellow")

class Snake():

    def __init__(self, points, direction):
        # points are in order, so points[0] is head
        self.points = points
        self.direction = direction
        self.color = Color_scheme.NORMAL

    def set_direction(self, new_direction): 
        # to be called by keyboard input 
        # make an array of moves called moves
        # this should only keep the 2 most recent moves made
        self.direction = new_direction

    def move(self):
        # removes last point (tail) and adds new head point
        self.points.pop() # remove tail
        new_head = self.next_head_pos()
        self.points.insert(0, new_head) # add new head
        return

    def lengthen(self):
        # just adds new head point
        new_head = self.next_head_pos()
        self.points.insert(0, new_head) # add new head
        return

    def next_head_pos(self):
        # returns next head position based on direction and current head
        current_head = self.points[0]
        if self.direction == Direction.UP:
            next_head = (current_head[0], current_head[1]-1)

        elif self.direction == Direction.DOWN:
            next_head = (current_head[0], current_head[1]+1)

        elif self.direction == Direction.LEFT:
            next_head = (current_head[0]-1, current_head[1])

        else:
            next_head = (current_head[0]+1, current_head[1])

        return next_head

class Fruit():
    # the most complicated class, get ready
    def __init__(self, location, fruit_type=Fruit_type.APPLE):
        self.location = location
        self.fruit_type = fruit_type

class Game():

    def __init__(self, m, n, speed):
        self.m = m
        self.n = n
        self.speed = speed
        self.move_q = []
        self.score = 0
        self.ui = Ui(width=self.m,grid_pixel_size=20, height=self.n)
        self.ui.init()
        self.game_in_progress = True
        # spicy pepper changes speed_adjustment until next fruit is eaten
        self.speed_adjustment = 0

        # start in middle of grid:
        starting_point = (self.m//2, self.n//2)

        # snake is 3 long to start, starting below starting_point:
        starting_snake_points = [starting_point, ((self.m//2) +1, self.n), ((self.m// 2) +2, self.n)]
        self.snake = Snake(starting_snake_points, Direction.UP)

        self.fruit = None 
        self.generate_fruit()

    def generate_fruit(self):
        # randomly create a fruit object with coordinates that are in the grid and
        # not in snake, and not right in front of the snake (i.e. snake head + direction)
        available_points = []
        for i in range(self.m):
            for j in range(self.n):
                if (i, j) not in self.snake.points and (i,j) != self.snake.next_head_pos():
                    available_points.append((i,j))
        pick = random.choice(available_points)

        num = random.randint(1,10)

        if num == 1:
            new_fruit = Fruit(pick, Fruit_type.SPICY_PEPPER)
        elif num == 2:
            new_fruit = Fruit(pick, Fruit_type.GOLDEN_APPLE)
        else:
            new_fruit = Fruit(pick)

        self.fruit = new_fruit
        return

    def end_game(self):
        self.game_in_progress = False
        # TODO
        # end game


        pass

    def will_collide(self, next_snake_head):
        # return True if snake will collide w/ self or wall

        # hits wall:
        if next_snake_head[0] < 0 or next_snake_head[0] >= self.m or next_snake_head[1] < 0 or next_snake_head[1] >= self.n:
            return True
        # hits self:
        elif next_snake_head in self.snake.points:
            return True
        else:
            return False

    def eat_fruit(self):

        if self.fruit.fruit_type == Fruit_type.SPICY_PEPPER:
            self.speed_adjustment = min(10, self.speed) # n.b. speed adjustment capped at 10; this might need to be adjusted for optimal gameplay
            self.snake.color = Color_scheme.SPICY
        elif self.fruit.fruit_type == Fruit_type.GOLDEN_APPLE:
            self.score += 4 # golden apples are worth 5 points rather than 1
            self.speed_adjustment = 0
            self.snake.color = Color_scheme.GOLD
        else:
            self.speed_adjustment = 0 
            self.snake.color = Color_scheme.NORMAL  

    def render_board(self):
        PIXEL_SIZE = 10
        self.ui.clear()
        for idx, (row,col) in enumerate(self.snake.points):
            head, body = self.snake.color
            color = head if idx == 0 else body
            self.ui.fill_square(row=row, column=col,color=color)

        row, col = self.fruit.location
        self.ui.draw_fruit(self.fruit.fruit_type, row=row, column=col)

        self.ui.render()

    def game_turn(self):
        
        # update direction from queue
        if self.move_q:
            self.snake.set_direction(self.move_q.pop(0))

        next_snake_head = self.snake.next_head_pos()
        # if snake will collide with wall / self: end game
        if self.will_collide(next_snake_head):
            self.end_game()
        
        # else if snake will collide with fruit
        elif next_snake_head == self.fruit.location:
            self.eat_fruit()
            self.score += 1
            self.generate_fruit() # this will also destroy old fruit, right?
            self.speed += 1

            self.snake.lengthen() # lengthen, rather than move

        # otherwise, snake moves
        else:
            self.snake.move()
        
    def game_play(self):

        while self.game_in_progress: # while game in progress
            self.handle_keypress()
            # define some wait time in terms of speed + speed_adjustment
            speed_increment = .005
            start_wait_time = .2
            min_wait_time = .035
            absolute_min_wait_time = .025
            wait_time = max((start_wait_time-(self.speed*speed_increment)),(min_wait_time)) # make some function that mins out at a certain time
            if self.speed_adjustment != 0:
                wait_time = max(wait_time/2 , absolute_min_wait_time)

            # call render_board function
            self.ui.write_text(str(self.score))
            self.render_board()

            self.game_turn()

            time.sleep(wait_time)

        countdown_to_end  = 10

        while countdown_to_end > 0:

            self.ui.write_text("GAME OVER ** SCORE: "+ str(self.score) + " ** ends: " + str(countdown_to_end), 0, 250)

            self.render_board()
            countdown_to_end -= 1
            time.sleep(1)

        

    def handle_keypress(self):
        last_keypresses = self.ui.get_relevant_keyevents()
        for keypress in last_keypresses:
            # print("Begin for loop")
            if keypress == Key_events.UP:
                input_direction = Direction.UP
            elif keypress == Key_events.DOWN:
                input_direction = Direction.DOWN
            elif keypress == Key_events.LEFT:
                input_direction = Direction.LEFT
            elif keypress == Key_events.RIGHT:
                input_direction = Direction.RIGHT
            elif keypress == Key_events.QUIT:
                self.end_game()
            # print("keypress = ", keypress, " input)_direction: ", input_direction)
            # print("move_q", self.move_q)
            if len(self.move_q) >= 3:
                continue
            else:
                self.move_q.append(input_direction)
            
            # print("current snake direction: ", self.snake.direction)
            
    

def run():
    new_game = Game(30,30,1)
    new_game.game_play()



if __name__=="__main__":
    run()
