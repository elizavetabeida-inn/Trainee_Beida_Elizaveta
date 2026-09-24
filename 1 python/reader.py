import json

class DataReader:
    """Чтение данных из json файлов"""

    @staticmethod
    def load_json(file_path: str) -> list:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)