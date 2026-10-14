WITH RECURSIVE annual_bom AS (
    -- агрегируем помесячные данные из таблицы до годового уровня (plant, year)
    -- суммируем помесячные объемы quantity для каждой уникальной пары материал-компонент
    SELECT 
        plant_id AS plant,
        year,
        produced_material,
        produced_material_production_type,
        produced_material_release_type,
        SUM(produced_material_quantity) AS produced_material_quantity,
        component_material,
        component_material_production_type,
        component_material_release_type,
        SUM(component_material_quantity) AS component_material_quantity
    FROM task
    GROUP BY 
        plant_id,
        year,
        produced_material,
        produced_material_production_type,
        produced_material_release_type,
        component_material,
        component_material_production_type,
        component_material_release_type
),
fin_starting_point AS (
    -- находим все FIN. каждый FIN связан со своим стартовым PROD
    SELECT 
        plant,
        year,
        produced_material AS fin_material_id,
        produced_material_release_type AS fin_material_release_type,
        produced_material_production_type AS fin_material_production_type,
        produced_material_quantity AS fin_production_quantity,
        component_material AS root_prod_id
    FROM annual_bom
    WHERE produced_material_release_type = 'FIN'
),
bom_recursion AS (
    -- базовая часть рекурсии:
    -- соединяем FIN с первым уровнем его PROD.
    SELECT 
        f.plant,
        f.fin_material_id,
        f.fin_material_release_type,
        f.fin_material_production_type,
        f.fin_production_quantity,
        b.produced_material AS prod_material_id,
        b.produced_material_release_type AS prod_material_release_type,
        b.produced_material_production_type AS prod_material_production_type,
        b.produced_material_quantity AS prod_material_production_quantity,
        b.component_material AS component_id,
        b.component_material_release_type,
        b.component_material_production_type,
        b.component_material_quantity AS component_consumption_quantity,
        f.year
    FROM fin_starting_point f
    INNER JOIN annual_bom b 
        ON f.plant = b.plant 
       AND f.year = b.year 
       AND f.root_prod_id = b.produced_material
    WHERE b.produced_material_release_type = 'PROD'

    UNION ALL

    -- рекурсивная часть:
    -- прослеживаем PROD вглубь дерева
    SELECT 
        r.plant,
        r.fin_material_id,
        r.fin_material_release_type,
        r.fin_material_production_type,
        r.fin_production_quantity,
        b.produced_material AS prod_material_id,
        b.produced_material_release_type AS prod_material_release_type,
        b.produced_material_production_type AS prod_material_production_type,
        b.produced_material_quantity AS prod_material_production_quantity,
        b.component_material AS component_id,
        b.component_material_release_type,
        b.component_material_production_type,
        b.component_material_quantity AS component_consumption_quantity,
        r.year
    FROM bom_recursion r
    INNER JOIN annual_bom b 
        ON r.plant = b.plant 
       AND r.year = b.year 
       AND r.component_id = b.produced_material
    WHERE r.component_material_release_type = 'PROD'
)

-- финальная выборка 
SELECT 
    plant,
    fin_material_id,
    fin_material_release_type,
    fin_material_production_type,
    fin_production_quantity,
    prod_material_id,
    prod_material_release_type,
    prod_material_production_type,
    prod_material_production_quantity,
    component_id,
    component_material_release_type,
    component_material_production_type,
    component_consumption_quantity,
    year
FROM bom_recursion
ORDER BY 
    plant,
    year,
    fin_material_id,
    prod_material_production_type DESC;

