import maya.cmds as mc
import os
import os.path
import re
import shutil
import sys
import getpass
import time
# PH_AUTOVERSIONSAVE SERVER
#si no entra een ningun criterio le meto V001 al final
#checkear si esta en carpeta permitida
#fecha: 03/09
version="1.0"

global rutaM

def versionM(nC):
    global archsO
    nCM = nC.upper()
    cP  = ['0','1','2','3','4','5','6','7','8','9']
    nM = ''
    if '_V' in nCM:
        if nCM[-4] in cP:
            if nCM[-5] in cP:
                if nCM[-6] in cP:
                    if nCM[-7] == 'V':
                        if nCM[-8] == '_':
                            vA = int (nC[-6:-3])
                            archs = mc.getFileList( folder= rutaM, filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
                            archsO = []
                            if archs!= None:
                                for arch in archs:
                                    if arch[-4] in cP and arch[-5] in cP and arch[-6] in cP and (arch[-7] == 'V' or arch[-7] == 'v' ) and arch[-8] == '_':
                                        archsO.append (int(arch[-6:-3]))
                            archsO.sort()
                            if archsO == [] or mc.file(rutaM,query=True,ex=True)==False:
                                vM = (str(vA)).zfill(3)

                            else:
                                vM = str(archsO[-1]+1).zfill(3)
                            nM = os.path.split(nC)[1][:-7]+'V'+vM+'.ma'

    return nM  # devuelve '' si esta mal nombrado

def abrirCarpetaUI():
    global winCrear3
    global archivosExistentes
    global archivosExistentesMayus
    winCrear3='aa'
    if mc.window(winCrear3,exists=True):
        mc.deleteUI(winCrear3)
    mc.window(winCrear3, title='PH_AUTOVERSIONSAVE SERVER 1.0', backgroundColor=[1,0.4,0.06],wh=[644, 131], titleBarMenu=1,toolbox=1,resizeToFitChildren=1,s=0 )
    layoutRC_1 = mc.rowColumnLayout ( numberOfRows=1 , rowSpacing= [50,50] ,noBackground=0 )

    layoutC_1 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.6,0.7,1] )
    archivosExistentes = mc.getFileList( folder="M:/MAYA/"+ os.path.split(nCompleto.split("/MAYA/")[1])[0] , filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
    archivosExistentesStr=[]
    for arch in archivosExistentes:
        archivosExistentesStr.append ( str(arch) )
    archivosExistentesMayus = map ( str.upper , archivosExistentesStr )
    archivosExistentesMayus.sort ()

    archivoConflictivoServer= "M"+(os.path.split(nCompleto)[0] + "/" + archivosExistentesMayus[-1]) [1:]
    archivoConflictivoDateServer = time.ctime (os.path.getmtime(archivoConflictivoServer) )
    nCompletoDateServer = time.ctime (os.path.getmtime(nCompleto) )


    mc.text(label="\nABRIR ARCHIVO EXISTENTE EN UNIDAD M:\n\n"+"VERSION ACTUAL (ULTIMA MOD):\n"+os.path.split(nCompleto)[1]+"\n"+nCompletoDateServer+"\n\n"+ "VERSION ENCONTRADA (ULTIMA MOD):\n"+ archivosExistentesMayus[-1] + "\n\nQUERES ABRIR EL ARCHIVO?\n" ) #TIENE QUE MOSTRAR EL NOMBRE DEL ARCHIVO QUE SE ABRIRIA
    mc.button( label= "ABRIR ARCHIVO" , backgroundColor=[0.79,0.74,0.12], command='PH_AUTOVERSIONSAVE_SERVER.abrirVersionM()')

    mc.separator(horizontal=0,height=15, p=layoutRC_1)

    layoutC_2 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.9,0.24,0.02])
    mc.text (label="\nCOPIAR COMO ULTIMA VERSION \nSIN SOBREESCRIBIR. \nSE INCREMENTA UNO A LA \nULTIMA VERSION ENCONTRADA\nCOPIAR COMO:\n  " +os.path.split(nCompletoM)[1] +"\n\n\n\n\n")
    mc.button( label= "VERSIONAR", backgroundColor=[0.79,0.74,0.12], align = "center" , command='PH_AUTOVERSIONSAVE_SERVER.copiarM()')

    mc.separator(horizontal=0,height=15, p=layoutRC_1)

    layoutC_3 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.4,1,0.4] )
    mc.text (label="\nO PODES VER LA CARPETA EN UNIDAD M:\n\n\n\n\n\n\n\n\n\n  ")
    mc.button( label='ABRIR',  backgroundColor=[0.79,0.74,0.12],align='center',command='PH_AUTOVERSIONSAVE_SERVER.abrirCarpetaM()'  )

    mc.showWindow( winCrear3 )

def abrirVersionM():
    mc.file ( "M:/MAYA/"+ os.path.split(nCompleto.split("/MAYA/")[1])[0] + "/" + archivosExistentesMayus[-1] , o = 1 , force = 1)
    mc.warning ("ABRIENDO ARCHIVO")
    mc.deleteUI(winCrear3)

