import maya.cmds as cmds
def setResolution(width=None, height=None, pixelAspect=None):
	    confirma = cmds.confirmDialog ( title='Confirmar', message='SEGURO QUE DESEAS SETEAR EL RENDER Y LAS CAMARAS PARA SHAKE UN 10%?', button=['SI, AMEO','NO, QUEDATE PIOLA'], defaultButton='SI, AMEO', cancelButton='NO, QUEDATE PIOLA', dismissString='NO, QUEDATE PIOLA' )
	    if confirma=='SI, AMEO':
			cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 1)
			cmds.setAttr("defaultResolution.width", (cmds.getAttr("defaultResolution.width"))*1.1  )
			cmds.setAttr("defaultResolution.height", (cmds.getAttr("defaultResolution.height"))*1.1   )

			camaras = cmds.ls (ca=1)
			for cam in camaras:
				cmds.setAttr(cam+".horizontalFilmAperture", (cmds.getAttr(cam+".horizontalFilmAperture"))*1.1)
				cmds.setAttr(cam+".verticalFilmAperture", (cmds.getAttr(cam+".verticalFilmAperture"))*1.1)
	    else:
	        cmds.warning ("CANCELADO POR USUARIO. TODO LISO. ")
