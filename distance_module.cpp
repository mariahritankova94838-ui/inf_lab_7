import math
import time

def calculate_distance(vec1, vec2):
    if len(vec1) != len(vec2):
        return -1.0
    
    sum_val = 0.0
    for i in range(len(vec1)):
        diff = vec2[i] - vec1[i]
        sum_val += diff * diff
    
    return math.sqrt(sum_val)

def calculate_distance_n_times(N, vec1, vec2):
    start_time = time.perf_counter()
    
    total = 0.0
    for i in range(N):
        result = calculate_distance(vec1, vec2)
        total += result
    
    dummy = total
    
    end_time = time.perf_counter()
    return end_time - start_time

