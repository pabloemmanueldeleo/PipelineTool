import maya.cmds as mc
import os
import os.path
import re
import shutil
import sys
import getpass
import time
#el versionado que importa es el utlimo
#si no entra een ningun criterio le meto V001 al final
#checkear si esta en carpeta permitida
#fecha: 28/08
version="1.0"

print 'PH_AUTOVERSIONSAVE LOCAL '+version

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
                            archs = mc.getFileList( folder=os.path.split("D"+nCompleto[1:])[0] , filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
                            archsO = []
                            if archs!= None:
                                for arch in archs:
                                    if '_V' in arch and arch[-4] in cP and arch[-5] in cP and arch[-6] in cP and arch[-7] == 'V' and arch[-8] == '_':
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
    global archivosExistentesMayus

    if mc.window('PH_AUTOVERSIONSAVE',exists=True):
        mc.deleteUI('PH_AUTOVERSIONSAVE')
    winCrear1=mc.window('PH_AUTOVERSIONSAVE', title='PH_AUTOVERSIONSAVE LOCAL', widthHeight=[642, 131],backgroundColor=[1,0.4,0.06],titleBarMenu=1,toolbox=1,resizeToFitChildren=1,s=0 )
    layoutRC_1 = mc.rowColumnLayout ( numberOfRows=1 , rowSpacing= [50,50] ,noBackground=0 )

    layoutC_1 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.6,0.7,1] )
    archivosExistentes = mc.getFileList( folder= os.path.split(nCompleto)[0] , filespec = os.path.split(nCompleto)[1][:-7]+'*.m*' )
    archivosExistentesStr=[]
    for arch in archivosExistentes:
        archivosExistentesStr.append ( str(arch) )
    archivosExistentesMayus = map ( str.upper , archivosExistentesStr )
    archivosExistentesMayus.sort ()
    archivoConflictivo= os.path.split(nCompleto)[0] + "/" + archivosExistentesMayus[-1]
    archivoConflictivoDate = time.ctime (os.path.getmtime(archivoConflictivo) )
    nCompletoDate = time.ctime (os.path.getmtime(nCompleto) )
    mc.text (label="\nABRIR ARCHIVO EXISTENTE EN UNIDAD D:\n\n"+ "VERSION ACTUAL (ULTIMA MOD):\n"+ os.path.split(nCompleto)[1]+"\n"+ nCompletoDate+"\n\n"+ "VERSION ENCONTRADA (ULTIMA MODIFICACION):\n"+archivosExistentesMayus[-1] +"\n"+ archivoConflictivoDate +"\n\n " )
    mc.button( label= "ABRIR ARCHIVO" , backgroundColor=[0.79,0.74,0.12], command=abrirVersionLocal)

    mc.separator(horizontal=0,height=15, p=layoutRC_1)

    layoutC_2 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.9,0.24,0.02])
    mc.text (label="\nCOPIAR COMO ULTIMA VERSION \nSIN SOBREESCRIBIR. \nSE INCREMENTA UNO A LA \nULTIMA VERSION ENCONTRADA\nCOPIAR COMO:\n  " +os.path.split(nCompletoLocal)[1] +"\n\n\n\n\n")
    mc.button( label= "VERSIONAR", backgroundColor=[0.79,0.74,0.12], align = "center" , command=guardarLocalUltimoMasUno)

    mc.separator(horizontal=0,height=15, p=layoutRC_1)

    layoutC_3 = mc.columnLayout ( adjustableColumn=1, p=layoutRC_1 , columnOffset= ["both",10] , backgroundColor= [0.4,1,0.4] )
    mc.text (label="\nO PODES VER LA CARPETA EN UNIDAD D:\n\n\n\n\n\n\n\n\n\n  ")
    mc.button( label='ABRIR',  backgroundColor=[0.79,0.74,0.12],align='center',command=abrirCarpetaLocal)

    mc.showWindow( winCrear1 )


