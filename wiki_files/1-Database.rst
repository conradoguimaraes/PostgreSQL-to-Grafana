Database
********

----

Database Parameters
...................

The database to be used will be the `PostgreSQL <https://db.fe.up.pt/phppgadmin/>`_. The main connection parameters:

+ database name
+ username
+ password
+ host ('db.fe.up.pt')
+ port (5432)


JSON File Format
................
The data that we want to store in this database has the JSON file format with the following structure:

```python
{
    "timeStart": 123.456,
    "timeEnd": 123.456,
    "environmentT": 123.456,
    "motorBearingT": 123.456,
    "spindleBearingT": 123.456,
    "counter": 1,
    "sdIntensity": 123.456,
    "times": [t0,t1,t2,...,tk],
    "angularVelocity": [a0,a1,a2,...,ak],
    "force": [fx0,f1,f2,..., fk],
    "displacement": [d0,d1,d2,...,dk]
}
```

|

Creating DB Table
.................

Considering each field corresponding to one column in the database table, the SQL statement (in python string format) below easly creates the table (*WELD_SAMPLES*) with the required columns and data types:


Standard Format
+++++++++++++++

```sql
CREATE TABLE IF NOT EXISTS "WELD_SAMPLES" ("id" serial, "time_start" float, "time_end" float, "environment_t" float, "motor_bearing_t" float, "spindle_bearing_t" float, "counter" int, "sdintensity" float, "times" float ARRAY, "angular_velocity" float ARRAY, "force" float ARRAY, "displacement" float ARRAY);
```

Python String Format
++++++++++++++++++++

```python
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
```


|

|

Insert JSON Sample Values
.........................

Therefore, to insert the JSON welding sample, the SQL statement would be:

Standard Format
+++++++++++++++

```sql
INSERT INTO "WELD_SAMPLES" (time_start, time_end, environment_t, motor_bearing_t, spindle_bearing_t, counter, sdintensity, times, angular_velocity, force, displacement) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
```

Python String Format
++++++++++++++++++++
  
```python
'INSERT INTO "WELD_SAMPLES" (\
    time_start, \
    time_end, \
    environment_t, \
    motor_bearing_t, \
    spindle_bearing_t, \
    counter, \
    sdintensity, \
    times, \
    angular_velocity, \
    force, \
    displacement\
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' 
```


|


DB Functions Code
.................

The following Code Example has functions to 

+ delete the DB Schema 
+ create the DataBase with the required table
+ create and return the connection handler
+ insert data (list)

```python
#%%
import traceback
import psycopg2
import time
#https://db.fe.up.pt/phppgadmin/


def deleteSchema(myUsername=None, myPassword=None):
    conn = psycopg2.connect(database=myUsername, 
                            user=myUsername, 
                            password=myPassword,
                            host='db.fe.up.pt',
                            port= '5432')
    cursor = conn.cursor()
    cursor.execute('DROP SCHEMA IF EXISTS "DINASORE" CASCADE')
    conn.commit()
    conn.close()
    return


def initDB(myUsername=None, myPassword=None):
    # Establishing the connection
    conn = psycopg2.connect(database=myUsername, 
                            user=myUsername, 
                            password=myPassword,
                            host='db.fe.up.pt',
                            port= '5432')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Executing an SQL function using the execute() method
    cursor.execute("select version()")
    
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print("Connection established to: ",data)

    #Create DINASORE Schema
    cursor.execute('CREATE SCHEMA IF NOT EXISTS "DINASORE"')

    #Setting the path to DINASORE
    cursor.execute('SET search_path TO "DINASORE"')
    
    
    #Creating Arrays in PostgreSQL: https://www.postgresql.org/docs/current/arrays.html
    #Other strategies: 
    #https://www.postgresql.org/docs/current/datatype-json.html
    #https://www.blendo.co/blog/storing-json-in-postgresql/
    

    
    #OBS: Camel Case may cause errors
    #example:
    #psycopg2.errors.UndefinedColumn: column "timestart" of relation "WELD_SAMPLES" does not exist
    #LINE 1: INSERT INTO "WELD_SAMPLES" (            timeStart,          ...
    
    
    
    #Sample example:
    # {
    #     "timeStart": 1643885832.053,
    #     "timeEnd": 1643885839.0434105,
    #     "environmentT": 316.10670037633975,
    #     "motorBearingT": 316.7429856634482,
    #     "spindleBearingT": 340.6813214621365,
    #     "counter": 1,
    #     "sdIntensity": 1.4685540517262314,
    #     "times": [t0,t1,t2,...],
    #     "angularVelocity": [a0,a1,a2...],
    #     "force": [fx0, f1, f2, ...],
    #     "displacement": [d0,d1,d2,...]
    # }
    
    cursor.execute(
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
           "force" float ARRAY, \
           "displacement" float ARRAY\
        )'
    )


    conn.commit()

    #Closing the connection
    conn.close()
   
    return




def getConnectionDB(myUsername=None, myPassword=None):
    conn = psycopg2.connect(database=myUsername, 
                            user=myUsername, 
                            password=myPassword,
                            host='db.fe.up.pt',
                            port= '5432')
    return conn


def insertDataV3(myUsername=None, myPassword=None, connection=None, statement = None, data = None):
    #Inputs:
    #    connection (such as connection = getConnectionDB())
    #    statement [STR]: statement sql
    #    data [LIST]: list with values to be saved
    try:
        delay = 0.050
        #-------------------------------------------------------
        for k in range(20):
            #Sometimes, postgres will give psycopg2.OperationalError
            #To avoid losing data and return without saving anything,
            #we try to save the data 20 times. 
            #Whenever the error occurs, we wait some time and
            #try to close the current connection in order to re-connect.
            try:
                print("Trying...(%d)" % k)
                cursor = connection.cursor()
                cursor.execute('SET search_path TO "DINASORE"')
                cursor.execute(statement, data)
            
                connection.commit()
                print("Success.\n")
                return k
            except:
                #print(traceback.format_exc())
                
                time.sleep(delay)
                try:
                    connection.close()
                    connection = getConnectionDB(myUsername=myUsername,
                                                 myPassword=password)
                except:
                    connection = getConnectionDB(myUsername=myUsername,
                                                 myPassword=myPassword)
        
        return -1
    except:
        print(traceback.format_exc())
    
        return -1
```