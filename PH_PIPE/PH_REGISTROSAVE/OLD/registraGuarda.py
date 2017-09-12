import maya.cmds as cmds
import maya.mel as maya
import socket
import os.path
import sys
import datetime
import getpass
import json


def saveJSONFile(dataBlock, filePath):
    outputFile = open(filePath, 'w')
    JSONData = json.dumps(dataBlock, indent=4)
    outputFile.write(JSONData)
    outputFile.close()

def writeJSONFile(dataBlock, filePath):
    f = open(filePath, 'a')
    d = json.dumps(dataBlock, indent=4)
    f.write(d)
    f.close()

def registraGuarda():
    
    operadoresIP = {"169.254.1.6":"Gabi VFX","169.254.1.7":"Joaco","169.254.1.8":"Franco","169.254.1.11":"Diego","169.254.1.17":"Emma","169.254.1.18":"Pili","169.254.1.20":"Cesar","169.254.1.91":"Julian","169.254.1.92":"Gabo","169.254.1.30":"Nestor","169.254.1.96":"Fox"}
    nombrereg=cmds.date(format='DD-MM-YY')
    reg_fechaHora=cmds.date(format="DD/MM/YY  hh:mm")
    reg_operador = socket.gethostbyname(socket.gethostname() )
    reg_maya = cmds.file ( q=1,sn=1)
    registro = ("M:\\Documentos\\COORDINACION\\DATOS_USUARIOS\\"+nombrereg+".json")
	
    if reg_operador in operadoresIP:
        reg_operador = (operadoresIP[str(reg_operador)]+", IP: " + reg_operador)

    if ( cmds.file ( registro, q=1, exists=1) ):
        writeJSONFile(   {'Fecha y hora':reg_fechaHora,'Operador':reg_operador,'Archivo':reg_maya} , registro)
    else:
        saveJSONFile( {'Fecha y hora':reg_fechaHora,'Operador':reg_operador,'Archivo':reg_maya} , registro)    