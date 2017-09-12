import maya.cmds as cmds
import getpass

usuario=getpass.getuser()

cmds.sysFile ("M:/Maya_Script/upd/userSetup.py",      copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/userSetup.py")  )
cmds.sysFile ("M:/Maya_Script/upd/registraGuarda.py", copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/registraGuarda.py") )
cmds.sysFile ("M:/Maya_Script/upd/upd.py",            copy= ( "C:/Users/" + usuario + "/Documents/maya/2015-x64/scripts/upd.py") )


import registraGuarda
cmds.scriptJob (e=['SceneSaved',registraGuarda.registraGuarda] )
