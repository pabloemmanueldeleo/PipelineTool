import maya.cmds as mc
import maya.mel as mel
import os
def bakearGUI():
	global winCrear2
	if mc.window('BAKEAR',exists=True):
		mc.deleteUI('BAKEAR')
	winCrear2=mc.window('BAKEAR', title='MegaTurboProDeluxe BAKER',  backgroundColor=[0,0,0],titleBarMenu=1,toolbox=1,s=0 ,resizeToFitChildren=1)
	row_1 = mc.columnLayout( parent=winCrear2 , backgroundColor=[0.1,0.1,0.1] , columnAlign = 'center'	, rowSpacing = 5)
	mc.separator()
	col_1 = mc.rowLayout( parent=winCrear2, backgroundColor=[0.2,0.2,0.2] , columnAttach = [1, 'both', 5]	, columnAlign4= ["center", "center", "center", "center"],numberOfColumns=4 )
	mc.button( label=' TRASLACION ' , parent=col_1 ,  backgroundColor=[0.6,0.6,0.6] , command='MEGATURBOPRODELUXEBAKER.traslacionTodos()')
	mc.checkBox ('chB_tx' , label='X', align='right' , parent=col_1 , value=1 , backgroundColor=[0.3,0.3,0.3])
	mc.checkBox ('chB_ty' , label='Y', align='right' , parent=col_1 ,  value=1 , backgroundColor=[0.3,0.3,0.3])
	mc.checkBox ('chB_tz' , label='Z', align='right' , parent=col_1 ,  value=1 , backgroundColor=[0.3,0.3,0.3])
	col_2 = mc.rowLayout(  parent=winCrear2, backgroundColor=[0.2,0.2,0.2] , columnAttach = [1, 'both', 5] , columnAlign6= ["center", "center", "center", "center", "center", "center"], numberOfColumns=6  )
	mc.button( label='   ROTACION  ' , parent=col_2 ,  backgroundColor=[0.6,0.6,0.6] , command='MEGATURBOPRODELUXEBAKER.rotacionTodos()')
	mc.checkBox ('chB_rx' , label='X', align='both' , parent=col_2 ,   value=1 , backgroundColor=[0.3,0.3,0.3])
	mc.checkBox ('chB_ry' , label='Y', align='right' , parent=col_2 ,  value=1 ,  backgroundColor=[0.3,0.3,0.3])
	mc.checkBox ('chB_rz' , label='Z', align='right' , parent=col_2 ,  value=1 ,  backgroundColor=[0.3,0.3,0.3])
	mc.separator (w=10, st="none")
	col_3 = mc.rowLayout( parent=winCrear2, backgroundColor=[0.2,0.2,0.2] , columnAttach = [1, 'both', 5]	, columnAlign4= ["center", "center", "center", "center"],numberOfColumns=4  )
	mc.button( label='     ESCALA     ' , parent=col_3 ,  backgroundColor=[0.6,0.6,0.6] , command='MEGATURBOPRODELUXEBAKER.escalaTodos()')
	mc.checkBox ('chB_sx' , label='X', align='right' , parent=col_3 ,  value=1 ,  backgroundColor=[0.3,0.3,0.3])
	mc.checkBox ('chB_sy' , label='Y', align='right' , parent=col_3 ,  value=1 ,  backgroundColor=[0.3,0.3,0.3])
	mc.checkBox ('chB_sz' , label='Z', align='right' , parent=col_3 ,   value=1 , backgroundColor=[0.3,0.3,0.3])

	col_4 = mc.rowLayout( parent = winCrear2 , backgroundColor = [0.2,0.2,0.2] , columnAttach = [1, 'both', 55]	, columnAlign1= "center",numberOfColumns=1  )
	mc.checkBox ('chB_fl' , label='FocalLenght', align='right' , parent=col_4 ,  value=1 ,  backgroundColor=[0.3,0.3,0.3])

	lay_boton = mc.rowLayout( parent=winCrear2 , h=25 , w=185 , backgroundColor=[0.5,0.5,0.5] ,numberOfColumns=2  )
	mc.button( label='TODOS'  ,w=90  , parent=lay_boton ,  backgroundColor=[0.6,0.6,0.6] , command='MEGATURBOPRODELUXEBAKER.todos()')
	mc.button( label='NINGUNO',w=90  , parent=lay_boton ,  backgroundColor=[0.6,0.6,0.6] , command='MEGATURBOPRODELUXEBAKER.ninguno()')
	lay_boton2 = mc.rowLayout( parent=winCrear2 , h=25 , w=185 , backgroundColor=[0.5,0.5,0.5] ,numberOfColumns=1 )
	mc.button( label='BAKEAR' ,w=182  , parent=lay_boton2 ,  backgroundColor=[0.6,0.6,0.6] , command='MEGATURBOPRODELUXEBAKER.bakeCanales()')
	mc.window('BAKEAR',e=1,wh=[185,180]  )
	mc.showWindow( winCrear2 )
	mc.warning ("MegaTurboProDeluxe BAKER v1.3 . SE EXPORTARA A D:\EXPORT")

