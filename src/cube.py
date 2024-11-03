import random

class Cube:
    def __init__(self, cube = None):
        self.magicNumber = 315
        if cube == None:
            self.cube = cube
        else:
            self.cube = self.__generate_cube()
        self.value = self.__get_objective_value()
        

    def __generate_cube(self):
        numbers = list(range(1,126))

        medianValue = 63
        numbers.remove(medianValue)
        
        random.shuffle(numbers)

        cube = [[[0 for _ in range(5)] for _ in range(5)] for _ in range(5)]

        for i in range(5):
            for j in range(5):
                for k in range(5):
                    if i == 2 and j == 2 and k == 2:
                        cube[i][j][k] = medianValue
                    else:
                        cube[i][j][k] = numbers.pop(0)

        return cube
    
    def __get_objective_value(self):
        objectiveSum = self.__rows_value() + self.__cols_value() + self.__pillars_value() + self.__diagonals_value() + self.__triagonals_value()
        return objectiveSum
    
    def __rows_value(self):
        rowsValue = 0

        for i in range(5):
            for j in range(5):
                rowSum = sum(self.cube[i][j][k] for k in range(5))
                rowsValue += abs(self.magicNumber - rowSum)

        return rowsValue

    def __cols_value(self):
        colsValue = 0

        for i in range(5):
            for k in range(5):
                colSum = sum(self.cube[i][j][k] for j in range(5))
                colsValue += abs(self.magicNumber - colSum)

        return colsValue

    def __pillars_value(self):
        pillarsValue = 0

        for j in range(5):
            for k in range(5):
                pillarSum = sum(self.cube[i][j][k] for i in range(5))
                pillarsValue += abs(self.magicNumber - pillarSum)

        return pillarsValue

    def __diagonals_value(self):
        diagonalsValue = 0

        for i in range(5):
            d1Sum = sum(self.cube[i][c][c] for c in range(5))
            d2Sum = sum(self.cube[i][c][4 - c] for c in range(5))
            diagonalsValue += abs(self.magicNumber - d1Sum) + abs(self.magicNumber - d2Sum)

        for j in range(5):
            d1Sum = sum(self.cube[c][j][c] for c in range(5))
            d2Sum = sum(self.cube[c][j][4 - c] for c in range(5))
            diagonalsValue += abs(self.magicNumber - d1Sum) + abs(self.magicNumber - d2Sum)

        for k in range(5):
            d1Sum = sum(self.cube[c][c][k] for c in range(5))
            d2Sum = sum(self.cube[c][4 - c][k] for c in range(5))
            diagonalsValue += abs(self.magicNumber - d1Sum) + abs(self.magicNumber - d2Sum)

        return diagonalsValue
    
    def __triagonals_value(self):
        triagonalsValue = 0

        t1Sum = sum(self.cube[i][i][i] for i in range(5))
        triagonalsValue += abs(self.magicNumber - t1Sum)

        t2Sum = sum(self.cube[i][i][4 - i] for i in range(5))
        triagonalsValue += abs(self.magicNumber - t2Sum)

        t3Sum = sum(self.cube[4 - i][i][i] for i in range(5))
        triagonalsValue += abs(self.magicNumber - t3Sum)

        t4Sum = sum(self.cube[4 - i][i][4 - i] for i in range(5))
        triagonalsValue += abs(self.magicNumber - t4Sum)

        return triagonalsValue