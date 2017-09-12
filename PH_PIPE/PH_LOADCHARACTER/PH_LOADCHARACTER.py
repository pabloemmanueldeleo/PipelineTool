import maya.cmds as mc
import sys
import os
import errno

suffName = 'D:/PH_SCRIPTS/SCRIPTS/suffNodes.py'
global unidadDisco
global unidad
global scene
global char
global charsFolders
charsFolders = []
#namesCharacters=[]
nameWindow = 'fixUpdateCharacterAlembic'
if mc.window(nameWindow ,ex=True):
	mc.deleteUI(nameWindow)

mc.window(nameWindow, title="fixUpdateCharacterAlembic", sizeable=True, resizeToFitChildren=True)
form = mc.formLayout(numberOfDivisions=100)
cl1 = cmds.columnLayout(adjustableColumn = True)
mc.text(label='-INFORMACION NECESARIA-')
tfu=mc.textFieldGrp(nameWindow + 'UD', label='UNIDAD:', ann='Nombre de la unidad.')
tfe=mc.textFieldGrp(nameWindow + 'ESC', label='ESCENA:',ann='Nombre de la escena.')
l1=mc.checkBox(label='UV WRITW',value=True)
l2=mc.checkBox(label='FIT TIME RANGE',value=True)
l2=mc.checkBox(label='BLENDSHAPE TO ALEMBIC', value=True)
mc.text(label='-CHARACTERS-')
scrol = cmds.textScrollList( nameWindow + 'FOLDERS',
                     numberOfRows=5,
                     allowMultiSelection=True,
        			 append=charsFolders,
			         showIndexedItem=8 )
b1=mc.button(nameWindow + 'btn1', label="CREATE ABC", w=50, h=50, command="importChar()")
b2=mc.button(nameWindow + 'btn2',label='UPDATE SHADER', w=50, h=50, command='')
mc.showWindow(nameWindow)

#Ruta absoluta de carpeta donde estan todos los personajes
pathCharacters = 'M:/MAYA/01_CHAR'
#Leo los nombres de las carpetas y las guardo
charsFolders = os.listdir(pathCharacters)

listdir(pathRoot)

'''
#Separo lo nombres de las carpetas
for nF in charsFolders:
    nameFix = nF.split('_')[-1]
    namesCharacters.append(nameFix)
    print nameFix
'''

#Leo los archivos en la carpeta seleccionada con la funcion list_files
filesInFolder = list_files( pathCharacters + '/' +  charsFolders[selecStringChar])

#Trato de ver si hay un archivo que tenga '_SHD'
for fileShader in filesInFolder:
    if fileShader.split('_SHD'):
        thisFileToLoad = fileShader
    else:
        mc.warning('NO EXISTE ARCHIVO QUE CONTANGA _SHD')

def importChar():
    #Lista de la seleccion del scroll
    selObj = cmds.textScrollList(nameWindow + 'FOLDERS',q=True, si=True)
    unidad = mc.textFieldGrp(nameWindow + 'UD', q = True, text=True)
    scene = mc.textFieldGrp(nameWindow + 'ESC', q = True, text=True)
    char = mc.textFieldGrp(nameWindow + 'CHAR', q = True, text=True)
    loadCharactersScene(unidadDisco,unidad,scene,char)
    #makeAlembic()

def loadCharactersScene(unidadDisco,unidad,scene,char):
    unidadDisco= 'D:/'
    pathMaya= 'MAYA/05_SHOT/UD'
    pathEs= '/E'
    esChar = 'E'
    pathAnim= '/Anim_Wip/'

    if (char):
        #aqui estan los archivos de animacion para importar el rig o los rig UD16_E117_FINAL.ma
        pathLoadAni = unidadDisco + str(pathMaya) + str(unidad) + str(pathEs) + str(scene) + str(pathAnim)
        fileCharFinal = str( 'UD' + str(unidad) + str(esChar) + str(scene) + '_' + str(char) + '_FINAL.ma')
        pathFile = str(pathLoadAni + fileCharFinal)
        print 'RUTA Y ARCHIVO DE CARGA: ' + pathFile
    else:
        #aqui estan los archivos de animacion para exportar alembic UD16_E117_FINAL.ma
        pathLoadAni = unidadDisco + str(pathMaya) + str(unidad) + str(pathEs) + str(scene) + str(pathAnim)
        fileCharFinal = str( 'UD' + str(unidad) + '_' + str(esChar) + str(scene) + '_FINAL.ma')
        pathFile = str(pathLoadAni + fileCharFinal)
        print 'RUTA Y ARCHIVO DE CARGA: ' + pathFile

    if os.path.exists(pathFile):
        nFile = mc.file(pathFile, i=True)
    else:
        mc.warning('NO EXISTE EL EL ARCHIVO -> ' + fileCharFinal )

def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files

