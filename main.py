## 10/13/18 - 10/27/18 IEEE zhiqin_lei_project
## 2D-World
from tkinter import *
import random

WORLD_WIDTH = 800
WORLD_HEIGHT = 600


# dirt = 1, water = 2, grass = 3, wood = 4, plank = 5
class Display:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WORLD_WIDTH, height=WORLD_HEIGHT + 100)
        self.canvas.pack()
        self.world = World()
        self.root.bind("<KeyPress>", self.key_press)
        self.dirt = PhotoImage(file="images/dirt.gif")
        self.water = PhotoImage(file="images/water.gif")
        self.grass = PhotoImage(file="images/grass.gif")
        self.wood = PhotoImage(file="images/wood.gif")
        self.plank = PhotoImage(file="images/plank.gif")
        self.player_image = PhotoImage(file="images/player.gif")

    def start(self):
        self.world.start()
        self.refresh()
        self.root.mainloop()

    def draw_game(self):
        self.canvas.create_rectangle(0, 0, WORLD_WIDTH, WORLD_HEIGHT)
        for i_idx, i in enumerate(self.world.object):
            for j_idx, j in enumerate(i):
                if j == 1:
                    self.canvas.create_image(j_idx * 25, i_idx * 25, image=self.dirt, anchor="nw")
                elif j == 2:
                    self.canvas.create_image(j_idx * 25, i_idx * 25, image=self.water, anchor="nw")
                elif j == 3:
                    self.canvas.create_image(j_idx * 25, i_idx * 25, image=self.grass, anchor="nw")
                elif j == 4:
                    self.canvas.create_image(j_idx * 25, i_idx * 25, image=self.wood, anchor="nw")
                elif j == 5:
                    self.canvas.create_image(j_idx * 25, i_idx * 25, image=self.plank, anchor="nw")
        self.canvas.create_image(self.world.player.x * 25, self.world.player.y * 25, image=self.player_image, anchor="nw")
        self.canvas.create_text(WORLD_WIDTH / 2, WORLD_HEIGHT + 50, text=self.world.player.get_inventory())

    def key_press(self, event):
        if event.keysym == "w":
            self.world.player.change_direction("Up")
        elif event.keysym == "s":
            self.world.player.change_direction("Down")
        elif event.keysym == "a":
            self.world.player.change_direction("Left")
        elif event.keysym == "d":
            self.world.player.change_direction("Right")
        elif event.keysym == "space":
            self.world.pick()
        elif event.keysym == "1":
            self.world.place(1)
        elif event.keysym == "2":
            self.world.place(2)
        elif event.keysym == "3":
            self.world.place(3)
        elif event.keysym == "4":
            self.world.place(4)
        elif event.keysym == "5":
            self.world.place(5)
        elif event.keysym == "t":
            self.world.player.craft(5)
        else:
            print("Invalid Input")

    def refresh(self):
        self.world.refresh()
        self.canvas.delete('all')
        self.draw_game()
        self.root.after(10, self.refresh)


class World:
    def __init__(self):
        self.width = int(WORLD_WIDTH / 25)
        self.height = int(WORLD_HEIGHT / 25)
        self.object = []
        self.player = Player()

    def start(self):
        for i in range(self.height):
            temp = []
            for i in range(self.width):
                temp.append(1)
            self.object.append(temp)
        for i in range(random.randint(250, 350)):
            self.object[random.randint(0, 23)][random.randint(0, 31)] = 3
        for i in range(random.randint(50, 100)):
            self.object[random.randint(0, 23)][random.randint(0, 31)] = 2
        for i in range(random.randint(20, 30)):
            self.object[random.randint(0, 23)][random.randint(0, 31)] = 4

    def pick(self):
        self.player.pick(self.object[self.player.y][self.player.x])
        self.object[self.player.y][self.player.x] = 1

    def place(self, num):
        if self.player.place(num):
            self.object[self.player.y][self.player.x] = num

    def refresh(self):
        pass


class Player:
    def __init__(self):
        self.width = int(WORLD_WIDTH / 25)
        self.height = int(WORLD_HEIGHT / 25)
        self.x = random.randint(0, 31)
        self.y = random.randint(0, 23)
        # [dirt, water, grass, wood, plank]
        self.inventory = [0, 0, 0, 0, 0]

    def change_direction(self, direction):
        if direction == "Up" and self.y > 0:
            self.y = self.y - 1
        elif direction == "Down" and self.y < self.height - 1:
            self.y = self.y + 1
        elif direction == "Left" and self.x > 0:
            self.x = self.x - 1
        elif direction == "Right" and self.x < self.width - 1:
            self.x = self.x + 1

    def pick(self, num):
        self.inventory[num - 1] += 1

    def place(self, num):
        if self.inventory[num - 1] > 0:
            self.inventory[num - 1] -= 1
            return True
        return False

    def get_inventory(self):
        return "Dirt: " + str(self.inventory[0]) + ", Water: " + str(self.inventory[1]) + ", Grass: " \
               + str(self.inventory[2]) + ", Wood: " + str(self.inventory[3]) + ", Plank: " + str(self.inventory[4])

    def craft(self, num):
        if num == 5 and self.inventory[3] >= 1:
            self.inventory[3] -= 1
            self.inventory[4] += 4


if __name__ == "__main__":
    d = Display()
    d.start()
