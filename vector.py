class Vector:
    """为了让向量的加减法更简单"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def length(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    def copy(self):
        return Vector(self.x, self.y)

    def __add__(self, other):
        # v3 = v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def uniform(self, length):
        """单位向量 * length"""
        return Vector(self.x / self.length * length, self.y / self.length * length) 
