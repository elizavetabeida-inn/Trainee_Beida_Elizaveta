import numpy as np

calorie_stats = np.loadtxt("data/cereal.csv", delimiter=",")

#в комментариях я вставила строки из задания, чтоб был понятен контекст)
#Разница между средним значением калорий продукции конкурентов и нашими CrunchieMunchies (60 ккал)
average_calories = np.mean(calorie_stats) - 60
print(f"Разница в количестве калорий между конкурентами и CrunchieMunchies: {round(average_calories)}")

#Сортируем данные
calorie_stats_sorted = np.sort(calorie_stats)
print(f"Отсортированный массив с калориями хлопьев у конкурентов: {calorie_stats_sorted}")

#считаем медиану
median_calories = np.median(calorie_stats_sorted)
print(f"Медиана массива калорий конкурентов через np.median: {median_calories}")
print(f"Среднее количество калорий у конкурентов через np.mean: {round(np.mean(calorie_stats))}")

#нужно выводить попытки угадать процентиль, на котором значение больше 60
print(np.percentile(calorie_stats_sorted, 10))
print(np.percentile(calorie_stats_sorted, 8))
print(np.percentile(calorie_stats_sorted, 5))
print(np.percentile(calorie_stats_sorted, 3))
print(np.percentile(calorie_stats_sorted, 4))
nth_percentile = 4

#Какой процент конкурентов, продукция которых содержит больше 60 калорий
more_calories = np.mean(calorie_stats > 60) * 100
print(f"Какой процент хлопьев конкурентов содержит больше 60 калорий: {more_calories}")

#находим стандартное отклонение
calorie_std = round(np.std(calorie_stats), 2)
print(f"Стандартное отклонение: {calorie_std}")
print("Поэтому можно сказать, что большинство хлопьев конкурентов содержат около 100 калорий")

#please write a short paragraph outlining your findings
# and how you believe this data can be used to Mycrunch's advantage in marketing CrunchieMunchies.
print("""
    В одной порции CrunchieMunchies содержится всего 60 калорий.
    Большинство конкурирующих сухих завтраков содержат более 60 калорий, 
    а медианный показатель калорийности составляет около 110 калорий.
    Это дает компании MyCrunch весомый аргумент для позиционирования
    CrunchieMunchies как низкокалорийной альтернативы продуктам конкурентов.
""")








