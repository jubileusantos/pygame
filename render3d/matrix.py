from __future__ import annotations
from pygame.math import Vector2, Vector3

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def getIndex(self, x, y):
        return self.matrix[y][x]

    def getDimensions(self):
        return len(self.matrix), len(self.matrix[0])

    def getInverse(self):
        if self.getDimensions() == (2,2):
            determinant = 1 / (self.getIndex(0, 0) * self.getIndex(1,1) - self.getIndex(0, 1) * self.getIndex(1, 0))
            return Matrix([
                [self.getIndex(1,1), -self.getIndex(1, 0)],
                [-self.getIndex(0, 1), self.getIndex(0, 0)]
            ]) * determinant
        else:
            return NotImplementedError(f"Calculation for inverse matrices of dimensions {self.getDimensions()[0]}x{self.getDimensions()[1]} not implemented")

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.getDimensions() != other.getDimensions(): raise TypeError(f"Cannot add two Matrices of different dimensions: {self.getDimensions()[0]}x{self.getDimensions()[1]} and {other.getDimensions()[0]}x{other.getDimensions()[1]}") 

            newMatrix = []
            for idxY, y in enumerate(self.matrix):
                line = []

                for idxX, x in enumerate(y):
                    line.append(x + other.matrix[idxY][idxX])

                newMatrix.append(line)
        return Matrix(newMatrix)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            newMatrix = []

            # Loop each line of my matrix
            for myIdxY, myY in enumerate(self.matrix):
                line = []

                # Loop each column of the other matrix
                for otherX in range(other.getDimensions()[1]):
                    value = 0

                    # Loop each column of my matrix's current line
                    for myIdxX, myX in enumerate(myY):
                        value += myX * other.matrix[myIdxX][otherX]

                    line.append(value)

                newMatrix.append(line)

        elif type(other) in (int, float):
            newMatrix = []
            for idxY, y in enumerate(self.matrix):
                line = []

                for idxX, x in enumerate(y):
                    line.append(other * x)
                newMatrix.append(line)
        else:
            raise TypeError("Unsupported operation")

        return Matrix(newMatrix)

    def __repr__(self) -> str:
        string = ""
        for idxY, y in enumerate(self.matrix):
            linha = "["
            
            for idxX, x in enumerate(y):
                linha += "{}{}".format(x, " " if idxX+1 != len(y) else "")

            linha += "]{}".format("\n" if idxY+1 != len(self.matrix) else "")
            string += linha

        return string

    def __eq__(self, other) -> bool:
        if not (isinstance(other, Matrix) and self.getDimensions() == other.getDimensions()): return False

        for idxY, y in enumerate(self.matrix):
            for idxX, x in enumerate(y):
                if x != other.matrix[idxY][idxX]:
                    return False

        return True

    def toVector2(self) -> Vector2:
        return Vector2(self.matrix[0][0], self.matrix[1][0])

    def toVector3(self) -> Vector3:
        return Vector3(self.matrix[0][0], self.matrix[1][0], self.matrix[2][0])

    @staticmethod
    def fromVector2(v: Vector2) -> Matrix:
        if type(v) != Vector2:
            raise TypeError("Argument v needs to be a Vector2")

        return Matrix([
        [v.x],
        [v.y]
    ])

    def fromVector3(v: Vector3) -> Matrix:
        if type(v) != Vector3:
            raise TypeError("Argument v needs to be a Vector3")

        return Matrix([
        [v.x],
        [v.y],
        [v.z]
    ])

if __name__ == "__main__":
    projection = Matrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    point = Vector3(15, 0, 0)

    print(Matrix.fromVector2(point))