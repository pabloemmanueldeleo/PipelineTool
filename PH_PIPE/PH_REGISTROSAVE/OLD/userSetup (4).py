import maya.cmds as cmds
import getpass

usuario=getpass.getuser()

cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/userSetup.py",      copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/userSetup.py")  )
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/registraGuarda.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/registraGuarda.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_AUTOSHELF/upd.pyc",            copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/upd.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_PIPE/PH_REGISTROSAVE/EnlistaDiscos.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/EnlistaDiscos.pyc") )
cmds.sysFile ("M:/PH_SCRIPTS/PH_LIGHTING/PH_RANGOCAMARA/PH_RANGOCAMARA.pyc", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/PH_RANGOCAMARA.pyc") )

import registraGuarda
cmds.scriptJob (e=['SceneSaved',registraGuarda.registraGuarda] )

import EnlistaDiscos
EnlistaDiscos.enlistaDiscos()

import PH_RANGOCAMARA
cmds.scriptJob ( e= ['playbackRangeSliderChanged' , setearInOutRender ]  )