SELECT
    CAST(date_plantation AS DATE) AS planting_date,
    essence_latin AS species,
    COUNT(*) AS trees_planted
FROM {{ ref('stg_public_trees') }}
WHERE date_plantation IS NOT NULL AND essence_latin IS NOT NULL AND date(date_plantation) > "1900-01-01"
GROUP BY planting_date, species
ORDER BY planting_date, species