import numpy as np
from scipy.spatial.distance import cdist
import timeit

#Task 1: Calculate the product of nonzero elements on the diagonal of a rectangular matrix.
#For example, for X = np.array([[1, 0, 1], [2, 0, 2], [3, 0, 3], [4, 4, 4]]) answer is 3.
print("Task 1. Перемножить элементы главной диагонали матрицы")
input_matrix = np.array([[1, 0, 1], [2, 0, 2], [3, 0, 3], [4, 4, 4]])

diagon = np.diag(input_matrix) #находим главную диагональ
nn_diagon = diagon[diagon != 0] #оставляем только ненулевые элементы
result = np.prod(nn_diagon) #перемножаем все элементы

print(result)
print()

#Task 2: Two vectors x and y are given. Check if they define the same multiset.
#For example, for x = np.array([1, 2, 2, 4]), y = np.array([4, 2, 1, 2]) answer is True.
print("Task 2. Проверить одинаковый ли набор элементов у двух векторов")
x = np.array([1, 2, 2, 4])
y = np.array([4, 2, 1, 2])

x = np.sort(x)
y = np.sort(y)

print(np.array_equal(x, y))
print()

#Task 3: Find the maximum element in the vector x among the elements preceded by zero.
#For example, for x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0]) answer is 5.
print("Task 3. Найти максимальный элемент, из стоящих после нулей")

x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0])

result = x[1:][x[:-1] == 0].max()

print(result)
print()

#Task 4: Implement run-length encoding. For some vector x, it is necessary to return a tuple of two vectors of the same length.
# The first one contains numbers and the second one contains how many times they need to be repeated.
#For example, for x = np.array([2, 2, 2, 3, 3, 3, 5]) answer is (np.array([2, 3, 5]), np.array([3, 3, 1])).
print("Task 4. ")

x = np.array([2, 2, 2, 3, 3, 3, 5])

changes = x[:-1] != x[1:]
y = np.where(changes)[0] #находим индексы после которых меняется значение повторояющегося
y += 1 #находим непосредственно индекс с которого меняется значение

bounds = np.concatenate(([0], y, [len(x)])) #находим границы каждого значения

values = x[bounds[:-1]] #сами числа
times = np.diff(bounds) #сколько раз встречаются

result = (values, times)
print(result)
print()

#Task 5: Two samples of objects are given - X and Y.
# Calculate the matrix of Euclidean distances between objects.
# Compare with function scipy.spatial.distance.cdist by operating speed.
print("Task 5. Считаем евклидово расстояние между объектами")

X = np.array([
    [1, 2],
    [4, 5]
])
Y = np.array([
    [1, 1],
    [2, 3],
    [6, 5]
])

difference = X[:, None, :] - Y[None, :, :] #вычитаем из каждой точки x точку y
distances = np.sqrt(np.sum((difference ** 2), axis=2)) #считаем по формуле евклидово расстояния

distances_cdist = cdist(X, Y) #рассчитаем расстояние используя встроенную функцию

print(f"Посчитали вручную: \n {distances}")
print(f"Через встроенную функцию: \n {distances_cdist}")


#засекаем скорость выполнения чтобы сравнить
time_numpy = timeit.timeit(
    lambda: np.sqrt(np.sum((X[:, None, :] - Y[None, :, :]) ** 2, axis=2)),
    number=100
)
time_cdist = timeit.timeit(
    lambda: cdist(X, Y),
    number=100
)

print("NumPy:", time_numpy)
print("cdist:", time_cdist)