def ventanaHD(arg):

    usuario=getpass.getuser()

    dl='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    discoRigido='0'
    pedidoNro=0
    mensajeParaUsuario=''
    while discoRigido not in dl:
        if pedidoNro!=0:
            mensajeParaUsuario='LETRA DE UNIDAD NO VALIDA.'

        hDrive = mc.promptDialog(
        		title='AUTOSAVE',
        		message= mensajeParaUsuario +'NO TENES DISCO D:. INGRESA LA LETRA DE LA UNIDAD QUE QUERES USAR.',
        		text='C',
        		button=['OK', 'Cancel'],
        		defaultButton='OK',
        		cancelButton='Cancel',
        		dismissString='Cancel')
        if hDrive == 'OK':
        	discoRigido = str( mc.promptDialog(query=True, text=True) ).upper()
        pedidoNro+=1

    drives=['%s'%d for d in dl if os.path.exists('%s:'%d) ]
    if discoRigido in drives:
        discoRigidoFile = open( ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/discoRigidoAutoSave.txt") ,"w")
        discoRigidoFile.write(discoRigido)
        discoRigidoFile.close()

def abrirVersionLocal(arg):
    mc.file ( "D:/MAYA/"+ os.path.split(nCompleto.split("/MAYA/")[1])[0] + "/" + archivosExistentesMayus[-1] , o = 1 , force = 1)
    mc.warning ("ABRIENDO ARCHIVO")
    mc.deleteUI('PH_AUTOVERSIONSAVE')

def guardarLocalUltimoMasUno(arg):
    global nCompletoLocal
    mc.file(rename=nCompletoLocal)
    mc.file(f=True, save=True, defaultExtensions=True)
    mc.deleteUI('PH_AUTOVERSIONSAVE')

def abrirCarpetaLocal(arg):
    global nCompletoLocal
    global nCompleto
    os.system ("explorer/n," + ("D"+os.path.split(nCompleto)[0][1:]).replace("/","\\")   )

####################################################################

global nCompleto
global nCompletoLocal


nCompleto = mc.file(query=True,sceneName=True)
nCompletoLocal = versionLocal(nCompleto)

#guarda disco local
usuario=getpass.getuser()
archivoDiscoLocalQ= "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/discoRigidoAutoSave.txt"
if mc.file(archivoDiscoLocalQ,query=True,ex=True)==False:
    ventanaHD()
discoLocalObj=open(archivoDiscoLocalQ,"r")
discoLocal=discoLocalObj.read()
discoLocalObj.close()

global carpetasPermitidas
carpetasPermitidas = ["M:/MAYA","Q:/MAYA","D:/MAYA"]
carpetasPermitidas.append(discoLocal+"://MAYA")
creaCarpeta=mc.sysFile ( discoLocal+os.path.split(nCompleto)[0][1:], makeDir=True )

if (nCompleto[:7] in carpetasPermitidas[0] or nCompleto[:7] in carpetasPermitidas[1] or nCompleto[:7] in carpetasPermitidas[2]) and nCompleto!="":
    # existe una copia local de M a D
    if nCompletoLocal != '' and nCompletoLocal[1:] != nCompleto[1:] and nCompleto[0]=="M" and  mc.file("D"+nCompleto[1:],query=True,ex=True)==True :
        mensajeCopiaEncontrada='SE HA ENCONTRADO ARCHIVO/S EN D:'
        mc.warning (mensajeCopiaEncontrada)
        ventanaSaveUI()

    # existe el versionado +1 local de D a D
    if nCompleto!="" and int ( (os.path.split(nCompletoLocal)[1])[-6:-3] ) -  int ( (os.path.split(nCompleto)[1])[-6:-3] )>1:
        if nCompleto[0]== "D" and nCompleto[1:]!=nCompletoLocal[1:]:
            mensajeIncrementalEncontrado='SE HA ENCONTRADO ARCHIVO/S EN D:'
            mc.warning (mensajeIncrementalEncontrado)
            ventanaSaveUI()

    # el archivo esta mal nombrado
    if nCompletoLocal == '' and nCompleto!="":
        mc.file(rename=discoLocal+nCompleto[1:-3] +'_V001.ma')
        mc.file(f=True, save=True, defaultExtensions=True)
        mc.headsUpMessage ('COMO TU ARCHIVO ESTABA MAL NOMBRADO SE AGREGO "_V001" AL FINAL.',verticalOffset=-320)

    # se guarda normalmente de M a Local
    if nCompleto[1:].upper() == nCompletoLocal[1:].upper() and nCompleto!="" :
        mensajeNormalM2Local = 'SE HA GUARDADO DE M: A LOCAL CON EXITO.'
        mc.file(rename=discoLocal+nCompletoLocal[1:])
        mc.file(f=True, save=True, defaultExtensions=True)
        mc.headsUpMessage ( mensajeNormalM2Local ,verticalOffset=-320)
        mc.warning (mensajeNormalM2Local)

    # guarda incremental en local
    if nCompleto!="" and int ( (os.path.split(nCompletoLocal)[1])[-6:-3] ) -  int ( (os.path.split(nCompleto)[1])[-6:-3] )==1:
        if nCompleto[0]== discoLocal and nCompleto[1:]!=nCompletoLocal[1:]:
            mensajeIncrementalOK='SE GUARDO INCREMENTAL ' + str( os.path.split(nCompletoLocal)[1])+ ' CON EXITO.'
            mc.file(rename=discoLocal+nCompletoLocal[1:])
            mc.file(f=True, save=True, defaultExtensions=True)
            mc.headsUpMessage (mensajeIncrementalOK,verticalOffset=-320)
            mc.warning (mensajeIncrementalOK)

else:
    mensajeElse = "NO ESTAS EN UNA CARPETA EN LA QUE PUEDAS USAR ESTE SCRIPT."
    print mensajeElse
    mc.confirmDialog( title='OJO!', message=mensajeElse, button=['OK'], backgroundColor=[1,0.4,0.06], dismissString='OK' )
