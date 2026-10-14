import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def load_and_aggregate_bom(file_path: str) -> pd.DataFrame:
    """Загружает датасет и агрегирует помесячные данные до годового уровня (plant, year)"""
    df = pd.read_excel(file_path)

    df.columns = [c.lower() for c in df.columns]

    # для группировки по году, заводу и материал-компоненту
    group_cols = [
        "plant_id",
        "year",
        "produced_material",
        "produced_material_production_type",
        "produced_material_release_type",
        "component_material",
        "component_material_production_type",
        "component_material_release_type",
    ]

    # суммируем помесячные объемы quantity для каждой уникальной пары материал-компонент
    agg_df = df.groupby(group_cols, as_index=False, dropna=False).agg(
        {
            "produced_material_quantity": "sum",
            "component_material_quantity": "sum",
        }
    )

    return agg_df


def explode_bom_hierarchy(agg_df: pd.DataFrame) -> pd.DataFrame:
    """Строит дерево производственной цепочки от FIN_material до конечных компонентов"""
    results = []

    # обрабатываем каждый завод и год отдельно
    for (plant, year), group in agg_df.groupby(["plant_id", "year"]):
        # находим все FIN-материалы этого завода и этого года
        fin_rows = group[group["produced_material_release_type"] == "FIN"]

        prod_components = {}  # словарь где хранится:  PROD -> список его компонентов
        for _, row in group[
            group["produced_material_release_type"] == "PROD"
        ].iterrows():
            parent = row["produced_material"]
            if parent not in prod_components:
                prod_components[parent] = []
            prod_components[parent].append(row)

        # разворачиваем иерархию для каждого FIN
        for _, fin_row in fin_rows.iterrows():
            fin_id = fin_row["produced_material"]
            fin_rel = fin_row["produced_material_release_type"]
            fin_prod_type = fin_row["produced_material_production_type"]
            fin_qty = fin_row["produced_material_quantity"]

            start_prod_id = fin_row["component_material"]

            def traverse(current_prod_id):
                """рекурсивный обход производственного дерева"""
                # проверяем на тупик в нашем словарике где: PROD -> список его компонентов (проверяем есть ли еще подкомпоненты)
                if current_prod_id not in prod_components:
                    return

                for comp_row in prod_components[current_prod_id]:
                    # Добавляем запись в итоговую структуру
                    results.append(
                        {
                            "plant": plant,
                            "fin_material_id": fin_id,
                            "fin_material_release_type": fin_rel,
                            "fin_material_production_type": fin_prod_type,
                            "fin_production_quantity": fin_qty,
                            "prod_material_id": comp_row["produced_material"],
                            "prod_material_release_type": comp_row[
                                "produced_material_release_type"
                            ],
                            "prod_material_production_type": comp_row[
                                "produced_material_production_type"
                            ],
                            "prod_material_production_quantity": comp_row[
                                "produced_material_quantity"
                            ],
                            "component_id": comp_row["component_material"],
                            "component_material_release_type": comp_row[
                                "component_material_release_type"
                            ],
                            "component_material_production_type": comp_row[
                                "component_material_production_type"
                            ],
                            "component_consumption_quantity": comp_row[
                                "component_material_quantity"
                            ],
                            "year": year,
                        }
                    )

                    # если компонент сам является PROD, идем глубже и снова вызываем функцию traverse
                    if comp_row["component_material_release_type"] == "PROD":
                        traverse(comp_row["component_material"])

            traverse(start_prod_id)

    res_df = pd.DataFrame(results)

    # итоговый порядок столбцов в нижнем регистре
    final_cols = [
        "plant",
        "fin_material_id",
        "fin_material_release_type",
        "fin_material_production_type",
        "fin_production_quantity",
        "prod_material_id",
        "prod_material_release_type",
        "prod_material_production_type",
        "prod_material_production_quantity",
        "component_id",
        "component_material_release_type",
        "component_material_production_type",
        "component_consumption_quantity",
        "year",
    ]

    return res_df[final_cols]


file_path = "data/task_2_data_ex.xlsx"

agg_df = load_and_aggregate_bom(file_path)
final_bom_df = explode_bom_hierarchy(agg_df)

final_bom_df.to_excel("data/bom_result.xlsx", index=False)
logging.info("Успешно обработано. Итоговое количество строк: %s", len(final_bom_df))
