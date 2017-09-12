import maya.cmds as mc
import os
import re
import shutil
import sys
import getpass
#el versionado que importa es el utlimo
#si no entra een ningun criterio le meto V001 al final
#checkear si esta en carpeta permitida
#fecha: 09/09
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
    if mc.window('PH_AUTOVERSIONSAVE',exists=True):
        mc.deleteUI('PH_AUTOVERSIONSAVE')
    winCrear=mc.window('PH_AUTOVERSIONSAVE', title='PH_AUTOVERSIONSAVE '+version, resizeToFitChildren=True,s=1 )
    mc.columnLayout(columnOffset=['both',10])
    mc.text ( label= ('Se ha encontrado un archivo con el mismo nombre en la carpeta local: '+os.path.split("D"+nCompleto[1:])[1]))
    mc.text ( label= 'No se lo sobreescribira. Quieres abrir la carpeta para revisarlo? Quieres guardar como una version mas reciente?' )
    mc.text ( label= ('El archivo se guardarIa como: '+str(os.path.split(nCompletoLocal)[1])) )
    mc.rowLayout (nc=2,columnWidth2=[200, 200],columnAlign2=['left','right'])
    mc.button( label='Abrir carpeta', width=120, command='abrirCarpetaLocal()')
    mc.button( label=('Guardar version '+ nCompletoLocal[-7:-3]), width=120 , align='right' , command='guardarLocalUltimoMasUno()')
    mc.showWindow( winCrear )

def ventanaHD():

    usuario=getpass.getuser()

    dl='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    discoRigido='0'
    pedidoNro=0
    mensajeParaUsuario=''
    while discoRigido not in dl:
        if pedidoNro!=0:
            mensajeParaUsuario='Letra de unidad no vAlida.'

        hDrive = mc.promptDialog(
        		title='AUTOSAVE',
        		message= mensajeParaUsuario +'No tenEs disco D. Ingresa letra de la unidad que querEs usar:',
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


def guardarLocalUltimoMasUno():
    global nCompletoLocal
    mc.file(rename=nCompletoLocal)
    mc.file(f=True, save=True, defaultExtensions=True)
    mc.deleteUI('PH_AUTOVERSIONSAVE')

def abrirCarpetaLocal():
    global nCompletoLocal
    global nCompleto
    os.system ("explorer/n," + ("D"+os.path.split(nCompleto)[0][1:]).replace("/","\\")   )
    mc.deleteUI('PH_AUTOVERSIONSAVE')

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
    # existe una copia local
    if nCompletoLocal != '' and nCompletoLocal[1:] != nCompleto[1:] and nCompleto[0]=="M" and  mc.file("D"+nCompleto[1:],query=True,ex=True)==True :
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
    if nCompleto!="":
        if nCompleto[0]== discoLocal and nCompleto[1:]!=nCompletoLocal[1:]:
            mensajeIncrementalOK='SE GUARDO INCREMENTAL ' + str( os.path.split(nCompletoLocal)[1])+ ' CON EXITO.'
            mc.file(rename=discoLocal+nCompletoLocal[1:])
            mc.file(f=True, save=True, defaultExtensions=True)
            mc.headsUpMessage (mensajeIncrementalOK,verticalOffset=-320)
            mc.warning (mensajeIncrementalOK)
else:
    mensajeElse = "ESTE SCRIPT SOLO FUNCIONA CON ESTAS CONDICIONES:\n1- ESTAR EN LA UNIDAD LOCAL D:.\n2- TENER LA MISMA ESTRUCTURA QUE EL SERVIDOR UNIDAD M:."
    print mensajeElse
    mc.confirmDialog( title='OJO!', message=mensajeElse, button=['OK'], backgroundColor=[1,0.4,0.06], dismissString='OK' )
