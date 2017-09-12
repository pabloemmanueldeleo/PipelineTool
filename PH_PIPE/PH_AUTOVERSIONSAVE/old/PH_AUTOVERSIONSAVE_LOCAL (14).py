import maya.cmds as mc
import os
import os.path
import re
import shutil
import sys
import getpass
import time
import datetime
#PH_AUTOVERSIONSAVE LOCAL
version="1.0"

def versionLocal(nC):
    nCM = nC.upper()
    cP  = ['0','1','2','3','4','5','6','7','8','9']
    nCL = ''
    #si esta bien nombrado, guardo sin sobreescribir. si existe subo versionado
    if '_V' in nCM:
        if nCM[-4] in cP:
            if nCM[-5] in cP:
                if nCM[-6] in cP:
                    if nCM[-7] == 'V':
                        if nCM[-8] == '_':
                            vA = int (nC[-6:-3])
                            archs = mc.getFileList( folder=os.path.split("D"+nCompleto[1:])[0] +"/", filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
                            archsO = []
                            if archs!= None:
                                for arch in archs:
                                    if ('_V' in arch or '_v' in arch ) and arch[-4] in cP and arch[-5] in cP and arch[-6] in cP  and arch[-8] == '_':
                                        archsO.append (int(arch[-6:-3]))
                                        archsO.sort()
                            if archsO == []:
                                vL = (str(vA)).zfill(3)
                            else:
                                vL = str(archsO[-1]+1).zfill(3)
                            nCL = 'D'+nC[1:-7]+'V'+vL+'.ma'
    return nCL # Devuelve version local posible. Si el archivo esta mal nombrado, devuelve ''.

def ventanaSaveUI():
    global nCompletoLocal
    global nCompleto
    global archivosExistentes
    global archivosExistentesStr

    if mc.window('PH_AUTOVERSIONSAVE',exists=True):
        mc.deleteUI('PH_AUTOVERSIONSAVE')
    winCrear1=mc.window('PH_AUTOVERSIONSAVE', title='PH_AUTOVERSIONSAVE LOCAL', widthHeight=[642, 183],backgroundColor=[1,0.4,0.06],titleBarMenu=1,toolbox=1,resizeToFitChildren=1,s=0 )
    layoutRC_1 = mc.rowColumnLayout ( numberOfRows=1 , rowSpacing= [50,50] ,noBackground=0 )

    layoutC_1 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.6,0.7,1] )
    archivosExistentes = mc.getFileList( folder= "D"+os.path.split(nCompleto)[0][1:] +"/", filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
    archivosExistentesStr=[]
    for arch in archivosExistentes:
        archivosExistentesStr.append ( arch.upper() )
    archivosExistentesStr.sort ()
    archivoConflictivo = "D"+ os.path.split(nCompleto)[0][1:] + "/" + archivosExistentesStr[-1]
    archivoConflictivoDate = time.ctime (os.path.getmtime( archivoConflictivo)  )
    nCompletoDate =          time.ctime (os.path.getmtime(nCompleto) )
    mc.text (label="\nABRIR ARCHIVO EXISTENTE EN UNIDAD D:\n\n"+ "VERSION ACTUAL (ULTIMA MOD):\n"+ os.path.split(nCompleto)[1]+"\n"+ nCompletoDate+"\n\n"+ "VERSION ENCONTRADA (ULTIMA MOD):\n"+archivosExistentesStr[-1] +"\n"+ archivoConflictivoDate +"\n\n " )
    mc.button( label= "ABRIR ARCHIVO" , backgroundColor=[0.79,0.74,0.12], command='PH_AUTOVERSIONSAVE_LOCAL.abrirVersionLocal()')

    mc.separator(horizontal=0,height=15, p=layoutRC_1)

    layoutC_2 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.9,0.44,0.42])
    mc.text (label="\nGUARDAR COMO ULTIMA VERSION \nSIN SOBREESCRIBIR. \nSE INCREMENTA UNO A LA \nULTIMA VERSION ENCONTRADA\nGUARDAR COMO:\n  " + os.path.split(nCompletoLocal)[1] +"\n\n\n\n\n")
    mc.button( label= "VERSIONAR", backgroundColor=[0.79,0.74,0.12], align = "center" , command='PH_AUTOVERSIONSAVE_LOCAL.guardarLocalUltimoMasUno()')

    mc.separator(horizontal=0,height=15, p=layoutRC_1)

    layoutC_3 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.4,1,0.4] )
    mc.text (label="\nO PODES VER LA CARPETA EN UNIDAD D:\n\n\n\n\n\n\n\n\n\n  ")
    mc.button( label='ABRIR',  backgroundColor=[0.79,0.74,0.12],align='center',command='PH_AUTOVERSIONSAVE_LOCAL.abrirCarpetaLocal()')

    anchoDeVentana = mc.columnLayout ( layoutC_1 , q = 1 , w = 1 ) + mc.columnLayout ( layoutC_2 , q = 1 , w = 1 ) + mc.columnLayout ( layoutC_3 , q = 1 , w = 1 )
    altoDeVentana = mc.rowColumnLayout ( layoutRC_1 , q = 1 , h = 1 )
    mc.window( winCrear1 , e = 1 , w = anchoDeVentana , h = altoDeVentana )

    mc.showWindow( winCrear1 )

