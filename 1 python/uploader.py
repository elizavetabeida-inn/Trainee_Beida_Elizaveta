from psycopg2.extras import execute_batch
from db import Database

class DataUploader:
    """Запись загруженных файлов в бд"""

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