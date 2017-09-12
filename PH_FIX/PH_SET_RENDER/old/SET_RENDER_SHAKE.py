import maya.cmds as mc
def setResolution(width=None, height=None, pixelAspect=None):

    confirma = mc.confirmDialog ( title='Confirmar', message='SEGURO QUE DESEAS SETEAR EL RENDER Y LAS CAMARAS PARA SHAKE?', button=['SI, AMEO','NO, QUEDATE PIOLA'], defaultButton='SI, AMEO', cancelButton='NO, QUEDATE PIOLA', dismissString='NO, QUEDATE PIOLA' )
    if confirma=='SI, AMEO':
        device_aspecto = float(width * pixelAspect)/float(height)
        mc.setAttr("defaultResolution.lockDeviceAspectRatio", 1)
        mc.setAttr("defaultResolution.width", width)
        mc.setAttr("defaultResolution.height", height)
        mc.setAttr("defaultResolution.deviceAspectRatio", device_aspecto)
        camaras = mc.ls (ca=1)
        for cam in camaras:
            mc.setAttr (cam+".horizontalFilmAperture", 0.982)
    else:
        mc.warning ("CANCELADO POR USUARIO. TODO LISO. ")
