import random
import numpy as np

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
        return instance
    
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
 
        if (total_deviation <= 200):
            print(total_deviation)
        
        return int(total_deviation) 

    def swap(self, pos1, pos2):
        x = self.cube[pos1] 
        y = self.cube[pos2]
        self.cube[pos1], self.cube[pos2] =y,x
    
    def get_random_position(self):
        return tuple(random.randint(0, self.n-1) for _ in range(3))
    def get_neighbors(self):
        neighbors = []
        flat_cube = self.cube.flatten()
        for i in range (len(flat_cube)):
            for j in range(i+1, len(flat_cube)):
                new_cube = flat_cube.copy()
                new_cube[i], new_cube[j] = new_cube[j], new_cube[i]
                cube_3d = new_cube.reshape(self.n, self.n, self.n)
                neighbors.append(DiagonalMagicCube.constructor(cube_3d))
        return neighbors


class SteepestHillClimbing:
    def __init__(self, cube, max_iterations=100):
        self.cube = cube
        self.max_iterations = max_iterations
        self.list_result=[]
    
    
    
    def run(self):
        current_score = self.cube.evaluate()
        print(self.cube.cube)
        i = 0
        self.list_result.append((i,self.cube.cube,current_score))
        # for k in range(1):
        while(True):
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

            # for j in range(100):  # Find highest neighbor
            #     pos1 = self.cube.get_random_position()
            #     pos2 = self.cube.get_random_position()
            #     # print(f'Iteration :{i},{j}\n')
            #     # print(self.cube.cube)
            #     # print(current_score)
            #     # print()
            #     self.cube.swap(pos1, pos2)
            #     new_score = self.cube.evaluate()
                
            #     if new_score <= best_score:
            #         best_neighbor = (pos1, pos2)
            #         best_score = new_score
            #     self.cube.swap(pos1, pos2)
            
            if best_neighbor is None: 
                break
            if best_score >= current_score:
                break
            self.cube= best_neighbor
            current_score = best_score
            i+=1
            self.list_result.append((i,self.cube.cube,current_score))
        return self.list_result

def main():
    cube = DiagonalMagicCube()
    initial_score = cube.evaluate()
    print(f"Magic number: {cube.magic_number}")
    print(f"Initial score: {initial_score}")
    # print("Initial cube configuration:")
    # print(cube.cube)
    
    hill_climbing = SteepestHillClimbing(cube)
    final_score = hill_climbing.run()
    
    print(f"Final score: {final_score}")
    # if final_score == 0:
    #     print("Perfect solution found!")
    # else:
    #     print("Local optimum reached.")
    
    # print("Final cube configuration:")
    print(cube.cube)

if __name__ == "__main__":
    main()