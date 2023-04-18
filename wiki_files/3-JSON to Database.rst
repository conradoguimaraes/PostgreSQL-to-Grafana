JSON to Database
****************

----


With the above ideas, the full example codes are:

(1) main.py
...........
        
Convert the subfolder (e.g., :code:`mysamples`) files into a Python List, which will be useful to iterate over them.
    
List example: mySampleFiles = ['weld_sample01.json', 'weld_sample02.json', 'weld_sample03.json', ..., 'weld_samplexy.json']
    
Code example:

```python
#%%
import os
import re
import json
import traceback
import dbFunctions


def getJSONfilesList(subfolderName = "mysamples"):
    
    filesFolder = os.path.join(os.getcwd(), subfolderName)
    filesList = sorted(os.listdir(filesFolder))

    sortAlphanum = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
    
    #Natural Sort:
    #['weld_0.json', 'weld_1.json', 'weld_10.json', 'weld_100.json', ..., 'weld_2.json', ...]
    #to
    ##['weld_0.json', 'weld_1.json', 'weld_2.json', 'weld_3.json', ..., 'weld_10.json', ..., 'weld_100.json']
    
    filesList = sorted(filesList, key=sortAlphanum)
    
    return filesList




dbUsername = "abcde"
dbPassword = "abcde1234"


try:
    dbFunctions.deleteSchema(myUsername = dbUsername,
                             myPassword = dbPassword)
    dbFunctions.initDB(myUsername = dbUsername,
                       myPassword = dbPassword)


    
    insertStatement = (   
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
    )
        
    
        
    filesList = getJSONfilesList()
    
    filesNotSaved = []
    filesWithReadingError = []
    
    DBconn = dbFunctions.getConnectionDB(myUsername = dbUsername,
                                         myPassword = dbPassword)
    #DBcursor = DBconn.cursor()
    #DBcursor.execute('SET search_path TO "DINASORE"')
    iters = 0
    
    #Iterate over the sample files:
    for file in filesList:
        try:
            filePath = os.path.join(os.getcwd(), "mysamples", file)
            rc = -2
            with open(filePath, 'r') as jsonFile:
                fileData = json.load(jsonFile)
                dataList = [
                    fileData["timeStart"],
                    fileData["timeEnd"],
                    fileData["environmentT"],
                    fileData["motorBearingT"],
                    fileData["spindleBearingT"],
                    fileData["counter"],
                    fileData["sdIntensity"],
                    fileData["times"],
                    fileData["angularVelocity"],
                    fileData["force"],
                    fileData["displacement"],
                ]

                rc = dbFunctions.insertDataV3(myUsername = dbUsername,
                                              myPassword = dbPassword,
                                              connection = DBconn,
                                              statement = insertStatement,
                                              data = dataList)
                
                if (rc >= 0):
                    print("%s saved to BD." % file)
                    if (rc > 0):
                        DBconn = dbFunctions.getConnectionDB(myUsername = dbUsername,
                                                             myPassword = dbPassword)
                else:
                    print("%s not saved to BD." % file)
                    filesNotSaved.append(file)
                    DBconn = dbFunctions.getConnectionDB(myUsername = dbUsername,
                                                         myPassword = dbPassword)

        except:
            print(traceback.format_exc())
            if (rc == -2):
                print("ERROR reading")
                filesWithReadingError.append(file)
            pass

        iters += 1
        # if (iters % 10 == 0):
        #     break

except:
    print(traceback.format_exc())


```
  
|
  
(2) dbFunctions
...............
        
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

  
|
  

Results
.......

.. image:: https://user-images.githubusercontent.com/98216516/232912923-95dfda28-5cbf-40b5-ae60-6371494a448b.PNG

 
        