import math


def are_parallel(v1, v2):
    """
        Determines whether two vectors are parallel
    """
    zero = Vector(0, 0, 0)
    cross = cross_product(v1, v2)
    return zero == cross


def are_orthogonal(v1, v2):
    """
        Determines whether two vectors are orthogonal
    """
    return dot_product(v1, v2) == 0


def cross_product(v1, v2):
    """
        Computes the outer product/cross product of two given vectors
    """
    return Vector(v1.y*v2.z - v1.z*v2.y, v1.z*v2.x - v1.x*v2.z, v1.x*v2.y - v1.y*v2.x)


def dot_product(v1, v2):
    """
        Computes the inner product/dot product of two given vectors
    """
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z


def magnitude(v):
    """
        Computes the euclidean norm of a given vector
    """
    return math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)


def normalize(v):
    """
        Generates the corresponding unit vector from the given vector
    """
    norm = Vector.magnitude(v)
    if norm != 0:
        return v / norm
    else:
        return Vector(0, 0, 0)


class Vector:
    """
        Represents a 3D math/geometry vector
    """

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return magnitude(self)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, multiple):
        return Vector(self.x*multiple, self.y*multiple, self.z*multiple)

    def __imul__(self, multiple):
        self.x *= multiple
        self.y *= multiple
        self.z *= multiple
        return self

    def __truediv__(self, divisor):
        return Vector(self.x / divisor, self.y / divisor, self.z / divisor)

    def __itruediv__(self, divisor):
        self.x /= divisor
        self.y /= divisor
        self.z /= divisor
        return self

    def __ifloordiv__(self, divisor):
        self.x //= divisor
        self.y //= divisor
        self.z //= divisor
        return self

    def __floordiv__(self, divisor):
        return Vector(self.x // divisor, self.y // divisor, self.z // divisor)

    def __idiv__(self, divisor):
        self.x /= divisor
        self.y /= divisor
        self.z /= divisor
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "Vector(x={0},y={1},z={2})".format(self.x, self.y, self.z)

    def copy(self):
        """
            Returns a deep copy of the current vector instance.
        """
        return Vector(self.x, self.y, self.z)
