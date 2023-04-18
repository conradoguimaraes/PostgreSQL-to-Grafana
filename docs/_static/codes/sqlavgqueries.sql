SELECT id AS "time", AVG(val) AS "AverageForce" FROM 
(SELECT id, UNNEST(force) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 5000;


SELECT id AS "time", AVG(val) AS "AverangeAngularVelocity" FROM 
(SELECT id, UNNEST(angular_velocity) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 5000;


SELECT id AS "time", AVG(val) AS "AverangeDisplacement" FROM 
(SELECT id, UNNEST(displacement) AS val FROM "DINASORE"."WELD_SAMPLES" ) 
subquery GROUP BY id ORDER BY id LIMIT 5000;