import random
import numpy as np
import time

class DiagonalMagicCube:
    def __init__(self, n=5):
        self.n = n
        self.size = n**3
        self.magic_number = self.calculate_magic_number()
        self.cube = self.initialize_cube()
    
    def calculate_magic_number(self):
        return (self.size + 1) * self.n**2 // 2
    
    def initialize_cube(self):
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)
        return np.array(numbers).reshape((self.n, self.n, self.n))
    
    def evaluate(self):
        total_deviation = 0
        
        # Check rows, columns, and pillars
        for i in range(self.n):
            total_deviation += abs(np.sum(self.cube[i, :, :]) - self.magic_number)
            total_deviation += abs(np.sum(self.cube[:, i, :]) - self.magic_number)
            total_deviation += abs(np.sum(self.cube[:, :, i]) - self.magic_number)
        
        # Check space diagonals
        total_deviation += abs(np.trace(self.cube) - self.magic_number)
        total_deviation += abs(np.trace(np.flip(self.cube, axis=0)) - self.magic_number)
        total_deviation += abs(np.trace(np.flip(self.cube, axis=1)) - self.magic_number)
        total_deviation += abs(np.trace(np.flip(self.cube, axis=2)) - self.magic_number)
        
        # Check plane diagonals (simplified, not all planes)
        for i in range(self.n):
            total_deviation += abs(np.trace(self.cube[i, :, :]) - self.magic_number)
            total_deviation += abs(np.trace(self.cube[:, i, :]) - self.magic_number)
            total_deviation += abs(np.trace(self.cube[:, :, i]) - self.magic_number)
        
        return int(np.sum(total_deviation))
    
    def swap(self, pos1, pos2):
        self.cube[pos1], self.cube[pos2] = self.cube[pos2].copy(), self.cube[pos1].copy()
    
    def get_random_position(self):
        return tuple(random.randint(0, self.n-1) for _ in range(3))

class PureStochasticHillClimbing:
    def __init__(self, n=5, max_iterations=100000, probability=0.1):
        self.n = n
        self.max_iterations = max_iterations
        self.probability = probability  # Probabilitas menerima langkah yang lebih buruk
    
    def run(self):
        cube = DiagonalMagicCube(self.n)
        current_score = cube.evaluate()
        best_score = current_score
        best_cube = cube.cube.copy()
        
        for iteration in range(self.max_iterations):
            if current_score == 0:  # Solusi sempurna ditemukan
                return current_score, cube
            
            pos1 = cube.get_random_position()
            pos2 = cube.get_random_position()
            
            cube.swap(pos1, pos2)
            new_score = cube.evaluate()
            
            if new_score < current_score or random.random() < self.probability:
                current_score = new_score
                if current_score < best_score:
                    best_score = current_score
                    best_cube = cube.cube.copy()
            else:
                cube.swap(pos1, pos2)  # Membatalkan pertukaran
            
            if iteration % 10000 == 0:
                print(f"Iterasi {iteration}, Skor terbaik: {best_score}, Skor saat ini: {current_score}")
        
        cube.cube = best_cube
        return best_score, cube

def main():
    start_time = time.time()
    
    shc = PureStochasticHillClimbing(n=5, max_iterations=1000000, probability=0.1)
    final_score, best_cube = shc.run()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Skor akhir: {final_score}")
    if final_score == 0:
        print("Solusi sempurna ditemukan!")
    else:
        print("Solusi terbaik ditemukan (mungkin tidak sempurna)")
    
    print(f"Waktu yang dibutuhkan: {elapsed_time:.2f} detik")
    print("Konfigurasi kubus terbaik:")
    print(best_cube.cube)

if __name__ == "__main__":
    main()