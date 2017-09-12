import maya.cmds as cmds
def onOffAttr(tipo='hairSystem',attr='simulationMethod',onOff=0):
	try:
		nodos=cmds.ls(type=tipo)
		currentState={}
		errores=[]
		for nodo in nodos:
			listAtt=cmds.listAttr(nodo)
			for at in listAtt:
				if attr in at:
					v=int(cmds.getAttr(nodo+'.'+attr))
					currentState[nodo]=v
					if onOff != None:
						cmds.setAttr(str(nodo)+'.'+attr,onOff)
					else:
						cmds.warning('Falta especificar argumento onOff. ')
		return currentState
	except:
		pass
