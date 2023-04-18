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