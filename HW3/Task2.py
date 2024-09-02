import time
import multiprocessing

def get_factors(number):
    factors = set()
    for i in range(1, int(number**0.5) + 1):
        if number % i == 0:
            factors.add(i)
            factors.add(number // i)
    return sorted(factors)

# Синхронна версія для порівняння
def factorize(*numbers):
    return [get_factors(number) for number in numbers]

# Паралельна версія
def factorize_multy(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        return pool.map(get_factors, numbers)

# Вимірювання часу виконання синхронної версії
start_time = time.time()
a, b, c, d = factorize(128, 255, 99999, 10651060)
end_time = time.time()
print(f"Synchronous execution time: {end_time - start_time} seconds")

# Перевірка результатів для синхронної версії
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

# Вимірювання часу виконання паралельної версії
start_time = time.time()
numbers = [128, 255, 99999, 10651060]
a, b, c, d = factorize_multy(numbers)
end_time = time.time()
print(f"Parallel execution time: {end_time - start_time} seconds")

# Перевірка результатів для паралельної версії
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
