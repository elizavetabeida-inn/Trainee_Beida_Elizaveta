import psycopg2

class Database:
    """Подключение к бд и выполнение запросов"""

    def __init__(self, db_params: dict):
        self.db_params = db_params

    def get_connection(self):
        return psycopg2.connect(**self.db_params)

    def execute_script(self, sql_script: str):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
            conn.commit()