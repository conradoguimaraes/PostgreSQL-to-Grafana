Reading JSON Files
******************

----

If we have one subfolder with JSON sample files (e.g., :code:`mysamples\\weld_sample01.json`), it is desirable to read their content.

The main steps to read the JSON sample files:




(1)Create Files List
....................
        
Convert the subfolder (e.g., :code:`mysamples`) files into a Python List, which will be useful to iterate over them.
    
List example: mySampleFiles = ['weld_sample01.json', 'weld_sample02.json', 'weld_sample03.json', ..., 'weld_samplexy.json']

Code example:
        
```python
import os
import re #required for the sorting

def getJSONfilesList(subfolderName = "samples"):
    
    filesFolder = os.path.join(os.getcwd(), subfolderName)
    filesList = sorted(os.listdir(filesFolder))

    sortAlphanum = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
    
    #Natural Sort:
    #['weld_0.json', 'weld_1.json', 'weld_10.json', 'weld_100.json', ..., 'weld_2.json', ...]
    #to
    ##['weld_0.json', 'weld_1.json', 'weld_2.json', 'weld_3.json', ..., 'weld_10.json', ..., 'weld_100.json']
    
    filesList = sorted(filesList, key=sortAlphanum)
    
    return filesList


filesList = getJSONfilesList()
```
  
  
(2)Create File Path
...................
        
Join the Current Working Directory, with the subfolder and with the JSON filename

Example:
        
:code:`filePath = C:\\Users\\Admin\\Dinasore\\mysamples\\weld_sample01.json`
            
:code:`filePath = C:\\Users\\Admin\\Dinasore\\mysamples\\weld_sample02.json`
            
...
            
:code:`filePath = C:\\Users\\Admin\\Dinasore\\mysamples\\weld_samplexy.json`
            
        

Code Example:
        
```python
subfolder = "samples"
filename = "weld_sample01.json"
filePath = os.path.join(os.getcwd(), "samples", filename)
```
               
Other methods also work.


(3)Read JSON File
.................

Considering a List of JSON Files inside the "samples" subfolder:
        
+ Iterate over the JSON files
+ Create FilePath for the current file in the current iteration
+ Open the file
+ Load the JSON data (returns dictionary data type)
+ Extract the desired dictionary fields and append them to a dataList
        
The conversion from dictionary to list is useful since it complies with the SQL Statement considered previously.
        
Code Example:
        
```python
import json

#Get the Files in List Format:
filesList = getJSONfilesList()

#Iterate over the sample files:
for file in filesList:
    #Create FilePath
    filePath = os.path.join(os.getcwd(), "samples", file)
    
    with open(filePath, 'r') as jsonFile:
        #Load the File contents
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
            fileData["force"]
        ]
```
        

With the :code:`fileData` (dictionary Data Type) having the structure:
        
```python
fileData = {
	'timeStart': 123.456,
	 'timeEnd': 123.456,
	 'environmentT': 123.456,
	 'motorBearingT': 123.456,
	 'spindleBearingT': 123.456,
	 'counter': 112,
	 'sdIntensity': 123.456,
	 'times': [t0, t1, t2, ...],
	 'angularVelocity': [a0, a1, a2, ...],
	 'force': [f0, f1, f2, ...],
	 'displacement': [d0, f1, f2, ...]
}
```
               

⚠️ Do not forget to import the json library.