import random
from vector import Vector

MOVE_RANGE = 10
MOVE_SPEED = 3
UNSAFE_DISTANCE = 5
INFECTIOUS_RATE = 0.3
INFECTIOUS_DURATION = 300  # 感染者300帧后恢复


class Person:

    def __init__(self, engine):
        """人所在的位置, 需要指导图的大小, 把engine直接传进来"""
        self.position = Vector(random.randrange(
            0, engine.size), random.randrange(0, engine.size))
        self.home = self.position.copy()
        self.move_target = self.home.copy()
        self.move_range = engine.move_range
        self.move_speed = engine.move_speed
        self.status = 'susceptible'  # 易感染的
        self.infectious_dur_left = 0

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def get_new_target(self):
        """新的move_target永远在home附近"""
        self.move_target = self.home + \
            Vector(random.uniform(-self.move_range, self.move_range),
                   random.uniform(-self.move_range, self.move_range)
                   )
        # 方向不变, 大小为move_speed
        self.step = (self.move_target - self.position).uniform(self.move_speed)

    def move(self):
        """如果走到了目标地点, 就换一个目标地点, step也同时完成"""
        if self.position == self.move_target:
            self.get_new_target()
        if (self.move_target - self.position).length < self.move_speed:
            self.position = self.move_target
        else:
            self.position = self.position + self.step

    def too_close(self, other):
        return (self.position - other.position).length < UNSAFE_DISTANCE

    def try_infect(self, other):
        if random.uniform(0, 1) < INFECTIOUS_RATE:
            other.status = 'infectious'
            other.infectious_dur_left = INFECTIOUS_DURATION


class Engine:

    def __init__(self, size, population):
        """引擎要把图放进来, 指导人口数量"""
        self.size = size
        self.population = population
        self.people = []

    def create(self, env_variables):
        for var, val in env_variables.items():
            setattr(self, var, val)
        self.people = [Person(self) for _ in range(self.population)]
        
        large_factor_people = random.sample(self.people, int(self.large_factor * self.population))
        for person in large_factor_people:
            person.move_range *= 10

    def next_frame(self):
        for person in self.people:
            person.move()
            if person.status == 'infectious':
                for target in self.people:
                    if target.status == 'susceptible' and target.too_close(person):
                        person.try_infect(target)
                person.infectious_dur_left -= 1
                if person.infectious_dur_left == 0:
                    person.status = 'recovered'

    def infect(self, number):
        initial_infected = random.sample(self.people, number)
        for person in initial_infected:
            person.status = 'infectious'
            person.infectious_dur_left = random.randrange(
                1, INFECTIOUS_DURATION + 1)
