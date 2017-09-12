import maya.cmds as cmds
import getpass
import os
import subprocess
import registraGuarda
import EnlistaDiscos
import PH_RANGOCAMARA

paths='M:/PH_SCRIPTS/_SCRIPTS/','M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/','M:/PH_SCRIPTS/PH_LIGHTING/PH_RANGOCAMARA'
for path in paths:
	if not path in sys.path:
	    sys.path.append(path)
directorioShelf='M:/PH_SCRIPTS/_SHELF/'

usuario=getpass.getuser()
print 'USUARIO: ' + str(usuario)

cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/userSetup.py", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/userSetup.py"))
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/registraGuarda.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/registraGuarda.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_CUSTOMAYA/PH_CUSTOMAYA.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/prefs/scripts/PH_CUSTOMAYA.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/EnlistaDiscos.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/EnlistaDiscos.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_LIGHTING/PH_RANGOCAMARA/PH_RANGOCAMARA.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/PH_RANGOCAMARA.pyc"))
cmds.sysFile ("M:/PH_SCRIPTS/_SCRIPTS/UTILITIES.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/UTILITIES.pyc") )
#Shelf for all
for file in os.listdir(directorioShelf):
    if file.endswith(".mel"):
		if cmds.sysFile ("M:/PH_SCRIPTS/_SHELF/"+str(file), copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/prefs/shelves/"+str(file))):
			print 'Se actualizo correctamente el shelf ' + str(file)
		else:
			print 'No fue necesario copiar el shelf o algo no funciono con ' + str(file)

print "COPIAS NECESARIA PARA GOLEM"
rlmDir='C:/rlm/'
if not os.path.exists(rlmDir):
    os.makedirs(rlmDir)
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/rlm/rlm.exe", copy= ( rlmDir+"rlm.exe") )

filepath="M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/variablesParaWindows.bat"
p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
stdout, stderr = p.communicate()
if p.returncode==0:
	print 'Se cargo las variables en el sistema.'# is 0 if success
print "COPIAS NECESARIA PARA GOLEM FINALIZADA"


cmds.scriptJob (e=['SceneSaved',registraGuarda.registraGuarda] )
EnlistaDiscos.enlistaDiscos()
cmds.scriptJob ( e= ['playbackRangeSliderChanged' , PH_RANGOCAMARA.setearInOutRender ]  )
B=BOTONERA()
cmds.evalDeferred("import PH_CUSTOMAYA")
cmds.evalDeferred(B=BOTONERA())
