import random
from cube import Cube

class HillClimbing:
    def __init__(self, initialState : Cube):
        self.state = initialState
        self.iteration = 0
        self.objectiveValues = []

    # Find best neighbor for steepest (Not stochastic)
    def find_best_neighbor(self):
        bestValue = float('inf')
        bestNeighbor : Cube = None

        for a in range(125):
            i = a % 5
            j = a // 5 % 5
            k = a // 25
            
            b = a + 1
            
            while b != 125:
                successor = self.state.cube.copy()

                di = b % 5
                dj = b // 5 % 5
                dk = b // 25

                successor[i,j,k], successor[di,dj,dk] = successor[di,dj,dk], successor[i,j,k]

                newState = Cube(successor)

                if newState.value < bestValue:
                    bestNeighbor = newState
                    bestValue = newState.value
                elif newState.value == bestValue and random.randint(0,1):
                    bestNeighbor = newState

                b += 1
        
        return bestNeighbor
    
    def find_random_neighbor(self):
        neighbor = self.state.cube.copy()
        x1, y1, z1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        x2, y2, z2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        neighbor[x1, y1, z1], neighbor[x2, y2, z2] = neighbor[x2, y2, z2], neighbor[x1, y1, z1]

        return neighbor

    def search(self):
        raise NotImplementedError("Subclasses should implement this method")
    
class SteepestAscent(HillClimbing):
    def __init__(self, initial_state : Cube):
        super().__init__(initial_state)

    def search(self):
        success = True
        self.objectiveValues.append(self.state.value)

        while success:
            self.iteration += 1
            neighbor : Cube = self.find_best_neighbor()

            if self.state.value > neighbor.value:
                self.state = neighbor
            else:
                success = False

            self.objectiveValues.append(self.state.value)

class SidewaysMovement(HillClimbing):
    def __init__(self, initial_state : Cube, maxSidewaysMoves = 4):
        super().__init__(initial_state)
        self.maxSidewaysMove = maxSidewaysMoves

    def search(self):
        success = True
        sidewaysMoves = 0
        self.objectiveValues.append(self.state.value)

        while success and sidewaysMoves < self.maxSidewaysMove:
            self.iteration += 1
            neighbor : Cube = self.find_best_neighbor()

            if self.state.value >= neighbor.value:
                if self.state.value == neighbor.value:
                    sidewaysMoves += 1
                else:
                    sidewaysMoves = 0
                self.state = neighbor
            else:
                success = False

            self.objectiveValues.append(self.state.value)

class StochasticHC(HillClimbing):
    def __init__(self, initialState: Cube, nmax = 50):
        super().__init__(initialState)
        self.nmax = nmax

    # Asumsi nmax adalah toleransi ketidaksesuaian nilai neighbor baru dari state tertentu
    def search(self):
        tolerance = self.nmax
        self.objectiveValues.append(self.state.value)

        while tolerance and self.state.value != 0:
            self.iteration += 1
            neighbor : Cube = self.find_random_neighbor()
            if self.state.value > neighbor.value:
                self.state = neighbor
                tolerance = self.nmax
            else:
                tolerance -= 1
            
            self.objectiveValues.append(self.state.value)
            

class RandomRestart(HillClimbing):
    def __init__(self, initialState: Cube, maxRestart = 8):
        super().__init__(initialState)
        self.maxRestart = maxRestart
        self.iterationsPerRestart = []

    def search(self):
        bestOverall : Cube = None
        bestOverallValue = float('inf')
        self.objectiveValues.append(self.state.value)

        nmax = 50

        for i in range(self.maxRestart):
            if i > 0:
                self.state = Cube()

            currentIterations = 0

            success = True
            
            while success  and currentIterations < nmax:
                currentIterations += 1
                neighbor : Cube = self.find_best_neighbor()

                if self.state.value > neighbor.value:
                    self.state = neighbor
                else:
                    success = False

                self.objectiveValues.append(self.state.value)
            
            self.iterationsPerRestart.append(currentIterations)

            if bestOverallValue > self.state.value:
                bestOverall = self.state
                bestOverallValue = self.state.value

        self.state = bestOverall
        self.iteration = sum(self.iterationsPerRestart)