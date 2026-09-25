from config import db_params
from db import Database
from reader import DataReader
from uploader import DataUploader
from analytics import AnalyticsService
from exporter import DataExporter
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Load student and room data into DB")

    parser.add_argument("--students", required=True, help="Path to students file")

    parser.add_argument("--rooms", required=True, help="Path to rooms file")

    args = parser.parse_args()

    db = Database(db_params)

    # создание таблиц
    schema_sql = """
        CREATE TABLE IF NOT EXISTS rooms (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL 
        );
        
        DO $$
        BEGIN
            CREATE TYPE sex_type AS ENUM ('M', 'F');
        EXCEPTION
            WHEN duplicate_object THEN NULL;
        END
        $$;
        
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY ,
            birthday DATE NOT NULL,
            name VARCHAR(255) NOT NULL,
            room INT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
            sex sex_type NOT NULL
        );
    """
    db.execute_script(schema_sql)


    # загрузка данных из файлов json
    rooms_data = DataReader.load_json(args.rooms)
    students_data = DataReader.load_json(args.students)

    uploader = DataUploader(db)
    uploader.upload_rooms(rooms_data)
    uploader.upload_students(students_data)


    # создание индексов
    indexes_sql = """
        CREATE INDEX IF NOT EXISTS idx_students_room_birthday ON students(room, birthday);
        CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);
    """
    db.execute_script(indexes_sql)


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
    logger.info("Готово! Результаты сохранены в файл: output.json")

if __name__ == "__main__":
    main()
