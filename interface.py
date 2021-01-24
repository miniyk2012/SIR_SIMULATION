import tkinter
from engine import Engine

CANVAS_SIZE = 800
POPULATION = 500

class Interface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.root, height=CANVAS_SIZE, width=CANVAS_SIZE, bg='white')
        self.canvas.pack()
        self.engine = Engine(CANVAS_SIZE, POPULATION)
        
    def draw_people(self):
        color = {
            'susceptible': 'green',
            'infectious': 'red',
            'recovered': 'yellow',
        }
        for person in self.engine.people:
            x, y = person.x, person.y
            self.canvas.create_rectangle(x-2, y-2, x+2, y+2, fill=color[person.status], outline=color[person.status])

    def next_frame(self):
        self.engine.next_frame()
        self.canvas.delete('all')  # 擦掉
        self.draw_people()
        self.root.after(30, self.next_frame)

    def start(self):
        self.engine.create()
        self.engine.infect(10)
        self.root.after(30, self.next_frame)  # 30ms后运行这个函数
        self.root.mainloop()


if __name__ == "__main__":
    interface = Interface()
    interface.start()