def todos():
	checkBoxes = ['chB_tx','chB_ty','chB_tz','chB_rx','chB_ry','chB_rz','chB_sx','chB_sy','chB_sz','chB_fl']
	for chB in checkBoxes:
		mc.checkBox (chB , e=1 , value=1)

def ninguno():
	checkBoxes = ['chB_tx','chB_ty','chB_tz','chB_rx','chB_ry','chB_rz','chB_sx','chB_sy','chB_sz','chB_fl']
	for chB in checkBoxes:
		mc.checkBox (chB , e=1 , value=0)

def traslacionTodos():
	checkBoxes = ['chB_tx','chB_ty','chB_tz']
	estadoChB = mc.checkBox ('chB_tx',q=1,value=1)
	for chB in checkBoxes:
		mc.checkBox (chB , e=1 , value=not estadoChB)

def rotacionTodos():
	checkBoxes = ['chB_rx','chB_ry','chB_rz']
	estadoChB = mc.checkBox ('chB_rx',q=1,value=1)
	for chB in checkBoxes:
		mc.checkBox (chB , e=1 , value= not estadoChB)

def escalaTodos():
	checkBoxes = ['chB_sx','chB_sy','chB_sz']
	estadoChB = mc.checkBox ('chB_sx',q=1,value=1)
	for chB in checkBoxes:
		mc.checkBox (chB , e=1 , value=not estadoChB)

def seteoExportFBX(inFrame=1,outFrame=2,nombreFBX="EXPORT"):
	mel.eval("FBXExportSmoothingGroups -v true")
	mel.eval("FBXExportHardEdges -v false")
	mel.eval("FBXExportTangents -v false")
	mel.eval("FBXExportSmoothMesh -v true")
	mel.eval("FBXExportInstances -v false")
	mel.eval("FBXExportBakeComplexAnimation -v false")
	mel.eval("FBXExportUseSceneName -v false")
	mel.eval("FBXExportQuaternion -v euler")
	mel.eval("FBXExportShapes -v true")
	mel.eval("FBXExportSkins -v false")
	mel.eval("FBXExportConstraints -v false")
	mel.eval("FBXExportCameras -v true")
	mel.eval("FBXExportLights -v false")
	mel.eval("FBXExportEmbeddedTextures -v false")
	mel.eval("FBXExportInputConnections -v true")
	mel.eval("FBXExportUpAxis y")
	mc.sysFile ("D:/EXPORT/", makeDir=True )
	mel.eval("FBXExport -f \"D:/EXPORT/"+ nombreFBX +".fbx\" -s;")