def copiarM():
    global winCrear3
    global nCompletoM
    mc.sysFile (nCompleto,copy=rutaM+"/"+nCompletoM)
    mc.warning ("COPIANDO COMO ULTIMA VERSION")
    mc.deleteUI(winCrear3)

def abrirCarpetaM():
    global winCrear3
    global nCompleto
    os.system ("explorer/n," + rutaM.replace("/","\\")   )
    mc.warning ("ABRIENDO CARPETA")

####################################################################

global nCompleto
global nCompletoM
global carpetasPermitidas

nCompleto = mc.file(query=True,sceneName=True)
if nCompleto != "" and "/MAYA/" in nCompleto:
    rutaM = "M:/MAYA/"+ os.path.split(nCompleto.split("/MAYA/")[1])[0]
    rutaArchivoM = "M:/MAYA/"+ os.path.split(nCompleto.split("/MAYA/")[1])[0] + "/" + os.path.split(nCompleto)[1]
    existeCarpeta = mc.file(rutaM ,query=True,ex=True)==True
else:
    rutaM = ""
    rutaArchivoM = ""
    existeCarpeta = False

nCompletoM = versionM(nCompleto)
usuarioServer=getpass.getuser()

carpetasPermitidas = ["Q:/MAYA","D:/MAYA","C:/MAYA","K:/MAYA","C:/Users/"+usuarioServer]

if (nCompleto[:7] in carpetasPermitidas[0] or nCompleto[:7] in carpetasPermitidas[1] or nCompleto[:7] in carpetasPermitidas[2] or nCompleto[:7] in carpetasPermitidas[3] or carpetasPermitidas[4] in nCompleto)and existeCarpeta and nCompleto[:7] != "M:/MAYA" :
    #existe una copia M
    cP  = ['0','1','2','3','4','5','6','7','8','9']
    vA = int (nCompleto[-6:-3])
    archs = mc.getFileList( folder= rutaM, filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
    archsO = []
    if archs!= None:
        for arch in archs:
            if arch[-4] in cP and arch[-5] in cP and arch[-6] in cP and (arch[-7] == 'V' or arch[-7] == 'v' ) and arch[-8] == '_':
                archsO.append (int(arch[-6:-3]))
        archsO.sort()

    if len(archsO)!=0 and (mc.file(rutaArchivoM,query=True,ex=True)==True or vA <= archsO[-1]):
        if nCompletoM != '' and nCompletoM[1:] != nCompleto[1:] and nCompleto[0]!="M" and  vA - archsO[-1]  < 1 :
            mensajeYaExiste = 'YA EXISTE EL MISMO ARCHIVO.'
            print mensajeYaExiste
            mc.warning (mensajeYaExiste)
            abrirCarpetaUI()

    # el archivo esta mal nombrado

    if nCompletoM == '' and nCompleto!="":
        mensajeMalNombrado='COMO TU ARCHIVO ESTABA MAL NOMBRADO SE AGREGO "_V001" AL FINAL. '
        mc.sysFile (nCompleto,copy=rutaArchivoM +'_V001.ma')
        mc.warning(mensajeMalNombrado)

    # SE COPIA AL M NORMALMENTE

    if len(archsO)!=0 and nCompleto!="" and vA-archsO[-1]>=1:
        mensajeNormalM2Local="SE GUARDA Y COPIA AL SERVER."
        mc.warning (mensajeNormalM2Local)
        mc.file(f=True, save=True, defaultExtensions=True)
        mc.sysFile (nCompleto,copy=rutaArchivoM)

    if os.path.split(nCompleto)[1].upper() == nCompletoM.upper() and nCompleto!="" and len(archsO)==0:
        mensajeNormalM2Local="SE GUARDA Y COPIA AL SERVER."
        mc.warning (mensajeNormalM2Local)
        mc.file(f=True, save=True, defaultExtensions=True)
        mc.sysFile (nCompleto,copy=rutaArchivoM)

elif existeCarpeta and nCompleto[:7] == "M:/MAYA":
    mensajeEstasEnM="-ERROR- ESTE SCRIPT SOLO FUNCIONA SI ESTAS EN LA UNIDAD D: LOCAL.\n\nCONDICIONES:\n1-USAR EL SCRIPT LOCAL PARA TRABAJAR EN UNIDAD D:."
    mc.warning (mensajeEstasEnM)
    mc.confirmDialog( title='PH_AUTOVERSIONSAVE', message=mensajeEstasEnM, button=['OK'], backgroundColor=[1,0.4,0.06], dismissString='OK' )

else:
    mensajeElseServer='-ERROR-: ESTE SCRIPT FUNCIONA SOLO PARA COPIAR DE LOCAL AL SERVER.\n\nCONDICIONES: \n1- ESTAR EN LA UNIDAD LOCAL D:.\n2- TENER LA MISMA ESTRUCTURA QUE EL SERVIDOR UNIDAD M:.\n'
    mc.warning (mensajeElseServer)
    mc.confirmDialog( title='USO DEL PH_AUTOVERSIONSAVE', message = mensajeElseServer , button=['OK'], backgroundColor=[1,0.4,0.06], dismissString='OK' )
