__author__ = 'victoriabetts'

import pyglet
import random

tiles_image = pyglet.image.load("minesweeper_tiles.jpg")

tile_size = 24
num_cols = 10
num_rows = 10
mine_ratio = (10.0 / 64.0) * (num_rows * num_cols)
num_mines = int(mine_ratio + 0.5)
neighbour_offsets = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
    (0, -1),
    (1, -1)
]


def get_icon(col, row):
    # returns the icon located in the specified cell
    x = (col - 1) * tile_size
    y = (row - 1) * tile_size
    return tiles_image.get_region(x, y, tile_size, tile_size)


mine_icon = get_icon(3, 3)
hidden_icon = get_icon(1, 3)
flag_icon = get_icon(2, 3)
numbered_icons = [
    get_icon(4, 3),
    get_icon(1, 2),
    get_icon(2, 2),
    get_icon(3, 2),
    get_icon(4, 2),
    get_icon(1, 1),
    get_icon(2, 1),
    get_icon(3, 1),
    get_icon(4, 1)
]


class Cell():
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.has_mine = False
        self.has_flag = False
        self.is_exposed = False
        self.num_surrounding_mines = 0
        self.gen_sprite()


    def description(self):
        return "I am cell(" + str(self.col) + ", " + str(self.row) + ")"

    def gen_sprite(self):
        """

        :rtype : object
        """
        if self.is_exposed is False and self.has_flag is True:
            icon = flag_icon
        elif self.is_exposed is True and self.has_mine is True:
            icon = mine_icon
        elif self.is_exposed is True and self.has_mine is False:
            icon = numbered_icons[self.num_surrounding_mines]
        else:
            icon = hidden_icon

        self.sprite = pyglet.sprite.Sprite(icon, self.col * tile_size, self.row * tile_size)


board = [[Cell(col, row) for row in xrange(num_rows)] for col in xrange(num_cols)]

window = pyglet.window.Window(width=num_cols * tile_size, height=num_rows * tile_size)

gameover = False

label = pyglet.text.Label('',
                          font_name='Sans Serif',
                          font_size=18,
                          x=window.width//2, y=window.height//2,
                          color=(0,0,0,255),
                          anchor_x='center', anchor_y='center')

def initialize_board():
    num_mines_created = 0
    num_surrounding_mines = 0

    while num_mines_created < num_mines:
        mine_row = random.randint(0, (num_rows - 1))
        mine_col = random.randint(0, (num_cols - 1))
        mine_cell = board[mine_col][mine_row]
        if mine_cell.has_mine == False:
            mine_cell.has_mine = True

            mine_cell.gen_sprite()

            for col_offset, row_offset in neighbour_offsets:
                neighbour_col = mine_col + col_offset
                neighbour_row = mine_row + row_offset
                if neighbour_col >= 0 and neighbour_col < num_cols and neighbour_row >= 0 and neighbour_row < num_rows:
                    neighbour_cell = board[neighbour_col][neighbour_row]
                    neighbour_cell.num_surrounding_mines += 1

                    neighbour_cell.gen_sprite()

            mine_cell.gen_sprite()
            num_mines_created += 1


initialize_board()


def expose(exposed_col, exposed_row):
    exposed_cell = board[exposed_col][exposed_row]
    if exposed_cell.is_exposed == False:
        exposed_cell.is_exposed = True
        exposed_cell.gen_sprite()
        if exposed_cell.num_surrounding_mines == 0 and exposed_cell.has_mine == False:
            for col_offset, row_offset in neighbour_offsets:
                neighbour_col = exposed_col + col_offset
                neighbour_row = exposed_row + row_offset
                if 0 <= neighbour_col < num_cols and neighbour_row >= 0 and neighbour_row < num_rows:
                    expose(neighbour_col, neighbour_row)

def check_end_conditions():
    global gameover
    num_exposed = 0
    mine_hit = False
    for col in xrange(num_cols):
        for row in xrange(num_rows):
            cell = board[col][row]
            if cell.is_exposed == True and cell.has_mine == True:
                mine_hit = True
            elif cell.is_exposed == True:
                num_exposed +=1
    if mine_hit == True:
        label.text = "Game Over :("
        gameover = True
    elif num_exposed == ((num_cols * num_rows) - num_mines):
        label.text = "You Win!"
        gameover = True

@window.event
def on_draw():
    window.clear()
    for col in xrange(num_cols):
        for row in xrange(num_rows):
            board[col][row].sprite.draw()
    label.draw()


@window.event
def on_mouse_release(mouse_x, mouse_y, button, modifiers):
    if gameover == True:
        return
    row = mouse_y / tile_size
    col = mouse_x / tile_size
    cell = board[col][row]

    if modifiers > 0:
        if cell.has_flag == True:
            cell.has_flag = False
        elif cell.has_flag == False:
            cell.has_flag = True
    else:
        expose(col, row)

    cell.gen_sprite()
    check_end_conditions()


pyglet.app.run()
