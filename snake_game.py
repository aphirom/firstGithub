import tkinter as tk
import random

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
UPDATE_MS = 100

class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.direction = 'Right'
        self.snake = [(SEG_SIZE*5, SEG_SIZE*5), (SEG_SIZE*4, SEG_SIZE*5), (SEG_SIZE*3, SEG_SIZE*5)]
        self.food = self.place_food()
        self.game_over = False
        self.score = 0
        self.score_var = tk.StringVar(value=f"Score: {self.score}")
        self.score_label = tk.Label(master, textvariable=self.score_var, fg="green", bg="black")
        self.score_label.pack()

        # ปุ่มเริ่มใหม่และออก
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        restart_btn = tk.Button(btn_frame, text="เริ่มใหม่", command=self.restart_game, width=10, bg="#e0e0ff")
        restart_btn.pack(side=tk.LEFT, padx=5)
        exit_btn = tk.Button(btn_frame, text="ออก", command=master.quit, width=10, bg="#ffe0e0")
        exit_btn.pack(side=tk.LEFT, padx=5)

        master.bind('<Up>', lambda e: self.set_dir('Up'))
        master.bind('<Down>', lambda e: self.set_dir('Down'))
        master.bind('<Left>', lambda e: self.set_dir('Left'))
        master.bind('<Right>', lambda e: self.set_dir('Right'))
        self.draw()
        self.update()
    def restart_game(self):
        self.direction = 'Right'
        self.snake = [(SEG_SIZE*5, SEG_SIZE*5), (SEG_SIZE*4, SEG_SIZE*5), (SEG_SIZE*3, SEG_SIZE*5)]
        self.food = self.place_food()
        self.game_over = False
        self.score = 0
        self.score_var.set(f"Score: {self.score}")
        self.draw()
        self.update()

    def set_dir(self, d):
        # ป้องกันงูย้อนกลับ
        opposites = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}
        if d != opposites.get(self.direction):
            self.direction = d

    def place_food(self):
        while True:
            x = random.randint(0, (WIDTH-SEG_SIZE)//SEG_SIZE)*SEG_SIZE
            y = random.randint(0, (HEIGHT-SEG_SIZE)//SEG_SIZE)*SEG_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def draw(self):
        self.canvas.delete('all')
        # วาดงู
        for i, (x, y) in enumerate(self.snake):
            color = 'lime' if i == 0 else 'green'
            self.canvas.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill=color)
        # วาดอาหาร
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx+SEG_SIZE, fy+SEG_SIZE, fill='red')
        if self.game_over:
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill="white", font=("Arial", 24))

    def update(self):
        if self.game_over:
            return
        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y-SEG_SIZE)
        elif self.direction == 'Down':
            new_head = (head_x, head_y+SEG_SIZE)
        elif self.direction == 'Left':
            new_head = (head_x-SEG_SIZE, head_y)
        else:
            new_head = (head_x+SEG_SIZE, head_y)
        # ตรวจสอบชนขอบหรือชนตัวเอง
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake):
            self.game_over = True
            self.draw()
            return
        self.snake = [new_head] + self.snake[:-1]
        # กินอาหาร
        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.place_food()
            self.score += 1
            self.score_var.set(f"Score: {self.score}")
        self.draw()
        self.master.after(UPDATE_MS, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
