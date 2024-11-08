import random
import numpy as np
import time


class RandomRestartHillClimbing:
    def __init__(self, cube, max_iterations=100):
        self.cube = cube
        self.max_iterations = max_iterations
        self.list_result=[]
    
    def run(self):
        start_time = time.time()
        current_score = self.cube.evaluate()
        # print(self.cube.cube)
        
        self.list_result.append((0,self.cube.cube,current_score,0))
        for k in range(self.max_iterations):
            if current_score == 0:  
                    break
            i = 0
            while(True): #hill climbing
                if current_score == 0:  
                    break
                
                best_neighbor = None
                best_score = current_score

                # Find highest neighbor
                neighbors = self.cube.get_neighbors()
                for neighbor in neighbors:
                    new_score = neighbor.evaluate()
                    if new_score < best_score:
                        best_neighbor = neighbor
                        best_score = new_score
                if best_neighbor is None or best_score >= current_score:
                    break
                self.cube= best_neighbor
                current_score = best_score
                i+=1
                self.list_result.append((i,self.cube.cube,current_score,k))
            if current_score != 0:
                self.cube = self.cube.generate_random_cube()
                current_score = self.cube.evaluate()
        end_time = time.time()
        total_time = end_time - start_time
        return self.list_result, total_time

# 
