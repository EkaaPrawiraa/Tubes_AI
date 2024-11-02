from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .diagonal_magic_cube import DiagonalMagicCube
from .random_restart_HC import RandomRestartHillClimbing
from .steepest_ascent_HC import SteepestHillClimbing
import numpy as np
# from .st import DiagonalMagicCube

# Create your views here.

@csrf_exempt 
def receive_cube(request):
    if request.method == "POST":
        print('start')
        cube = DiagonalMagicCube()
        data = json.loads(request.body)  
        print("Request Body:", request.body)

        if (data['algorithm']== 1): #steepest
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
        elif (data['algorithm'] == 2): #random restart
            max_iteration = data['max_iteration'] 
            hill_climbing = RandomRestartHillClimbing(cube,max_iteration)
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
            
        # elif (data.algorithm==1):
        # elif (data.algorithm==1):
        # elif (data.algorithm==1):
        # elif (data.algorithm==1):
        return JsonResponse({"error":"Algorithm not recognized"},status = 404)
    # Jika metode bukan POST, kembalikan error
    return JsonResponse({"error": "Invalid request"}, status=400)