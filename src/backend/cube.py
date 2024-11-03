import numpy as np

class Cube:
    def __init__(self, cube = None):
        self.magicNumber = 315
        if cube is None:
            self.cube = self.__generate_cube()
        else:
            self.cube = np.array(cube)
        self.value = self.__get_objective_value()

    def copy(self):
        return Cube(self.cube.copy())

    def __generate_cube(self):
        numbers = np.arange(1, 126)
        
        np.random.shuffle(numbers)
        
        cube = numbers.reshape((5, 5, 5))

        return cube
    
    def __get_objective_value(self):
        objectiveSum = (self.__rows_value() + self.__cols_value() + self.__pillars_value() + self.__diagonals_value() + self.__triagonals_value())
        return objectiveSum
    
    def __rows_value(self):
        rowsValue = np.sum(np.abs(self.magicNumber - np.sum(self.cube[:, :, :], axis = 2)))
        return rowsValue

    def __cols_value(self):
        colsValue = np.sum(np.abs(self.magicNumber - np.sum(self.cube[:, :, :], axis = 1)))
        return colsValue

    def __pillars_value(self):
        pillarsValue = np.sum(np.abs(self.magicNumber - np.sum(self.cube[:, :, :], axis = 0)))
        return pillarsValue

    def __diagonals_value(self):
        diagonalsValue = 0

        indices = np.arange(5)

        for i in indices:
            d1Sum = np.sum(self.cube[i, indices, indices])
            d2Sum = np.sum(self.cube[i, indices, 4 - indices])
            diagonalsValue += abs(self.magicNumber - d1Sum) + abs(self.magicNumber - d2Sum)

        for j in indices:
            d1Sum = np.sum(self.cube[indices, j, indices])
            d2Sum = np.sum(self.cube[indices, j, 4 - indices])
            diagonalsValue += abs(self.magicNumber - d1Sum) + abs(self.magicNumber - d2Sum)

        for k in indices:
            d1Sum = np.sum(self.cube[indices, indices, k])
            d2Sum = np.sum(self.cube[indices, 4 - indices, k])
            diagonalsValue += abs(self.magicNumber - d1Sum) + abs(self.magicNumber - d2Sum)

        return diagonalsValue
    
    def __triagonals_value(self):
        indices = np.arange(5)

        t1Sum = np.sum(self.cube[indices, indices, indices])
        t2Sum = np.sum(self.cube[indices, indices, 4 - indices])
        t3Sum = np.sum(self.cube[4 - indices, indices, indices])
        t4Sum = np.sum(self.cube[4 - indices, indices, 4 - indices])

        triagonalsValue = (abs(self.magicNumber - t1Sum) + abs(self.magicNumber - t2Sum) + abs(self.magicNumber - t3Sum) + abs(self.magicNumber - t4Sum))

        return triagonalsValue