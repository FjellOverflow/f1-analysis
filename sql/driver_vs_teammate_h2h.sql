SELECT
    r.id AS race_id,
    r.year AS race_year,
    rr1.constructor_id,
    c.name AS constructor_name,
    rr1.driver_id,
    d1.abbreviation AS driver_abbr,
    d1.name AS driver_name,
    rr2.driver_id AS teammate_id,
    d2.abbreviation AS teammate_abbr,
    d2.name AS teammate_name,
    CASE
        WHEN
            rr1.position_number IS NOT NULL
            AND (
                rr2.position_number IS NULL
                OR rr1.position_number < rr2.position_number
            )
            THEN 'win'

        WHEN
            rr1.position_number IS NULL AND rr2.position_number IS NULL
            THEN 'draw'
        WHEN rr1.position_number = rr2.position_number THEN 'draw'

        WHEN
            rr1.position_number IS NULL AND rr2.position_number IS NOT NULL
            THEN 'loss'
        WHEN rr1.position_number > rr2.position_number THEN 'loss'
    END AS result
FROM race_result AS rr1
INNER JOIN race_result AS rr2
    ON
        rr1.race_id = rr2.race_id
        AND rr1.constructor_id = rr2.constructor_id
        AND rr1.driver_id != rr2.driver_id
INNER JOIN race AS r ON rr1.race_id = r.id
INNER JOIN constructor AS c ON rr1.constructor_id = c.id
INNER JOIN driver AS d1 ON rr1.driver_id = d1.id
INNER JOIN driver AS d2 ON rr2.driver_id = d2.id
