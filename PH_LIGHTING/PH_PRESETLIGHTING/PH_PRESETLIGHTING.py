import os.path
import sys
import datetime
#libreria para saber el username de la pc
import getpass
import json


def ld_listFiles(path,saveFilePath,namefile):
    fileString='\n'.join(sorted(os.listdir(path)))
    d=datetime.date.today()
    date=d.isoformat()
    filePath=saveFilePath+namefile+date+'.ema'
    thefile=open(filePath,'w')
    thefile.write(fileString)
    thefile.close()
    return fileString
#funcion para guardar cualquier archivo de json
def saveJSONFile(dataBlock, filePath):
    outputFile = open(filePath, 'w')
    JSONData = json.dumps(dataBlock, sort_keys=True, indent=4)
    outputFile.write(JSONData)
    outputFile.close()

#funcion para leer cualquier archivo de json
def loadJSONFile(filePath):
	inputFile = open(filePath, 'r')
	JSONData = json.load(inputFile)
	print '<<file was loaded position>>'
	inputFile.close()
	return JSONData

#funcion solo para leer datos de archivo con json
def writeJSONFile(dataBlock, filePath):
	# append in file
	f = open(filePath, 'a')
	d = json.dumps(dataBlock, sort_keys=True, indent=4)
	f.write(d)
	f.close()

username=getpass.getuser()
#dato para guardar
dataBlock = {'NONE' : [0, 0, 0, 0, 0, 0]}
#path='C:/Users/'+username+'/Downloads/'
saveFilePath='C:/Users/'+username+'/Desktop/'
namefile='emma.ema'


saveJSONFile(dataBlock,saveFilePath+namefile)

#ld_listFiles(path,saveFilePath,namefile)
