import numpy as np
from numba import jit
import random
import time

class SidewaysHillClimbing:
    def __init__(self, cube, max_iterations=100):
        self.cube = cube
        self.max_iterations = max_iterations
        self.max_sideways = 100
        self.list_result=[]
    
    def run(self):
        start_time = time.time()
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
            self.list_result.append((iteration, self.cube.cube, current_score))
        end_time = time.time() 
        total_time = end_time - start_time
        return self.list_result,total_time

# def main():

#     np.random.seed(42)
    
#     cube = DiagonalMagicCube()
#     initial_score = cube.evaluate()
#     print(f"Initial score: {initial_score}")
    
#     hill_climbing = SidewaysHillClimbing(cube)
#     iterations, final_cube, final_score = hill_climbing.run()
    
#     print(f"Final score: {final_score}")
#     print(f"Number of iterations: {iterations}")
#     print(f"Final cube configuration:\n{final_cube.cube}")
#     if final_score == 0:
#         print("Perfect solution found!")
#     else:
#         print("Local optimum reached.")

# if __name__ == "__main__":
#     main()