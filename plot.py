import multiprocessing
import platform
import time


class Plot(multiprocessing.Process):
    def __init__(self, data_queue):
        # daemon=False，主线程结束时会检测该子线程是否结束，如果该子线程还在运行，则主线程会等待它完成后再退出；
        # daemon=True, 主线程运行结束时不对这个子线程进行检查而直接退出，同时所有daemon值为True的子线程将随主线程一起结束
        super().__init__(daemon=True)
        self.data_queue = data_queue


    def update(self, frame):
        # 1~100
        while not self.data_queue.empty():
            elem = self.data_queue.get()
            if elem['type'] == 'data':
                self.data.append(elem['data'])
            elif elem['type'] == 'clear':
                self.data = []
        y = self.data
        x = list(range(1, len(self.data)+1))
        self.ax.relim()  # 调整坐标轴的范围
        self.ax.autoscale_view()
        self.line.set_data(x, y)
        return self.line,

    def animate_init(self):
        self.line.set_data([], [])
        return self.line,

    def run(self):
        # interface和plot在同一个进程中恰好共用同一个tkinter后端, 为了防止竞态条件的发生, 需要让它们不使用同一个后端, 因此不能在文件开头导入plt
        # 可以在run里再单独导入plt, 因为run是在新的进程里跑的, 导入的plt用的后端就和tkinter不是同一个了.
        import matplotlib.pyplot as plt
        from matplotlib import animation
        self.fig = plt.figure()
        self.ax = plt.axes()  # 坐标轴
        self.line, = self.ax.plot([1, 2, 3], [1, 2, 4])
        self.data = []
        _ = animation.FuncAnimation(self.fig,
                                    self.update,  # 每次更新数据
                                    frames=range(1, 100),  # 100帧, 每一帧会传update函数一个值
                                    init_func=self.animate_init,  # 动画开始时做什么
                                    interval=1000,  # 1000ms画一次
                                    blit=False)  # 优化用, 置为False
        plt.show()


if __name__ == "__main__":
    if platform.system() == "Darwin":
        multiprocessing.set_start_method('spawn')
    plot = Plot()
    plot.start()
    while True:
        time.sleep(10)