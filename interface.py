import tkinter
import multiprocessing
import platform

from engine import Engine
from plot import Plot

CANVAS_SIZE = 600
POPULATION = 500


class Interface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.engine = Engine(CANVAS_SIZE, POPULATION)
        self.data_queue = multiprocessing.Queue()  # 进程间通信用到的队列
        self.plot = Plot(self.data_queue)  # 感染人数时间序列传给Plot
        self.env_variables = {
            'population': 500,
            'move_range': 100,
            'move_speed': 3,
            'large_factor': 0.05,  # 需要到处逛的人的比例
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
        self.data_queue.put({'type': 'data', 'data': self.stats.get('infectious', 0)})  # 感染人数时间序列新增数据, Plot进程能够收到新增的数据 
        self.root.after(30, self.next_frame)

    def start(self):
        self.engine.create(self.env_variables)
        self.engine.infect(10)
        self.root.after(30, self.next_frame)  # 30ms后运行这个函数
        self.plot.start()
        self.root.mainloop()
        
    def restart(self):
        for var in self.env_variables:
            type_val = type(self.env_variables[var])
            self.env_variables[var] = type_val(self.strvars[var].get())  # 获取新的输入后重启
        self.data_queue.put({'type': 'clear'})  # 传递清空信号
        self.engine.create(self.env_variables)
        self.engine.infect(10)


if __name__ == "__main__":
    if platform.system() == "Darwin":
        multiprocessing.set_start_method('spawn')
    interface = Interface()
    interface.start()