mc.window(nameWindow, title="fixUpdateCharacterAlembic", sizeable=False, resizeToFitChildren=True)
form = mc.formLayout(numberOfDivisions=100)
cl1 = cmds.columnLayout(adjustableColumn = True)
mc.text(label='-INFORMACION NECESARIA-')
tfu=mc.textFieldGrp(nameWindow + 'UD', label='UNIDAD:', ann='Nombre de la unidad.')
tfe=mc.textFieldGrp(nameWindow + 'ESC', label='ESCENA:',ann='Nombre de la escena.')
l1=mc.checkBox(label='UV WRITW',value=True)
l2=mc.checkBox(label='FIT TIME RANGE',value=True)
l2=mc.checkBox(label='BLENDSHAPE TO ALEMBIC', value=True)
mc.text(label='-CHARACTERS-')
scrol = cmds.textScrollList( nameWindow + 'FOLDERS',
                     numberOfRows=5,
                     allowMultiSelection=True,
        			 append=charsFolders,
			         selectItem=selecStringChar,
			         showIndexedItem=8 )
b1=mc.button(nameWindow + 'btn1', label="CREATE ABC", w=50, h=50, command="importChar()")
b2=mc.button(nameWindow + 'btn2',label='UPDATE SHADER', w=50, h=50, command='')
mc.showWindow(nameWindow)

#Ruta absoluta de carpeta donde estan todos los personajes
pathCharacters = 'M:/MAYA/01_CHAR'
#Leo los nombres de las carpetas y las guardo
charsFolders = os.listdir(pathCharacters)



'''
#Separo lo nombres de las carpetas
for nF in charsFolders:
    nameFix = nF.split('_')[-1]
    namesCharacters.append(nameFix)
    print nameFix
'''

#Leo los archivos en la carpeta seleccionada con la funcion list_files
filesInFolder = list_files( pathCharacters + '/' +  charsFolders[selecStringChar])

#Trato de ver si hay un archivo que tenga '_SHD'
for fileShader in filesInFolder:
    if fileShader.split('_SHD'):
        thisFileToLoad = fileShader
    else:
        mc.warning('NO EXISTE ARCHIVO QUE CONTANGA _SHD')

def importChar():
    #Lista de la seleccion del scroll
    selObj = cmds.textScrollList(nameWindow + 'FOLDERS',q=True, si=True)
    unidad = mc.textFieldGrp(nameWindow + 'UD', q = True, text=True)
    scene = mc.textFieldGrp(nameWindow + 'ESC', q = True, text=True)
    char = mc.textFieldGrp(nameWindow + 'CHAR', q = True, text=True)
    loadCharactersScene(unidadDisco,unidad,scene,char)
    #makeAlembic()

def loadCharactersScene(unidadDisco,unidad,scene,char):
    unidadDisco= 'D:/'
    pathMaya= 'MAYA/05_SHOT/UD'
    pathEs= '/E'
    esChar = 'E'
    pathAnim= '/Anim_Wip/'

    if (char):
        #aqui estan los archivos de animacion para importar el rig o los rig UD16_E117_FINAL.ma
        pathLoadAni = unidadDisco + str(pathMaya) + str(unidad) + str(pathEs) + str(scene) + str(pathAnim)
        fileCharFinal = str( 'UD' + str(unidad) + str(esChar) + str(scene) + '_' + str(char) + '_FINAL.ma')
        pathFile = str(pathLoadAni + fileCharFinal)
        print 'RUTA Y ARCHIVO DE CARGA: ' + pathFile
    else:
        #aqui estan los archivos de animacion para exportar alembic UD16_E117_FINAL.ma
        pathLoadAni = unidadDisco + str(pathMaya) + str(unidad) + str(pathEs) + str(scene) + str(pathAnim)
        fileCharFinal = str( 'UD' + str(unidad) + '_' + str(esChar) + str(scene) + '_FINAL.ma')
        pathFile = str(pathLoadAni + fileCharFinal)
        print 'RUTA Y ARCHIVO DE CARGA: ' + pathFile

    if os.path.exists(pathFile):
        nFile = mc.file(pathFile, i=True)
    else:
        mc.warning('NO EXISTE EL EL ARCHIVO -> ' + fileCharFinal )

def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files
#aqui guardar el archivo exportado UD16_E117_ALVARO_FINAL.abc
def makeAlembic(path):
    # check to see if plugin is loaded
    plugs=mc.pluginInfo( query=True, listPlugins=True )
    if "AbcExport" not in plugs :
      print "AbcExport not loaded please load it"

#only a string as command to pass all args
#"-frameRange 1 120 -uvWrite -dataFormat ogawa -root |ARTURO_ROOT|ARTURO_MSH_GRP|ARTURO_CABEZA_MSH -file D:/MAYA/06_SHOT_RESULT/UD16/E117/UD16_E117_ARTURO_FINAL.abc";
minTime = mc.playbackOptions( query=True, minTime=True)
maxTime = mc.playbackOptions( query=True, maxTime=True)
command = "-frameRange" +" " +str(int(minTime)) + " " +str(int(maxTime))+" "+"-uvWrite"+str(myRoot)+" -file "+str(Outpoutpath)
mc.AbcExport( j = command )
pathSaveAniAbc = 'M:/MAYA/06_SHOT_RESULT/' + unidad + '/' + scene
fileAbcFinal = ''
print pathSaveAniAbc
    if not os.path.exists(pathLoadAni):
        os.mkdir(pathLoadAni)
