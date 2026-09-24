import json

class DataExporter:
    """Экспорт в json или xml"""

    @staticmethod
    def export_json(data: dict, output_file: str):
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)