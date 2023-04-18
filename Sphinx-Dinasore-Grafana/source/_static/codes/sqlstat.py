'CREATE TABLE IF NOT EXISTS "WELD_SAMPLES" (\
           "id" serial, \
           "time_start" float, \
           "time_end" float, \
           "environment_t" float, \
           "motor_bearing_t" float, \
           "spindle_bearing_t" float, \
           "counter" int, \
           "sdintensity" float, \
           "times" float ARRAY, \
           "angular_velocity" float ARRAY, \
           "force" float ARRAY,\
           "displacement" float ARRAY\
)'