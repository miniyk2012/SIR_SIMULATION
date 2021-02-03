import tkinter
from engine import Engine

CANVAS_SIZE = 600
POPULATION = 500


class Interface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.engine = Engine(CANVAS_SIZE, POPULATION)
        self.env_variables = {
            'population': 500,
            'move_range': 100,
            'move_speed': 3,
        }
        self.strvars = {}
        self.create_widgets()

    def create_widgets(self):
        for var, val in self.env_variables.items():
            frame = tkinter.Frame(self.root)
            strvar = tkinter.StringVar(frame)
            strvar.set(val)
            label = tkinter.Label(frame, text=var, width=20)
            entry = tkinter.Entry(frame, textvariable=strvar)  # 输入框
            label.pack(side=tkinter.LEFT)
            entry.pack(side=tkinter.LEFT)
            self.strvars[var] = strvar
            frame.pack()
        
        self.canvas = tkinter.Canvas(
            self.root, height=CANVAS_SIZE, width=CANVAS_SIZE, bg='white')
        self.canvas.pack()
        self.restart_button = tkinter.Button(self.root, text='restart', command=self.restart)
        self.restart_button.pack()

    def draw_people(self):
        color = {
            'susceptible': 'green',
            'infectious': 'red',
            'recovered': 'yellow',
        }
        for person in self.engine.people:
            x, y = person.x, person.y
            self.canvas.create_rectangle(
                x-2, y-2, x+2, y+2, fill=color[person.status], outline=color[person.status])
            
    def draw_stats(self):
        self.stats = {}
        for person in self.engine.people:
            self.stats[person.status] = self.stats.get(person.status, 0) + 1
        y_coord = 20
        for stat in self.stats:
            self.canvas.create_text(70, y_coord, text=f'{stat}: {self.stats[stat]}')
            y_coord += 20

    def next_frame(self):
        self.engine.next_frame()
        self.canvas.delete('all')  # 擦掉
        self.draw_people()
        self.draw_stats()
        self.root.after(30, self.next_frame)

    def start(self):
        self.engine.create(self.env_variables)
        self.engine.infect(10)
        self.root.after(30, self.next_frame)  # 30ms后运行这个函数
        self.root.mainloop()
        
    def restart(self):
        for var in self.env_variables:
            type_val = type(self.env_variables[var])
            self.env_variables[var] = type_val(self.strvars[var].get())
        self.engine.create(self.env_variables)
        self.engine.infect(10)


if __name__ == "__main__":
    interface = Interface()
    interface.start()
