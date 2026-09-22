import os
import psycopg2
import json
from dotenv import load_dotenv
from psycopg2.extras import execute_batch



class Database:
    # подключение к бд и выполнение запросов

    def __init__(self, db_params: dict):
        self.db_params = db_params

    def get_connection(self):
        return psycopg2.connect(**self.db_params)

    def execute_script(self, sql_script: str):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
            conn.commit()


class DataReader:
    # чтение данных из json файлов

    @staticmethod
    def load_json(file_path: str) -> list:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)


class DataUploader:
    # Запись загруженных файлов в бд

    def __init__(self, db: Database):
        self.db = db

    def upload_rooms(self, rooms: list):
        query = """
            INSERT INTO rooms (id, name)
            VALUES (%(id)s, %(name)s)
            ON CONFLICT (id) DO NOTHING;
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                execute_batch(cursor, query, rooms)
            conn.commit()

    def upload_students(self, students: list):
        query = """
            INSERT INTO students (birthday, id, name, room, sex)
            VALUES (%(birthday)s, %(id)s, %(name)s, %(room)s, %(sex)s)
            ON CONFLICT (id) DO NOTHING;
        """

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                execute_batch(cursor, query, students)
            conn.commit()


class AnalyticsService:
    # Выполнение аналитических запросов

    def __init__(self, db: Database):
        self.db = db

    def _fetch_all(self, query: str) -> list:
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                results = []
                for row in cursor.fetchall():
                    formatted_row = {}
                    for col, val in zip(columns, row):
                        # преобразуем числовые типы к float для JSON
                        formatted_row[col] = float(val) if isinstance(val, (int, float)) and not isinstance(val,
                                                                                                            bool) else str(
                            val)
                    results.append(formatted_row)
                return results

    def get_rooms_with_student_count(self) -> list:
        query = """
            SELECT
                r.id,
                r."name",
                COUNT(s.id) AS students_count
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY 
                r.id,
                r."name";
        """
        return self._fetch_all(query)

    def get_top5_smallest_avg_age(self) -> list:
        query = """
            SELECT
                r.id,
                r."name",
                ROUND(AVG(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))), 2) AS avg_age
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY 
                r.id, 
                r."name"
            ORDER BY avg_age ASC
            LIMIT 5;
        """
        return self._fetch_all(query)

    def get_top5_biggest_age_difference(self) -> list:
        query = """
            SELECT 
                r.id, 
                r.name, 
                EXTRACT(YEAR FROM AGE(MAX(s.birthday), MIN(s.birthday))) AS age_difference
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY 
                r.id, 
                r.name
            ORDER BY age_difference DESC
            LIMIT 5;
        """
        return self._fetch_all(query)

    def get_mixed_sex_rooms(self) -> list:
        query = """
            SELECT 
                r.id, 
                r.name
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY 
                r.id, 
                r.name
            HAVING COUNT(DISTINCT s.sex) > 1;
        """
        return self._fetch_all(query)


class DataExporter:
    # экспорт в json или xml

    @staticmethod
    def export_json(data: dict, output_file: str):
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


# параметры подключения к бд
load_dotenv()
db_params = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

db = Database(db_params)

# создание таблиц
schema_sql = """
    CREATE TABLE IF NOT EXISTS rooms (
        id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL 
    );

    CREATE TABLE IF NOT EXISTS students (
        id INT PRIMARY KEY ,
        birthday DATE NOT NULL,
        name VARCHAR(255) NOT NULL,
        room INT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
        sex CHAR(1) NOT NULL
    );
"""
db.execute_script(schema_sql)

# создание индексов
indexes_sql = """
    CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room);
    CREATE INDEX IF NOT EXISTS idx_students_room_birthday ON students(room, birthday);
    CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);
"""
db.execute_script(indexes_sql)

# загрузка данных из файлов json
rooms_data = DataReader.load_json("rooms.json")
students_data = DataReader.load_json("students.json")

uploader = DataUploader(db)
uploader.upload_rooms(rooms_data)
uploader.upload_students(students_data)

# выполнение аналитических запросов
analytics = AnalyticsService(db)
results = {
    "rooms_with_student_count": analytics.get_rooms_with_student_count(),
    "top5_smallest_avg_age": analytics.get_top5_smallest_avg_age(),
    "top5_biggest_age_difference": analytics.get_top5_biggest_age_difference(),
    "mixed_sex_rooms": analytics.get_mixed_sex_rooms()
}

# выгрузка результатов запросов в output.json
DataExporter.export_json(results, "output.json")
print(f"Готово! Результаты сохранены в файл: output.json")


