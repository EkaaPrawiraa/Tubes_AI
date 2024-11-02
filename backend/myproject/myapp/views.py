from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt  # Nonaktifkan CSRF sementara untuk pengujian lokal; diatur ulang nanti untuk keamanan
def receive_cube(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Mengambil JSON dari body request POST
        final_score = data.get("final_score")  # Mengambil skor akhir
        final_cube = data.get("final_cube")  # Mengambil array kubus

        # Menampilkan data yang diterima (hanya untuk debugging)
        print("Final Score:", final_score)
        print("Final Cube:", final_cube)

        # Mengirim respons bahwa data berhasil diterima
        return JsonResponse({"message": "Data received successfully"})
    
    # Jika metode bukan POST, kembalikan error
    return JsonResponse({"error": "Invalid request"}, status=400)