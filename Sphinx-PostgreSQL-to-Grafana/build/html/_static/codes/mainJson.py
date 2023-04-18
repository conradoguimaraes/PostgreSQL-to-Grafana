# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 00:40:46 2023

@author: Conrado
"""

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

