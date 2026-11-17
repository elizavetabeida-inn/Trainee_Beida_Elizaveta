from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import logging
from pyspark.sql.window import Window
from config import JDBC_URL, CONNECTION_PROPERTIES

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("pagila_analysis")


spark = (
    SparkSession.builder.master("local[*]")
    .appName("Pagila Analysis")
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

logger.info("Spark started successfully!")


def load_table(table_name: str):
    return spark.read.jdbc(JDBC_URL, table_name, properties=CONNECTION_PROPERTIES)


category_df = load_table("category")
film_category_df = load_table("film_category")
actor_df = load_table("actor")
film_actor_df = load_table("film_actor")
inventory_df = load_table("inventory")
rental_df = load_table("rental")
payment_df = load_table("payment")
film_df = load_table("film")
city_df = load_table("city")
address_df = load_table("address")
customer_df = load_table("customer")


# Output the number of movies in each category, sorted in descending order.
task_1_df = (
    category_df.join(film_category_df, ["category_id"], "inner")
    .groupBy("name")
    .agg(F.count("film_id").alias("movie_count"))
    .orderBy(F.col("movie_count").desc())
)

logger.info(
    "1 Output the number of movies in each category, sorted in descending order."
)
task_1_df.show(truncate=False)


# Output the 10 actors whose movies rented the most, sorted in descending order.
task_2_df = (
    actor_df.join(film_actor_df, ["actor_id"], "inner")
    .join(inventory_df, ["film_id"], "inner")
    .join(rental_df, ["inventory_id"], "inner")
    .groupBy("actor_id", "first_name", "last_name")
    .agg(F.count("rental_id").alias("rental_count"))
    .orderBy(F.col("rental_count").desc())
    .limit(10)
)

logger.info(
    "2 Output the 10 actors whose movies rented the most, sorted in descending order."
)
task_2_df.show(truncate=False)


# Output the category of movies on which the most money was spent.
task_3_df = (
    category_df.join(film_category_df, ["category_id"], "inner")
    .join(inventory_df, ["film_id"], "inner")
    .join(rental_df, ["inventory_id"], "inner")
    .join(payment_df, ["rental_id"], "inner")
    .groupBy("name")
    .agg(F.sum("amount").alias("total_revenue"))
    .orderBy(F.col("total_revenue").desc())
    .limit(1)
)

logger.info("3 Output the category of movies on which the most money was spent.")
task_3_df.show(truncate=False)


# Output the names of movies that are not in the inventory.
task_4_df = film_df.join(inventory_df, ["film_id"], "left_anti").select("title")

logger.info("4 Output the names of movies that are not in the inventory.")
task_4_df.show(truncate=False)


# Output the top 3 actors who have appeared most in movies in the “Children” category. If several actors have the same number of movies, output all of them.
window_spec = Window.orderBy(F.col("movie_count").desc())

task_5_df = (
    category_df.filter(F.col("name") == "Children")
    .join(film_category_df, ["category_id"], "inner")
    .join(film_actor_df, ["film_id"], "inner")
    .join(actor_df, ["actor_id"], "inner")
    .groupBy("actor_id", "first_name", "last_name")
    .agg(F.count("film_id").alias("movie_count"))
    .withColumn("rank", F.dense_rank().over(window_spec))
    .filter(F.col("rank") <= 3)
    .orderBy(F.col("movie_count").desc())
    .drop("rank")
)

logger.info(
    "5 Output the top 3 actors who have appeared most in movies in the “Children” category. If several actors have the same number of movies, output all of them."
)
task_5_df.show(truncate=False)


# Output cities with the number of active and inactive customers (active - customer.active = 1). Sort by the number of inactive customers in descending order.
task_6_df = (
    city_df.join(address_df, ["city_id"], "inner")
    .join(customer_df, ["address_id"], "inner")
    .groupBy("city_id", "city")
    .agg(
        F.sum(F.when(F.col("active") == 1, 1).otherwise(0)).alias("active_customers"),
        F.sum(F.when(F.col("active") == 0, 1).otherwise(0)).alias("inactive_customers"),
    )
    .orderBy(F.col("inactive_customers").desc())
)

logger.info(
    "6 Output cities with the number of active and inactive customers (active - customer.active = 1). Sort by the number of inactive customers in descending order."
)
task_6_df.show(truncate=False)


# Output the category of movies that have the highest number of total rental hours in the cities (customer.address_id in this city), and that start with the letter “a”. Do the same for cities with a “-” symbol.
rental_city_category_df = (
    rental_df.filter(F.col("return_date").isNotNull())
    .withColumn(
        "rental_hours",
        (
            F.unix_timestamp(F.col("return_date"))
            - F.unix_timestamp(F.col("rental_date"))
        )
        / 3600.0,
    )
    .join(customer_df, ["customer_id"], "inner")
    .join(address_df, ["address_id"], "inner")
    .join(city_df, ["city_id"], "inner")
    .join(inventory_df, ["inventory_id"], "inner")
    .join(film_category_df, ["film_id"], "inner")
    .join(category_df, ["category_id"], "inner")
)

top_cities_starting_with_a_df = (
    rental_city_category_df.filter(F.lower(F.col("city")).startswith("a"))
    .groupBy("name")
    .agg(F.round(F.sum("rental_hours"), 2).alias("total_rental_hours"))
    .orderBy(F.col("total_rental_hours").desc())
    .limit(1)
)

logger.info("7.1 Top category for cities starting with 'a':")
top_cities_starting_with_a_df.show(truncate=False)

top_cities_with_dash_df = (
    rental_city_category_df.filter(F.col("city").contains("-"))
    .groupBy("name")
    .agg(F.round(F.sum("rental_hours"), 2).alias("total_rental_hours"))
    .orderBy(F.col("total_rental_hours").desc())
    .limit(1)
)

logger.info("7.2 Top category for cities containing '-':")
top_cities_with_dash_df.show(truncate=False)
