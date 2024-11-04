from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .diagonal_magic_cube import DiagonalMagicCube
from .random_restart_HC import RandomRestartHillClimbing
from .steepest_ascent_HC import SteepestHillClimbing
import numpy as np
from .hc_sideways import SidewaysHillClimbing
from .stochastic_hc import StochasticHillClimbing
from .geneticv2 import play
from .simulated_annealing import SimulatedAnnealing

# Create your views here.

@csrf_exempt 
def receive_cube(request):
    if request.method == "POST":
        print('start')
        cube = DiagonalMagicCube()
        data = json.loads(request.body)  
        print("Request Body:", request.body)

        if (int(data['algorithm'])== 1): #steepest
            hill_climbing = SteepestHillClimbing(cube)
            result,total_time = hill_climbing.run()
            processed_result = [
                (i, j.tolist() if isinstance(j, np.ndarray) else j, k)
                for i, j, k in result
            ]
            # print(result)
            return JsonResponse({
                    "message": "Data received successfully",
                    "result": processed_result,
                    "total_time": total_time
                })
        elif (int(data['algorithm']) == 2): #random restart
            max_iteration = data['max_iteration'] 
            hill_climbing = RandomRestartHillClimbing(cube,max_iteration)
            result,total_time = hill_climbing.run()
            processed_result = [
                (i, j.tolist() if isinstance(j, np.ndarray) else j, k,l)
                for i, j, k, l in result
            ]
            return JsonResponse({
                    "message": "Data received successfully",
                    "result": processed_result,
                    "total_time": total_time
                })
            
        elif (int(data['algorithm']) == 3):#sideways
            max_sideways = data['max_iteration']
            hill_climbing = SidewaysHillClimbing(cube, max_sideways)
            result,total_time = hill_climbing.run()
            processed_result = [
                (i, j.tolist() if isinstance(j, np.ndarray) else j, k)
                for i, j, k in result
            ]
            return JsonResponse({
                    "message": "Data received successfully",
                    "result": processed_result,
                    "total_time": total_time
                })
        elif (int(data['algorithm']) == 4): #sthocastic
            hill_climbing = StochasticHillClimbing(cube)
            result,total_time = hill_climbing.run()
            processed_result = [
                (i, j.tolist() if isinstance(j, np.ndarray) else j, k)
                for i, j, k in result
            ]
            return JsonResponse({
                    "message": "Data received successfully",
                    "result": processed_result,
                    "total_time": total_time
            })
        elif (data["algorithm"]==6): #ga
            result,total_time = play(data['population'], data['max_iteration'])
            processed_result = [
                (
                    i,                                          
                    j.tolist() if isinstance(j, np.ndarray) else j,  # cube state
                    k, l,m                                           
                ) 
                for i, j, k, l, m in result
            ]
            
            return JsonResponse({
                    "message": "Data received successfully",
                    "result": processed_result,
                    "total_time": total_time,
            })
        elif (int(data['algorithm'])==5): #simulated
            simulated = SimulatedAnnealing(cube)
            result,total_time = simulated.run()
            processed_result = [
                (
                    i,                                          
                    j.tolist() if isinstance(j, np.ndarray) else j,  # cube state
                    k, l,m                                           
                ) 
                for i, j, k, l, m in result
            ]


            return JsonResponse({
                    "message": "Data received successfully",
                    "result": processed_result,
                    "total_time": total_time,
            })
        # elif (data.algorithm==6): ga
        return JsonResponse({"error":"Algorithm not recognized"},status = 404)
    # Jika metode bukan POST, kembalikan error
    return JsonResponse({"error": "Invalid request"}, status=400)