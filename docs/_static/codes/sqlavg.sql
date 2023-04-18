SELECT id AS "time", AVG(val) AS "AverageForce" FROM 
(SELECT id, UNNEST(force) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 50;