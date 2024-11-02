import json
import requests
import random
import numpy as np
import time

class SteepestHillClimbing:
    def __init__(self, cube):
        self.cube = cube
        self.list_result=[]
        
    def run(self):
        start_time = time.time()
        current_score = self.cube.evaluate()
        print(self.cube.cube)
        i = 0
        self.list_result.append((i,self.cube.cube,current_score))

        while(True):
            if current_score == 0:  
                break
            
            best_neighbor = None
            best_score = current_score
            neighbors = self.cube.get_neighbors()
            for neighbor in neighbors:
                    new_score = neighbor.evaluate()
                    if new_score <= best_score:
                        best_neighbor = neighbor
                        best_score = new_score
                        break
            if best_neighbor is None: 
                break
            if best_score >= current_score:
                break
            self.cube= best_neighbor
            current_score = best_score
            i+=1
            self.list_result.append((i,self.cube.cube,current_score))

        end_time = time.time()
        total_time = end_time - start_time
        return self.list_result,total_time




