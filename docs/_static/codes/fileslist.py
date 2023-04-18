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