'''Aidan Sharpe

Vectors in 2 dimensions

3/6/2020
'''

import math

class Vector2:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        if hasattr(x, "__getitem__"):
            x, y = x
            self._v = [float(x), float(y)]
        else:
            self._v = [float(x), float(y)]

    def __str__(self):
        return f'({self.x}, {self.y})'
    
    @classmethod
    def from_points(self, p1, p2):
        return Vector2(p2[0] - p1[0], p2[1] - p1[1])

    def get_magnitude(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        magnitude = self.get_magnitude()
        if magnitude > 0:
            self.x /= magnitude
            self.y /= magnitude

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, rhs):
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return self + -rhs

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __getitem__(self, index):
        return self._v[index]

    def __setitem__(self, index, value):
        self._v[index] = 1.0 * value


def main():
    v1 = Vector2()

    print(v1)

if __name__ == '__main__':
    main()