def abrirVersionLocal():
    mc.warning ("ABRIENDO ARCHIVO")
    mc.file (os.path.split(nCompletoLocal)[0] + "/" + archivosExistentesStr[-1] , o = 1 , force = 1)
    mc.deleteUI('PH_AUTOVERSIONSAVE')

def guardarLocalUltimoMasUno():
    global nCompletoLocal
    mc.warning ("SE VERSIONA EN LOCAL")
    mc.file(rename=nCompletoLocal    )
    mc.file(f=True, save=True, defaultExtensions=True)
    mc.deleteUI('PH_AUTOVERSIONSAVE')

def abrirCarpetaLocal():
    global nCompletoLocal
    global nCompleto
    mc.warning ("ABRIR CARPETA LOCAL")
    os.system ("explorer/n," + ("D"+os.path.split(nCompleto)[0][1:]).replace("/","\\")   )

####################################################################

global nCompleto
global nCompletoLocal
global carpetasPermitidas

def autoversionlocal():
    global nCompleto
    global nCompletoLocal
    global carpetasPermitidas
    nCompleto = mc.file(query=True,sceneName=True)
    nCompletoLocal = versionLocal(nCompleto)

    #guarda disco local
    usuario=getpass.getuser()

    carpetasPermitidas = ["M:/MAYA","Q:/MAYA","D:/MAYA","M:/PH_SCRIPTS"]

    if not len(nCompleto)==0:
        rutasplit = nCompleto.split ("/")[:2]
        rutajuntaAMEO = rutasplit[0]+"/"+rutasplit[1]

    creaCarpeta=mc.sysFile ( "D"+os.path.split(nCompleto)[0][1:], makeDir=True )

    if nCompleto!="":
        bienNombrado = (nCompleto[-7]=="V" or nCompleto[-7]=="v") and nCompleto[-6:-3].isdigit() == True

    if nCompleto!="":
        if (rutajuntaAMEO in carpetasPermitidas) and nCompleto!="" and creaCarpeta:

            if bienNombrado:
                cP  = ['0','1','2','3','4','5','6','7','8','9']
                vA = int (nCompleto[-6:-3])
                archs = mc.getFileList( folder= "D"+os.path.split(nCompleto)[0][1:]+"/", filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
                archsO = []
                if archs!= None:
                    for arch in archs:
                        if arch[-4] in cP and arch[-5] in cP and arch[-6] in cP and (arch[-7] == 'V' or arch[-7] == 'v' ) and arch[-8] == '_':
                            archsO.append (int(arch[-6:-3]))
                    archsO.sort()
            else:
                archsO=[]

            # existe una copia local de M a D
            if len (archsO)!= 0:
                if nCompletoLocal != '' and nCompletoLocal[1:] != nCompleto[1:] and vA <= archsO[-1]  and nCompleto[0]=="M" :
                    mensajeCopiaEncontrada='SE HA ENCONTRADO ARCHIVO/S EN D:'
                    mc.warning (mensajeCopiaEncontrada)
                    ventanaSaveUI()

            # el archivo esta mal nombrado
            if nCompletoLocal == '' and nCompleto!="" and not (bienNombrado):
                mc.file(rename='D'+nCompleto[1:-3] +'_V001.ma')
                mc.file(f=True, save=True, defaultExtensions=True)
                mc.headsUpMessage ('COMO TU ARCHIVO ESTABA MAL NOMBRADO SE AGREGO "_V001" AL FINAL.',verticalOffset=-320)

            # se guarda normalmente de M a Local
            if nCompleto[1:].upper() >= nCompletoLocal[1:].upper() and nCompleto!="" and  bienNombrado :
                mensajeNormalM2Local = 'DE M: A LOCAL CON EXITO: ' + os.path.split(nCompleto)[1]
                mc.file(rename="D"+nCompleto[1:])
                mc.file(f=True, save=True, defaultExtensions=True)
                mc.headsUpMessage ( mensajeNormalM2Local ,verticalOffset=-320)
                mc.warning (mensajeNormalM2Local)

            # guarda incremental en local
            if bienNombrado:
                if nCompleto!="" and int ( (os.path.split(nCompletoLocal)[1])[-6:-3] ) -  int ( (os.path.split(nCompleto)[1])[-6:-3] )>=1 and vA >= archsO[-1]:
                    if nCompleto[0]== "D" and nCompleto[1:]!=nCompletoLocal[1:]:
                        mensajeIncrementalOK='SE GUARDO INCREMENTAL ' + str( os.path.split(nCompletoLocal)[1])+ ' CON EXITO.'
                        mc.file(rename=nCompletoLocal)
                        mc.file(f=True, save=True, defaultExtensions=True)
                        mc.headsUpMessage (mensajeIncrementalOK,verticalOffset=-320)
                        mc.warning (mensajeIncrementalOK)

        else:
            mensajeElse = "NO ESTAS EN UNA CARPETA EN LA QUE PUEDAS USAR ESTE SCRIPT."
            print mensajeElse
            mc.confirmDialog( title='OJO!', message=mensajeElse, button=['OK'], backgroundColor=[1,0.4,0.06], dismissString='OK' )
    else:
        mc.warning ("ESCENA NO VALIDA")
