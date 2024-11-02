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

class SidewaysHillClimbing:
    def __init__(self, cube, max_iterations=100):
        self.cube = cube
        self.max_iterations = max_iterations
        self.max_sideways = 100
    
    def run(self):
        current_score = self.cube.evaluate()
        iteration = 0
        
        while True:
            if current_score == 0:
                break
            
            best_neighbor = None
            best_score = current_score

            neighbors = self.cube.get_neighbors()
            
            for neighbor in neighbors:
                new_score = neighbor.evaluate()
                if new_score < best_score:
                    best_neighbor = neighbor
                    best_score = new_score
                elif new_score == best_score:
                    best_neighbor = neighbor
                    best_score = new_score
                    self.max_sideways -= 1
            
            if best_neighbor is None or best_score >= current_score or self.max_sideways <= 0:
                break
                
            self.cube = best_neighbor
            current_score = best_score
            iteration += 1
            
        return iteration, self.cube, current_score

def main():

    np.random.seed(42)
    
    cube = DiagonalMagicCube()
    initial_score = cube.evaluate()
    print(f"Initial score: {initial_score}")
    
    hill_climbing = SidewaysHillClimbing(cube)
    iterations, final_cube, final_score = hill_climbing.run()
    
    print(f"Final score: {final_score}")
    print(f"Number of iterations: {iterations}")
    print(f"Final cube configuration:\n{final_cube.cube}")
    if final_score == 0:
        print("Perfect solution found!")
    else:
        print("Local optimum reached.")

if __name__ == "__main__":
    main()