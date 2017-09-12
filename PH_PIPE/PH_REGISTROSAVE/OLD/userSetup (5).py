import maya.cmds as cmds
import getpass
import subprocess

usuario=getpass.getuser()
print 'USUARIO: ' + str(usuario)
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/userSetup.py", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/userSetup.py"))
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/registraGuarda.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/registraGuarda.pyc") )

print "COPIAS NECESARIA PARA GOLEM"
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/rlm/rlm.exe", copy= ( "C:/rlm/rlm.exe") )
filepath="M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/variablesParaWindows.bat"
p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
stdout, stderr = p.communicate()
if p.returncode==0:
	print 'Se cargo las variables en el sistema.'# is 0 if success

print "COPIAS NECESARIA PARA GOLEM FINALIZADA"


cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_CUSTOMAYA/PH_CUSTOMAYA.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/PH_CUSTOMAYA.pyc") )
import PH_CUSTOMAYA
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/EnlistaDiscos.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/EnlistaDiscos.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_LIGHTING/PH_RANGOCAMARA/PH_RANGOCAMARA.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/PH_RANGOCAMARA.pyc"))
cmds.sysFile ("M:/PH_SCRIPTS/_SCRIPTS/UTILITIES.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/UTILITIES.pyc") )

import registraGuarda
cmds.scriptJob (e=['SceneSaved',registraGuarda.registraGuarda] )

import EnlistaDiscos
EnlistaDiscos.enlistaDiscos()

import PH_RANGOCAMARA
cmds.scriptJob ( e= ['playbackRangeSliderChanged' , setearInOutRender ]  )
