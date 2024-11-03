import random
import numpy as np
import time
from numba import jit

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

# class DiagonalMagicCube:
#     def __init__(self, n=5):
#         self.n = n
#         self.size = n**3
#         self.magic_number = self.calculate_magic_number()
#         self.cube = self.initialize_cube()
    
#     @classmethod 
#     def constructor(cls, cube):
#         instance = cls()
#         instance.cube = cube
#         return instance
    
#     def calculate_magic_number(self):
#         return ((self.size + 1) * self.n) // 2
    
#     def initialize_cube(self):
#         numbers = list(range(1, self.size + 1))
#         random.shuffle(numbers)
#         return np.array(numbers).reshape((self.n, self.n, self.n))
    
#     def evaluate(self):
#         total_deviation = 0

#         def calculate_deviation(sum_value):
#             return abs(sum_value - self.magic_number)

#         # Check
#         for i in range(self.n):
#             for j in range(self.n):
#                 total_deviation += calculate_deviation(np.sum(self.cube[i, j, :]))  # Row
#                 total_deviation += calculate_deviation(np.sum(self.cube[i, :, j]))  # Column
#                 total_deviation += calculate_deviation(np.sum(self.cube[:, i, j]))  # Pillar

#             total_deviation += calculate_deviation(np.sum(self.cube[i, i, :]))  # Diagonal
#             total_deviation += calculate_deviation(np.sum(self.cube[4-i, i, :]))  # Diagonal

#             total_deviation += calculate_deviation(np.sum(self.cube[:, i, 4-1]))  # Diagonal
#             total_deviation += calculate_deviation(np.sum(self.cube[:, i, i]))  # Diagonal

#             total_deviation += calculate_deviation(np.sum(self.cube[i, :, i]))  # Diagonal
#             total_deviation += calculate_deviation(np.sum(self.cube[4-i, :, i]))  # Diagonal

#         # Diagonal Ruang
#         main_diagonal_sum = 0
#         anti_diagonal_sum_1 = 0
#         anti_diagonal_sum_2 = 0
#         anti_diagonal_sum_3 = 0
#         for i in range(self.n):
#             main_diagonal_sum += self.cube[i, i, i]                         
#             anti_diagonal_sum_1 += self.cube[i, self.n - 1 - i, i]          
#             anti_diagonal_sum_2 += self.cube[self.n - 1 - i, i, i]          
#             anti_diagonal_sum_3 += self.cube[i, i, self.n - 1 - i]          

#         total_deviation += calculate_deviation(main_diagonal_sum)
#         total_deviation += calculate_deviation(anti_diagonal_sum_1)
#         total_deviation += calculate_deviation(anti_diagonal_sum_2)
#         total_deviation += calculate_deviation(anti_diagonal_sum_3) 
 
#         # if (total_deviation <= 200):
#         #     print(total_deviation)
        
#         return int(total_deviation) 
#     def swap(self, pos1, pos2):
#             x = self.cube[pos1] 
#             y = self.cube[pos2]
#             self.cube[pos1], self.cube[pos2] =y,x
#     def get_random_position(self):
#         return tuple(random.randint(0, self.n-1) for _ in range(3))
#     def get_neighbors(self):
#         neighbors = []
#         flat_cube = self.cube.flatten()
#         for i in range (len(flat_cube)):
#             for j in range(i+1, len(flat_cube)):
#                 new_cube = flat_cube.copy()
#                 new_cube[i], new_cube[j] = new_cube[j], new_cube[i]
#                 cube_3d = new_cube.reshape(self.n, self.n, self.n)
#                 neighbors.append(DiagonalMagicCube.constructor(cube_3d))
#         return neighbors