def bakeCanales():
	shotsAll = mc.ls (type="shot")
	shots = []
	curvasParaBorrar=[]
	shotsConCamaraMalAsignada=[]
	shotsConCamaraMalAsignadaStr=""

	for i,s in enumerate(shotsAll):
		if mc.shot(s,q=1,trk=1)==1 or mc.shot(s,q=1,trk=1)==2:
			shots.append(s)

	for sho in shots:
		if not "_CAMSH" in mc.shot (sho,q=1,cc=1):
			shotsConCamaraMalAsignada.append (sho)
			print sho

	canales = ['chB_tx','chB_ty','chB_tz','chB_rx','chB_ry','chB_rz','chB_sx','chB_sy','chB_sz','chB_fl']
	canalesParaBake=[]
	constraints=[]
	camaraAsignadaAlShotTRF=""
	for canal in canales:
		canalPedido = mc.checkBox (canal, q=1, value=1)
		if canalPedido == True:
			canalesParaBake.append( canal.split('chB_')[1] )
	if len(shotsConCamaraMalAsignada)==0:
		if len(shots)!=0  :
			if len(canalesParaBake) !=0 :
				mel.eval("paneLayout -e -manage false $gMainPane")
				mc.confirmDialog( title='RECORDA', message='RECORDA QUE ESTA CAMARA NO BORRA LOS KEYS QUE GENERA', button=['OKI'], backgroundColor=[1,0.1,0.1] ,defaultButton='OKI', cancelButton='OKI')
				for o in shots:
					camaraAsignadaAlShotTRF = mc.listRelatives( mc.shot (o, q=1, cc=1) , p=1 , type='transform')[0]
					atts = mc.listAttr (camaraAsignadaAlShotTRF,k=1)
					print o," camaraAsignadaAlShotTRF::::----> " + camaraAsignadaAlShotTRF
					for att in atts:
						mc.setAttr (camaraAsignadaAlShotTRF+"."+att, l=0)
					inF = mc.shot (o, q=1 , startTime =1)
					outF = mc.shot (o, q=1 , endTime =1)

					inFrameSequencer = mc.shot (o, q=1 , sequenceStartTime =1)
					outFrameSequencer = mc.shot (o, q=1 , sequenceEndTime =1)


					for canalSolicitado in canalesParaBake:
						if canalSolicitado=="fl":
							mel.eval('bakeResults -simulation true -t "'+str(inF)+':'+str(outF)+'" -sampleBy 1 -disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -bakeOnOverrideLayer false -minimizeRotation true -at "'+canalSolicitado+'" '+camaraAsignadaAlShotTRF+'SH;')
						else:
							mel.eval('bakeResults -simulation true -t "'+str(inF)+':'+str(outF)+'" -sampleBy 1 -disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -bakeOnOverrideLayer false -minimizeRotation true -at "'+canalSolicitado+'" '+camaraAsignadaAlShotTRF+';')
					shotsClonExcluyendo = []
					for item in shots:
						shotsClonExcluyendo.append(item)
					shotsClonExcluyendo.remove(o)
					for excluido in shotsClonExcluyendo:
						print "excluido " + excluido
						if mc.shot (excluido, q=1 , sequenceStartTime =1)==inFrameSequencer and mc.shot (excluido, q=1 , sequenceEndTime =1)==outFrameSequencer and mc.shot(excluido,q=1,track=1)!=3 and mc.shot(excluido,q=1,track=1)!=mc.shot(o,q=1,track=1):
							camaraAsignadaAlExcluidoShotTRF = mc.listRelatives( mc.shot (excluido, q=1, cc=1), p=1 , type='transform')[0]
							atts = mc.listAttr (camaraAsignadaAlExcluidoShotTRF,k=1)
							print o," camaraAsignadaAlExcluidoShotTRF::::----> " + camaraAsignadaAlExcluidoShotTRF
							for att in atts:
								mc.setAttr (camaraAsignadaAlExcluidoShotTRF+"."+att, l=0)

							print ( camaraAsignadaAlShotTRF , camaraAsignadaAlExcluidoShotTRF )
							for canalSolicitado in canalesParaBake:
								if canalSolicitado=="fl":
									mel.eval('bakeResults -simulation true -t "'+str(inF)+':'+str(outF)+'" -sampleBy 1 -disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -bakeOnOverrideLayer false -minimizeRotation true -at "'+canalSolicitado+'" '+camaraAsignadaAlExcluidoShotTRF+'SH;')
								else:
									mel.eval('bakeResults -simulation true -t "'+str(inF)+':'+str(outF)+'" -sampleBy 1 -disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -bakeOnOverrideLayer false -minimizeRotation true -at "'+canalSolicitado+'" '+camaraAsignadaAlExcluidoShotTRF+';')
							mc.select ( camaraAsignadaAlShotTRF , camaraAsignadaAlExcluidoShotTRF )
							seteoExportFBX ( int(inF) , int(outF) , camaraAsignadaAlShotTRF)
							curvasParaBorrar.append( mc.listConnections (camaraAsignadaAlShotTRF,exactType=1,type="animCurveTL" ))
							curvasParaBorrar.append( mc.listConnections (camaraAsignadaAlShotTRF,exactType=1,type="animCurveTA" ))
							curvasParaBorrar.append( mc.listConnections (camaraAsignadaAlExcluidoShotTRF,exactType=1,type="animCurveTL" ))
							curvasParaBorrar.append( mc.listConnections (camaraAsignadaAlExcluidoShotTRF,exactType=1,type="animCurveTA" ))
				mel.eval("paneLayout -e -manage true $gMainPane")
				os.system ("explorer \"D:\export\"")
			else:
				mc.warning ("NINGUN CANAL SELECCIONADO, SELECCIONA LOS CANALES QUE QUERES BAKEAR.")
		else:
			mc.warning ("NO SE DETECTAN NODOS \"shot\".")
	else:
		for sho in shotsConCamaraMalAsignada:
			shotsConCamaraMalAsignadaStr=shotsConCamaraMalAsignadaStr + sho + "\n"
		mc.select (shotsConCamaraMalAsignada)
		print "shotsConCamaraMalAsignadaStr " + shotsConCamaraMalAsignadaStr
		mc.confirmDialog( title='BAKER: ALERTA', message='SE ENCONTRARON SHOTS CON CAMARA MAL ASIGNADA. \nSE LOS HA SELECCIONADO PARA UBICARLOS MAS RAPIDO:\n\n' + shotsConCamaraMalAsignadaStr , button=['OKI'], backgroundColor=[.7,0.7,0.7] ,defaultButton='OKI', cancelButton='OKI')
		mc.warning ("HAY SHOTS CON CAMARAS MAL ASIGNADAS.")
