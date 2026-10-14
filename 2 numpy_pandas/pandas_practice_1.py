import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

df = pd.read_csv("data/adult.data.csv")
df.head()

# 1. Calculate how many men and women (attribute sex) are represented in this dataset.
logging.info("1. Сколько мужчин и женщин в датасете:")

# result = df.groupby("sex")["sex"].count()
result = df["sex"].value_counts()

logging.info("%s\n", result)


# 2. What is the average age of men (attribute age) across the entire dataset?
logging.info("2. Средний возраст мужчин:")

result = df[df["sex"] == "Male"]["age"].mean()

logging.info("%s\n", round(result))


# 3. What is the proportion of United States citizens (native-country attribute)?
logging.info("3. Какая доля граждан США?:")

result = (df["native-country"] == "United-States").mean()

logging.info("%s\n", result)

# 4-5. Calculate the mean and standard deviation of the age of those
# who earn more than 50K per year (the salary attribute) and those who earn less than 50K per year

result_least_than_50K = df[df["salary"] == "<=50K"]["age"].agg(["mean", "std"])
result_more_than_50K = df[df["salary"] == ">50K"]["age"].agg(["mean", "std"])

logging.info(
    "4. стандартное отклонение и средний возраст людей, зарабатывающих больше 50K в год: %s\n",
    result_more_than_50K,
)
logging.info(
    "5. стандартное отклонение и средний возраст людей, зарабатывающих меньше 50K в год: \n %s\n",
    result_least_than_50K,
)

# 6. Is it true that people who earn more than 50k have at least a higher education?
# (education indicator – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters or Doctorate)
higher_education = [
    "Bachelors",
    "Prof-school",
    "Assoc-acdm",
    "Assoc-voc",
    "Masters",
    "Doctorate",
]
result = df.loc[df["salary"] == ">50K", "education"].isin(higher_education).all()

logging.info(
    "6. Правда ли, что у людей, которые получают >50K в год, как минимум высшее образование?"
)
logging.info("%s\n", result)

# 7. Find age statistics for each race (race attribute) and each gender. Use groupby and describe.
# Find the maximum age of males of the Asian-Pac-Islander race.

result = df.groupby(["race", "sex"])["age"].describe()
logging.info("7. Статистика по каждому гендеру в каждой расе:")
logging.info(result)

result = df[(df["race"] == "Asian-Pac-Islander") & (df["sex"] == "Male")]["age"].max()
logging.info("Максимальный возраст в расе Asian-Pac-Islander")
logging.info("%s\n", result)

# 8. Among whom is the proportion of high-earning individuals (>50K) higher: married or single men (marital-status indicator)?
# We consider those whose marital-status begins with Married (Married-civ-spouse, Married-spouse-absent, or Married-AF-spouse)
# to be married; the rest are considered single.

married = df[(df["sex"] == "Male") & (df["marital-status"].str.startswith("Married"))]

single = df[(df["sex"] == "Male") & (~df["marital-status"].str.startswith("Married"))]

high_earning_married = (married["salary"] == ">50K").sum()
high_earning_single = (single["salary"] == ">50K").sum()

logging.info(
    "8. Количество женатых мужчин с высоким доходом:  %s", high_earning_married
)
logging.info(
    "Количество холостых мужчин с высоким доходом:  %s \n", high_earning_single
)

# 9. What is the maximum number of hours a person works per week (hours-per-week indicator)?
# How many people work that many hours, and what percentage of them earn a lot?

max_hours = df["hours-per-week"].max()

max_workers = df[df["hours-per-week"] == max_hours]
how_many_people = len(max_workers)

high_earners = (max_workers["salary"] == ">50K").sum()
percentage = high_earners / len(max_workers) * 100

logging.info("9. Максимальное количество рабочих часов за неделю: %s", max_hours)
logging.info("Сколько людей работают {max_hours} часов: %s", how_many_people)
logging.info(
    "Процент людей с доходом >50K работающих %s часов: %s \n",
    max_hours,
    round(percentage, 2),
)

# 10. Calculate the average working hours (hours-per-week) of low and high earners (salary) for each country (native-country).

result = df.groupby(["native-country", "salary"])["hours-per-week"].mean().round(2)

logging.info(
    "10. Среднее количество рабочих часов в неделю для каждой страны и для каждого уровня зарплаты:"
)
logging.info("%s\n", result)

# 11.Group people into age groups young, adult, retiree, where:
# young corresponds to 16-35 years old
# adult - 35-70 years old
# retiree - 70-100 years old
# Enter the name of the appropriate age group for each person in the new AgeGroup column.

df.loc[df["age"].between(16, 35), "AgeGroup"] = "young"
df.loc[df["age"].between(36, 70), "AgeGroup"] = "adult"
df.loc[df["age"].between(71, 100), "AgeGroup"] = "retiree"

logging.info("11. Добавить новый столбец AgeGroup: ")
logging.info(df[["age", "AgeGroup"]].head(10))

# 12-13. Determine the number of people earning >50K in each age group (AgeGroup column),
# and also output the name of the age group in which people most often earn more than 50K (>50K)

result = df[df["salary"] == ">50K"].groupby("AgeGroup")["salary"].count()
logging.info("\n12. Сколько людей в каждой возрастной группе зарабатывает больше 50K:")
logging.info(result)

result2 = result.idxmax()
logging.info(
    "13. В какой возрастной группе встречается больше всего людей с зарплатой >50K:: %s\n",
    result2,
)

# 14. Group people by employment type (the occupation column) and determine the number of people in each group.
# Then write a filter function, filter_func, that will return only those groups in which the average age (the age column)
# is 40 or less and in which all employees work more than 5 hours per week (the hours-per-week column).

by_employment_type = df.groupby("occupation")
logging.info("14. Количество сотрудников по должностям:")
logging.info(by_employment_type["occupation"].count())


def filter_func(data):
    return (data["age"].mean() <= 40) and (data["hours-per-week"] > 5).all()


result = by_employment_type.filter(filter_func)

logging.info(
    "\nТипы сотрудников у которых средних возраст меньше или = 40 и которые работают больше пяти часов в неделю:"
)
logging.info(result["occupation"].value_counts())
