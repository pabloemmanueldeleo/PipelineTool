import maya.cmds as mc
def setResolution(width=None, height=None, pixelAspect=None):
	global listaLayer
	try:
		del renderLayers
	except:
		pass
	anchoActual = mc.getAttr("defaultResolution.width")
	height = mc.getAttr("defaultResolution.height")
	rlayers = mc.ls (type="renderLayer")
	if 'defaultRenderLayer' in rlayers:
		rlayers.remove('defaultRenderLayer')

	if mc.window ('listaLayers',ex=1):
		mc.deleteUI ('listaLayers')
	if len (rlayers) > 0:
		print rlayers,len(rlayers)
		confirma = mc.promptDialog(title='OVERSCAN 1.0',
				message= 'ANCHO ACTUAL: ' + str(anchoActual) + '\nINGRESA CUANTOS PXs QUERES SUMAR:',
				button=['OK', 'Cancel'],
				defaultButton='OK',
				cancelButton='Cancel',
				dismissString='Cancel')
		if confirma=='OK':
			if str(mc.promptDialog(q=1, text=1)).isdigit():
				mc.window('listaLayers', title='RENDER LAYERS')
				lay_lista = mc.columnLayout ( 'column1' , p='listaLayers',adjustableColumn=1 )
				listaLayer=mc.textScrollList (p=lay_lista , numberOfRows=40 , h=150 , allowMultiSelection = True,append=rlayers)
				mc.button ('b_OK' , l='OK' , c=OverrideLayers )
				mc.showWindow ('listaLayers')
			else:
				mc.warning ("INGRESO INVALIDO. CANCELADO.")
		else:
			mc.warning ("CANCELADO POR EL USUARIO.")
	else:
		mc.warning('NO SE DETECTARON RENDER LAYERS AMEEEOOOO')

def OverrideLayers(*args):
	if mc.textScrollList(listaLayer,q=1,si=1)!=None:
		global listaLayer
		anchoActual = mc.getAttr("defaultResolution.width")
		height = mc.getAttr("defaultResolution.height")
		layers = mc.textScrollList(listaLayer,q=1,si=1)
		pixelsMas = int(mc.promptDialog(q=1, text=1))
		device_aspect = float( ( anchoActual+pixelsMas )* 1.0)/float(height)
		wit=anchoActual+pixelsMas
		mc.deleteUI ('listaLayers')
		for layer in layers:
			mc.editRenderLayerGlobals ( currentRenderLayer=layer )
			mc.editRenderLayerAdjustment ('defaultResolution.lockDeviceAspectRatio', layer=layer)
			mc.setAttr('defaultResolution.lockDeviceAspectRatio', 1)
			mc.editRenderLayerAdjustment ('defaultResolution.width', layer=layer)
			mc.setAttr('defaultResolution.width', wit)
			mc.editRenderLayerAdjustment ('defaultResolution.height', layer=layer)
			mc.setAttr("defaultResolution.height", height)
			mc.editRenderLayerAdjustment ('defaultResolution.deviceAspectRatio', layer=layer)
			mc.setAttr("defaultResolution.deviceAspectRatio", device_aspect)
			cams = mc.ls (ca=1)
			for cam in cams:
				#mc.setAttr (cam+".horizontalFilmAperture", (anchoActual+pixelsMas)*0.98/2048 )
				vfilm=mc.getAttr(cam+'.verticalFilmAperture' )
				mc.editRenderLayerAdjustment(cam+'.cameraAperture', layer=layer)
				mc.setAttr(cam+'.cap', wit*(0.98/2048), vfilm ,type='double2' )
				mc.setAttr ("defaultResolution.pa",1)
	else:
		mc.warning ("NO HAY SELECCION EN LA LISTA DE RENDER LAYERS. RECATATEEE !!")
