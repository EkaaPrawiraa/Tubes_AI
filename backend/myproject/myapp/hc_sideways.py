import numpy as np
from numba import jit
import random
import time

class SidewaysHillClimbing:
    def __init__(self, cube,max_sideways, max_iterations=1000):
        self.cube = cube
        self.max_iterations = max_iterations
        self.max_sideways = max_sideways
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
            random.shuffle(neighbors)
            
            for neighbor in neighbors:
                new_score = neighbor.evaluate()
                if new_score <= best_score:
                    if new_score < best_score:
                        best_neighbor = neighbor
                        best_score = new_score
                    else:
                        if best_neighbor != neighbor:
                            best_neighbor = neighbor
                            best_score = new_score
            if best_neighbor is None:
                # print(1)
                break
            if best_score > current_score:
                # print(2)
                break
            if self.max_sideways <= 0:
                # print(self.max_sideways)
                # print(3)
                break
            if iteration >= self.max_iterations:
                # print(4)
                break
            if best_score == current_score:
                self.max_sideways -= 1
                
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