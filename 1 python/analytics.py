from db import Database

class AnalyticsService:
    """Выполнение аналитических запросов"""

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