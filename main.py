import ctypes
import time
import os
import math
import random
from datetime import datetime

def py_vector_distance(vec1, vec2):
    """Python реализация евклидова расстояния"""
    if len(vec1) != len(vec2):
        raise ValueError("Векторы должны иметь одинаковую длину")
    
    sum_sq = 0.0
    for v1, v2 in zip(vec1, vec2):
        diff = v1 - v2
        sum_sq += diff * diff
    
    return math.sqrt(sum_sq)

def py_distance_n_times(vec1, vec2, iterations):
    """Многократный вызов Python функции"""
    if iterations <= 0:
        return 0.0, 0.0
    
    start = time.perf_counter()
    total = 0.0
    for _ in range(iterations):
        total += py_vector_distance(vec1, vec2)
    end = time.perf_counter()
    
    return end - start, total

def cpp_distance_n_times(lib, vec1, vec2, iterations):
    """Многократный вызов C++ функции"""
    if lib is None or iterations <= 0:
        return 0.0, 0.0
    
    n = len(vec1)
    arr1 = (ctypes.c_double * n)(*vec1)
    arr2 = (ctypes.c_double * n)(*vec2)
    
    start = time.perf_counter()
    total = lib.vector_distance_n_times(arr1, arr2, n, iterations)
    end = time.perf_counter()
    
    return end - start, total

def compare_performance():
    """Основная функция сравнения производительности"""
    print("=" * 80)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ: C++ DLL vs PYTHON")
    print("Задача: вычисление евклидова расстояния между векторами")
    print("=" * 80)
    
    # Загрузка библиотеки
    cpp_lib = load_cpp_library()
    
    # Генерация тестовых векторов
    print(f"\nГенерация тестовых данных...")
    print(f"Размер векторов: {VECTOR_SIZE} элементов")
    
    random.seed(42)  # Для воспроизводимости
    vec1 = [random.uniform(0, 100) for _ in range(VECTOR_SIZE)]
    vec2 = [random.uniform(0, 100) for _ in range(VECTOR_SIZE)]
    
    # Проверка корректности вычислений
    print("\n[ПРОВЕРКА КОРРЕКТНОСТИ]")
    py_result = py_vector_distance(vec1, vec2)
    
    if cpp_lib:
        n = len(vec1)
        arr1 = (ctypes.c_double * n)(*vec1)
        arr2 = (ctypes.c_double * n)(*vec2)
        cpp_result = cpp_lib.vector_distance(arr1, arr2, n)
        
        diff = abs(py_result - cpp_result)
        if diff < 0.0001:
            print(f"✅ Результаты C++ ({cpp_result:.6f}) и Python ({py_result:.6f}) совпадают.")
        else:
            print(f"⚠️  Результаты различаются: C++={cpp_result:.6f}, Python={py_result:.6f}")
    else:
        print(f"Python результат: {py_result:.6f}")
        cpp_result = 0.0
    
    results_table = []
    
    # Запуск тестов производительности
    print("\n" + "=" * 80)
    print("ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 80)
    
    for iterations, description in TESTS:
        print(f"\n--- Тест: {description}, размер массива {VECTOR_SIZE} ---")
        
        # Python тест
        py_time, py_total = py_distance_n_times(vec1, vec2, iterations)
        print(f"Python общее время: {py_time:.2f} с, среднее за итерацию: {py_time/iterations*1000:.2f} мс")
        
        # C++ тест
        if cpp_lib:
            cpp_time, cpp_total = cpp_distance_n_times(cpp_lib, vec1, vec2, iterations)
            print(f"C++ общее время: {cpp_time*1000:.2f} мс, среднее за итерацию: {cpp_time/iterations*1000:.4f} мс")
            
            # Проверка совпадения результатов
            if abs(py_total - cpp_total) < 0.01:
                print(f"[OK] Суммы расстояний совпадают: {cpp_total:.2f}")
            else:
                print(f"[WARNING] Суммы различаются: C++={cpp_total:.2f}, Python={py_total:.2f}")
            
            # Вычисление ускорения
            if cpp_time > 0:
                speedup = py_time / cpp_time
                print(f"Ускорение C++ над Python: {speedup:.2f}x")
            else:
                speedup = 0
        else:
            cpp_time = 0
            speedup = 0
        
        # Сохранение результатов для таблицы
        results_table.append({
            'iterations': iterations,
            'cpp_time': cpp_time,
            'py_time': py_time,
            'speedup': speedup
        })
    
    # Вывод итоговой таблицы
    print("\n" + "=" * 80)
    print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
    print("=" * 80)
    print(f"{'№':<3} {'Итерации':<12} {'C++ (с)':<12} {'Python (с)':<12} {'Ускорение (раз)':<15}")
    print("-" * 80)
    
    total_speedup = 0
    valid_speedups = 0
    
    for i, result in enumerate(results_table, 1):
        cpp_seconds = f"{result['cpp_time']:.2f}" if cpp_lib else "N/A"
        speedup_str = f"{result['speedup']:.2f}" if result['speedup'] > 0 else "N/A"
        
        print(f"{i:<3} {result['iterations']:<12} {cpp_seconds:<12} {result['py_time']:<12.2f} {speedup_str:<15}")
        
        if result['speedup'] > 0:
            total_speedup += result['speedup']
            valid_speedups += 1
    
    # Вывод среднего ускорения
    if valid_speedups > 0:
        avg_speedup = total_speedup / valid_speedups
        print("-" * 80)
        print(f"Среднее ускорение: {avg_speedup:.2f}x")
        
        print("\n" + "=" * 80)
        print("ВЫВОД:")
        if avg_speedup > 1:
            print(f"C++ модуль в среднем в {avg_speedup:.2f} раз быстрее Python.")
        else:
            print("Python оказался быстрее или сравним с C++.")
    
    print("\n" + "=" * 80)
    print(f"Тестирование завершено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    compare_performance()
