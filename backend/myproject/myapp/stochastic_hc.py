import numpy as np
from numba import jit
import random
import time

class StochasticHillClimbing:
    def __init__(self, cube, max_iterations=100):
        self.cube = cube
        self.max_iterations = max_iterations
        self.list_result=[]
    
    def run(self):
        start_time = time.time()
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
                current_score = best_score
                iteration+=1
                self.list_result.append((iteration, self.cube.cube, current_score))
            else:
                self.cube.swap(pos1, pos2)
        end_time = time.time()
        total_time = end_time - start_time
        return self.list_result, total_time

# def main():
#     cube = DiagonalMagicCube()
#     initial_score = cube.evaluate()
#     print(f"Initial score: {initial_score}")
#     print("Initial cube configuration:")
#     # print(cube.cube)
   
#     hill_climbing = StochasticHillClimbing(cube)

#     iterations, final_cube, final_score = hill_climbing.run()
#     print(f"Final score: {final_score}")
#     print(f"Number of iterations: {iterations}")
#     print(f"Final cube configuration:\n{final_cube.cube}")
#     if final_score == 0:
#         print("Perfect solution found!")
#     else:
#         print("Local optimum reached.")
    
#     # print("Final cube configuration:")
#     # print(cube.cube)

# if __name__ == "__main__":
#     main()