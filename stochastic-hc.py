import numpy as np
from numba import jit
import random

@jit(nopython=True)
def calculate_deviation_numba(value, magic_number):
    return abs(value - magic_number)

@jit(nopython=True)
def evaluate_cube(cube, n, magic_number):
    total_deviation = 0
    

    for i in range(n):
        for j in range(n):

            total_deviation += calculate_deviation_numba(np.sum(cube[i, j, :]), magic_number)
     
            total_deviation += calculate_deviation_numba(np.sum(cube[i, :, j]), magic_number)

            total_deviation += calculate_deviation_numba(np.sum(cube[:, i, j]), magic_number)
        
        # Diagonals
        total_deviation += calculate_deviation_numba(np.sum(cube[i, i, :]), magic_number)
        total_deviation += calculate_deviation_numba(np.sum(cube[n-1-i, i, :]), magic_number)
        total_deviation += calculate_deviation_numba(np.sum(cube[:, i, n-1]), magic_number)
        total_deviation += calculate_deviation_numba(np.sum(cube[:, i, i]), magic_number)
        total_deviation += calculate_deviation_numba(np.sum(cube[i, :, i]), magic_number)
        total_deviation += calculate_deviation_numba(np.sum(cube[n-1-i, :, i]), magic_number)
    
        # Diagonal Ruang
        main_diagonal_sum = 0
        anti_diagonal_sum_1 = 0
        anti_diagonal_sum_2 = 0
        anti_diagonal_sum_3 = 0
        for i in range(n):
            main_diagonal_sum += cube[i, i, i]                         
            anti_diagonal_sum_1 += cube[i, n - 1 - i, i]          
            anti_diagonal_sum_2 += cube[n - 1 - i, i, i]          
            anti_diagonal_sum_3 += cube[i, i, n - 1 - i]          

        total_deviation += calculate_deviation_numba(main_diagonal_sum, magic_number)
        total_deviation += calculate_deviation_numba(anti_diagonal_sum_1, magic_number)
        total_deviation += calculate_deviation_numba(anti_diagonal_sum_3, magic_number) 
        total_deviation += calculate_deviation_numba(anti_diagonal_sum_2, magic_number)
    return total_deviation

@jit(nopython=True)
def generate_neighbors_numba(flat_cube, n):
    size = len(flat_cube)
    num_neighbors = (size * (size - 1)) // 2
    neighbor_cubes = np.zeros((num_neighbors, size), dtype=flat_cube.dtype)
    
    idx = 0
    for i in range(size):
        for j in range(i + 1, size):
            neighbor_cubes[idx] = flat_cube.copy()
            neighbor_cubes[idx, i], neighbor_cubes[idx, j] = flat_cube[j], flat_cube[i]
            idx += 1
            
    return neighbor_cubes.reshape(-1, n, n, n)

class DiagonalMagicCube:
    def __init__(self, n=5):
        self.n = n
        self.size = n**3
        self.magic_number = self.calculate_magic_number()
        self.cube = self.initialize_cube()

    @classmethod
    def constructor(cls, cube):
        instance = cls()
        instance.cube = cube
        instance.n = cube.shape[0]
        instance.size = cube.size
        instance.magic_number = instance.calculate_magic_number()
        return instance

    def calculate_magic_number(self):
        return ((self.size + 1) * self.n) // 2
    
    def initialize_cube(self):
        numbers = np.arange(1, self.size + 1, dtype=np.int32)
        np.random.shuffle(numbers)
        return numbers.reshape((self.n, self.n, self.n))
    
    def evaluate(self):
        return evaluate_cube(self.cube, self.n, self.magic_number)
    
    def get_neighbors(self):
        flat_cube = self.cube.flatten()
        neighbor_cubes = generate_neighbors_numba(flat_cube, self.n)
        return [DiagonalMagicCube.constructor(cube) for cube in neighbor_cubes]
    def swap(self, pos1, pos2):
        x = self.cube[pos1] 
        y = self.cube[pos2]
        self.cube[pos1], self.cube[pos2] =y,x
    
    def get_random_position(self):
        return tuple(random.randint(0, self.n-1) for _ in range(3))

class StochasticHillClimbing:
    def __init__(self, cube, max_iterations=100):
        self.cube = cube
        self.max_iterations = max_iterations
        self.max_sideways = 100
    
    def run(self):
        current_score = self.cube.evaluate()
        print(self.cube.cube)
        iteration = 0
        
        for k in range(1000000):
        # while(True):
            if current_score == 0:  
                break
            
            best_score = current_score
            pos1 = self.cube.get_random_position()
            pos2 = self.cube.get_random_position()
            self.cube.swap(pos1, pos2)
            new_score = self.cube.evaluate()
            if new_score < best_score:
                best_score = new_score
            else:
                self.cube.swap(pos1, pos2)
            current_score = best_score
            iteration+=1
        return iteration, self.cube, current_score

def main():
    cube = DiagonalMagicCube()
    initial_score = cube.evaluate()
    print(f"Initial score: {initial_score}")
    print("Initial cube configuration:")
    # print(cube.cube)
   
    hill_climbing = StochasticHillClimbing(cube)

    iterations, final_cube, final_score = hill_climbing.run()
    print(f"Final score: {final_score}")
    print(f"Number of iterations: {iterations}")
    print(f"Final cube configuration:\n{final_cube.cube}")
    if final_score == 0:
        print("Perfect solution found!")
    else:
        print("Local optimum reached.")
    
    # print("Final cube configuration:")
    # print(cube.cube)

if __name__ == "__main__":
    main()