import heapq

# Inisialisasi priority queue sebagai list kosong
pq = []

# Menambahkan elemen ke priority queue
heapq.heappush(pq, (1, "prioritas rendah"))
heapq.heappush(pq, (0, "prioritas tinggi"))
heapq.heappush(pq, (2, "prioritas menengah"))

# Mengambil elemen berdasarkan prioritas
while pq:
    item = heapq.heappop(pq)
    print(item)
