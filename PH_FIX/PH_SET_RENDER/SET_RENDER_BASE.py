import maya.cmds as mc
def setResolution(width=None, height=None, pixelAspect=None,customPixel=1.009):
    confirma = mc.confirmDialog ( title='Confirmar identidad 1.0', message='SEGURO QUE ERES EL AGENTE 015, ALIAS FRANCO?', button=['SI, SOY YO.\nMANDALE CUMBIA!','NO, POR SUERTE. \nQUIERO CANCELAR'], defaultButton='SI, SOY YO.\nMANDALE CUMBIA!', cancelButton='NO, POR SUERTE', dismissString='NO, POR SUERTE' )
    if confirma=='SI, SOY YO.\nMANDALE CUMBIA!':
        device_aspecto = float(width * pixelAspect)/float(height)
        mc.setAttr("defaultResolution.lockDeviceAspectRatio", 1)
        mc.setAttr("defaultResolution.width", width)
        mc.setAttr("defaultResolution.height", height)
        mc.setAttr("defaultResolution.deviceAspectRatio", device_aspecto)
        camaras = mc.ls (ca=1)
        for cam in camaras:
            mc.setAttr (cam+".horizontalFilmAperture",lock=0)
            actualApertura=mc.getAttr (cam+".horizontalFilmAperture")
            mc.setAttr (cam+".horizontalFilmAperture", (actualApertura*customPixel))
            mc.setAttr (cam+".horizontalFilmAperture",lock=1)
    else:
        mc.warning ("CANCELADO POR USUARIO. TODO LISO. ")
