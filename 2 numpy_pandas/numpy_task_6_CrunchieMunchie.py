import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

calorie_stats = np.loadtxt("data/cereal.csv", delimiter=",")

# в комментариях я вставила строки из задания, чтоб был понятен контекст)
# Разница между средним значением калорий продукции конкурентов и нашими CrunchieMunchies (60 ккал)
average_calories = np.mean(calorie_stats) - 60
logging.info(
    "Разница в количестве калорий между конкурентами и CrunchieMunchies: %s",
    round(average_calories),
)

# Сортируем данные
calorie_stats_sorted = np.sort(calorie_stats)
logging.info(
    "Отсортированный массив с калориями хлопьев у конкурентов: %s", calorie_stats_sorted
)

# считаем медиану
median_calories = np.median(calorie_stats_sorted)
logging.info("Медиана массива калорий конкурентов через np.median: %s", median_calories)
logging.info(
    "Среднее количество калорий у конкурентов через np.mean: %s",
    round(np.mean(calorie_stats)),
)

# нужно выводить попытки угадать процентиль, на котором значение больше 60
logging.info(np.percentile(calorie_stats_sorted, 10))
logging.info(np.percentile(calorie_stats_sorted, 8))
logging.info(np.percentile(calorie_stats_sorted, 5))
logging.info(np.percentile(calorie_stats_sorted, 3))
logging.info(np.percentile(calorie_stats_sorted, 4))
nth_percentile = 4

# Какой процент конкурентов, продукция которых содержит больше 60 калорий
more_calories = np.mean(calorie_stats > 60) * 100
logging.info(
    "Какой процент хлопьев конкурентов содержит больше 60 калорий: %s", more_calories
)

# находим стандартное отклонение
calorie_std = round(np.std(calorie_stats), 2)
logging.info("Стандартное отклонение: %s", calorie_std)
logging.info(
    "Поэтому можно сказать, что большинство хлопьев конкурентов содержат около 100 калорий"
)

# please write a short paragraph outlining your findings
# and how you believe this data can be used to Mycrunch's advantage in marketing CrunchieMunchies.
logging.info(
    """
    В одной порции CrunchieMunchies содержится всего 60 калорий. 
    Разница в количестве калорий между конкурентами и CrunchieMunchies: %s, 
    а медианный показатель калорийности составляет около %s калорий.
    Это дает компании MyCrunch весомый аргумент для позиционирования
    CrunchieMunchies как низкокалорийной альтернативы продуктам конкурентов.
""",
    round(average_calories),
    median_calories,
)  # 60 калорий - это по условию, тут переменной не заменить
