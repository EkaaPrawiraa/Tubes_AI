import random
import numpy as np

class DiagonalMagicCube:
    def __init__(self, n=5, cube = None):
        self.n = n
        self.size = n**3
        self.magic_number = self.calculate_magic_number()
        self.cube = cube if cube is not None else self.initialize_cube()
    
    def calculate_magic_number(self):
        return ((self.size + 1) * self.n) // 2
    
    def initialize_cube(self):
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)
        return np.array(numbers).reshape((self.n, self.n, self.n))
    
    def evaluate(self):
        total_deviation = 0

        def calculate_deviation(sum_value):
            return abs(sum_value - self.magic_number)

        # Check
        for i in range(self.n):
            for j in range(self.n):
                total_deviation += calculate_deviation(np.sum(self.cube[i, j, :]))  # Row
                total_deviation += calculate_deviation(np.sum(self.cube[i, :, j]))  # Column
                total_deviation += calculate_deviation(np.sum(self.cube[:, i, j]))  # Pillar

            total_deviation += calculate_deviation(np.sum(self.cube[i, i, :]))  # Diagonal
            total_deviation += calculate_deviation(np.sum(self.cube[4-i, i, :]))  # Diagonal

            total_deviation += calculate_deviation(np.sum(self.cube[:, i, 4-1]))  # Diagonal
            total_deviation += calculate_deviation(np.sum(self.cube[:, i, i]))  # Diagonal

            total_deviation += calculate_deviation(np.sum(self.cube[i, :, i]))  # Diagonal
            total_deviation += calculate_deviation(np.sum(self.cube[4-i, :, i]))  # Diagonal

        # Diagonal Ruang
        main_diagonal_sum = 0
        anti_diagonal_sum_1 = 0
        anti_diagonal_sum_2 = 0
        anti_diagonal_sum_3 = 0
        for i in range(self.n):
            main_diagonal_sum += self.cube[i, i, i]                         
            anti_diagonal_sum_1 += self.cube[i, self.n - 1 - i, i]          
            anti_diagonal_sum_2 += self.cube[self.n - 1 - i, i, i]          
            anti_diagonal_sum_3 += self.cube[i, i, self.n - 1 - i]          

        total_deviation += calculate_deviation(main_diagonal_sum)
        total_deviation += calculate_deviation(anti_diagonal_sum_1)
        total_deviation += calculate_deviation(anti_diagonal_sum_2)
        total_deviation += calculate_deviation(anti_diagonal_sum_3) 
 

        # print(total_deviation)
        return int(total_deviation) 

    def swap(self, pos1, pos2):
        x = self.cube[pos1] 
        y = self.cube[pos2]
        self.cube[pos1], self.cube[pos2] =y,x
    
    def get_random_position(self):
        return tuple(random.randint(0, self.n-1) for _ in range(3))