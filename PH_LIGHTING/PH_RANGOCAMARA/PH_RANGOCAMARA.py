import maya.cmds as mc
def setearInOutRender():
	camaras = mc.ls (type="camera")
	nS = mc.ls (sl=1)
	for n in nS:
	    if mc.objectType(n)=="shot":
			shotSeleccionado = n[0]
			inShot = int(mc.shot (n , q=1 ,st=1))
			outShot = int(mc.shot (n, q=1 ,et=1))
			duracionShot = outShot - inShot + 1
			mc.setAttr ("defaultRenderGlobals.startFrame" , inShot)
			mc.setAttr ("defaultRenderGlobals.endFrame" , outShot)
			mc.headsUpMessage ("CANTIDAD DE FRAMES: " + str(duracionShot) )
			mc.playbackOptions (min=inShot)
			mc.playbackOptions (max=outShot)
