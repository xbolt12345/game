from tkinter import *
import random

#Game Backbone


BACKGROUND_COLOR = '#0A0A0A'

window = Tk()
window.title('Snake Game')
window.resizable(True, True)

canvas = None


def start():
    global canvas

    canvas = Canvas(window,
                    bg=BACKGROUND_COLOR,
                    width=grid_size[0] * sq_size, height=grid_size[1] * sq_size)
    canvas.pack()

    game_loop()

    window.mainloop()

def update():
    snakestep()

def check_coll():
    snake_coll()
    food_coll()

def elem():
    canvas.delete("all")
    grid()
    drsnake()
    drfood()

is_game_running = True
game_speed = 5 

def game_over():
    canvas.delete("all")

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    canvas.create_text(
        canvas_width/2.0,
        canvas_height/2.0,
        text="Game Over",
        font=("consolas", 80),
        fill="#F12A00")

def game_loop():
    update()
    check_coll()
    elem()

    if is_game_running:
        update_time = int(1000 / game_speed)
        window.after(update_time, game_loop)
    else:
        game_over()

#Grid

grid_col = '#222222'
grid_size = (10,10)
sq_size = 40

def grid():
    global canvas

    canvas_width = grid_size[0] * sq_size
    canvas_height = grid_size[1] * sq_size

    for ix in range(grid_size[0]):
        xpos = ix * sq_size
        canvas.create_line(xpos, 0, xpos, canvas_height, width=1, fill=grid_col)

    for iy in range(grid_size[1]):
        ypos = iy * sq_size
        canvas.create_line(0, ypos, canvas_width, ypos, width=1, fill=grid_col)

    

#Snake

snake_col = "green"
snake_cord = [(0,0),(0,0),(0,0)]
curr_dir = "down"
next_dir = "down"

def snakestep():
    global snake_cord, curr_dir

    head = snake_cord[0]
    snake_cord=snake_cord[:-1]

    newhead = None
    if next_dir == "down":
        newhead = (head[0],head[1]+1)
    elif next_dir == "up":
        newhead = (head[0], head[1]-1)
    elif next_dir == "left":
        newhead = (head[0]-1, head[1])
    elif next_dir == "right":
        newhead = (head[0]+1, head[1])

    snake_cord.insert(0, newhead)
    curr_dir=next_dir


def drsnake():
    global canvas
    for x, y in snake_cord:
        x1 = x * sq_size
        y1 = y * sq_size

        x2 = (x+1) * sq_size
        y2 = (y+1) * sq_size

        canvas.create_rectangle(x1,y1,x2,y2, fill = snake_col)


def snake_coll():
    global is_game_running
    head = snake_cord[0]
    headx = head[0]
    heady = head[1]
    
    gridx = grid_size[0]
    gridy = grid_size[1]

    if headx < 0 or headx >= gridx or heady < 0 or heady >= gridy:
        is_game_running = False

    if head in snake_cord[1:]:
        is_game_running = False


def change_dir(new_dir):
    global next_dir
    next_dir = new_dir

    if (new_dir == "up" and curr_dir == "down") or (new_dir == "down" and curr_dir == "up") or \
            (new_dir == "left" and curr_dir == "right") or (new_dir == "right" and curr_dir == "left"):
        return

window.bind("<Left>", lambda event: change_dir("left"))
window.bind("<Right>", lambda event: change_dir("right"))
window.bind("<Up>", lambda event: change_dir("up"))
window.bind("<Down>", lambda event: change_dir("down"))

#********************************************************
#*******************************************#Food
#********************************************************
FOOD_COLOR = '#F12A00'
food_pos=(0,0)
def move_food():
    global food_pos

    newx=random.randint(0,grid_size[0]-1)
    newy=random.randint(0,grid_size[1]-1)

    food_pos=(newx,newy)
    if food_pos in snake_cord:
        move_food()
move_food()

def food_coll():
    head=snake_cord[0]

    if head==food_pos:
        move_food()
        increase_score()

        snake_cord.append(snake_cord[-1])
def drfood():
    x1=food_pos[0]* sq_size
    y1=food_pos[1]* sq_size
    x2=(food_pos[0]+1)* sq_size
    y2=(food_pos[1]+1)* sq_size

    canvas.create_rectangle(x1,y1,x2,y2, fill=FOOD_COLOR)

#*****************************************************
#*********************************#Score
#****************************************************
    
score=0
label_score = Label(window, text="Score: {}".format(score), font=('sans-serif', 20))
label_score.pack()

def increase_score():
    global score, game_speed
    score=score+1

    label_score.config(text="Score: {}".format(score))
    game_speed=game_speed+0.25

#********************************************************
#********************************************************
#********************************************************
    
if __name__ == '__main__':
    start()