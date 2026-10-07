import numpy as np
import itertools

rng = np.random.default_rng()
a = rng.random(5)


# 1 Given a random array, change the sign of elements whose values are between 3 and 8
print("1 числа от 3 до 8 с противоположным знаком")

#list
arr1_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for i in range(len(arr1_list)):
    if 3 <= arr1_list[i] <= 8:
        arr1_list[i] *= -1

print(arr1_list)

#np
arr2_np = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
arr2_np[(arr2_np >= 3) & (arr2_np <= 8)] *= -1
print(arr2_np)
print()

# 2 Replace the maximum element of a random array with 0
print("2 максимальный элемент заменить на 0")

#list
max_val = max(arr1_list)
max_index = arr1_list.index(max_val)
arr1_list[max_index] = 0
print(arr1_list)

#через np
arr2_np[np.max(arr2_np)] = 0
print(arr2_np)
print()

# 3 Construct the direct product of arrays (all combinations with each element). A two-dimensional array is provided as input.
print("3 декартово произведение массивов")
#через list
arr3_list = [[1, 2], [3, 4]]

result = list(itertools.product(*arr3_list))
print(result)

#через numpy
arr3_np = np.array([[1, 2], [3, 4]])

result = np.array(np.meshgrid(*arr3_np)).T.reshape(-1, len(arr3_np))
print(result)
print()


# 4. Given two arrays, A (8x3) and B (2x2), find rows in A that contain elements from each row in B, regardless of the order of the elements in B.
print("Вывести строки масссива A которые содержат элементы из каждой строки массива B")
A = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 3, 5],
    [2, 4, 6],
    [5, 7, 8],
    [1, 4, 7],
    [2, 3, 8]
]
B = [
    [1, 3],
    [4, 6]
]

#через list
result = []

for b_row in B:
    rows = []
    for a_row in A:
        if all(x in a_row for x in b_row):
            rows.append(a_row)
    result.append(rows)
print(result)

#через numpy
A = np.array(A)
B = np.array(B)

result = []
for b_row in B:
    mask = np.all(
        [np.any(A == value, axis=1) for value in b_row],
        axis=0
    )
    result.append(A[mask])
print(result)

#5. Given a 10x3 matrix, find rows of unequal values (for example, the row [2,2,3] remains, the row [3,3,3] is deleted)
print("Удалить строки в которых все элементы одинаковые")

matrix_list = [
    [2, 2, 3],
    [3, 3, 3],
    [1, 5, 1],
    [0, 0, 0],
    [7, 8, 9],
    [4, 4, 4],
    [2, 1, 2],
    [5, 5, 5],
    [1, 2, 3],
    [6, 6, 6]
]
#через List
result = []
for row in matrix_list:
    if len(set(row)) > 1:
        result.append(row)
print(result)

#через numpy
matrix_np = np.array(matrix_list)

mask = np.array([len(np.unique(row)) > 1 for row in matrix_np])
result = matrix_np[mask]

print(result)
print()

#6. Given a two-dimensional array, remove the rows that are repeated.
print("6 вывести двумерный массив у которого удалены повторяющиеся строки")
arr6_list = [
    [1, 2, 3],
    [4, 5, 6],
    [1, 2, 3],
    [7, 8, 9],
    [4, 5, 6]
]

result = []
for row in arr6_list:
    if row not in result:
        result.append(row)
print(result)

#через numpy
arr6_np = np.array(arr6_list)

result = np.unique(arr6_np, axis=0)
print(result)


