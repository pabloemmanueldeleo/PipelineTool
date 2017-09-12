# -*- encoding: utf-8 -*-
# CAMS A STEREO v1.3 - 22/07/2015
# Importa los rigs stereo y los empata a las camaras standards en posicion, rotacion y focalLenght.
# Seleccionar las camaras que se deseen procesar.
# Si no puede por algun motivo, deja seleccionadas las camaras con problemas.

import maya.cmds as cmds
import maya.mel as mel
import sets

#################################################################################

def matchStr (str1,str2):
    #str1 es el patron, el checker. (por ejemplo,'UD??_E???_P??_CAM')
    #str2 es la string que quiero ver si esta bien.
    #return True, hay match.
    #return False, no hay match.
    hayDif=False
    for i in range(len(str1)):
        if (hayDif !=True):
            if (str1[i] != '?'):
                hayDif=  not(str1[i] == str2[i])
            else:
                if str2[i] not in ['0','1','2','3','4','5','6','7','8','9']:
                    hayDif=True
    return not(hayDif)

#conecta los mismos atributos de un mismo nodo ya conectados en nodoA hacia nodoB

def conectToOtherNode(nodeA,nodeB):
    attrs=cmds.listConnections(nodeA)
    attrs2=cmds.listAttr(nodeB,keyable=1)
    c1={}
    conect=''
    disconect=''
    for att in attrs:
        c1 [  cmds.listConnections(att,plugs=1,connections=True) [0] ]  =     cmds. listConnections(att,plugs=1,connections=True)[1]
    for i in range(len(attrs2)):
        for k, v in c1.items():
            if str(v.split('.')[1]) in attrs2[i]:
                conect=cmds.connectAttr(k,nodeB+'.'+attrs2[i] , f=True)
                #disconect=cmds.disconnectAttr(k,v)
                #print 'Pude conectar el '+str(conect)

# BORRA DUPLICADOS DE ARRAY
def borrarDuplicados (aConDuplicados):
    a =set(aConDuplicados)
    result = []
    for item in a:
        result.append(item)
    return result
# RENOMBRO
def renombrado ():
    cmds.rename ( 'C_E999_P00__GRP', ('C_' + EXXX_PXX +'__GRP')  )
    cmds.rename ( 'C_E999_P00__CNTSH', ("C_" + EXXX_PXX +"__CNTSH") )
    cmds.rename ( 'C_E999_P00__TRF' ,("C_" + EXXX_PXX +"__TRF"))
    cmds.rename ( 'L_E999_P00__CAM' ,("L_" + EXXX_PXX + "__CAM"))
    cmds.rename ( 'L_E999_P00__HCNS', ("L_" + EXXX_PXX +"__HCNS") )
    cmds.rename ( 'R_E999_P00__CAM', ("R_" + EXXX_PXX + "__CAM"))
    cmds.rename ( 'R_E999_P00__HCNS', ("R_" + EXXX_PXX +"__HCNS"))
    cmds.rename ( 'C_E999_P00__CNT', ("C_" + EXXX_PXX + "__CNT"))
    cmds.rename ( 'C_E999_P00_SCAM', ("C_"+EXXX_PXX + "_SCAM"))
    cmds.rename ( 'L_E999_P00_SCAM', ("L_" + EXXX_PXX + "__SCAM"))
    cmds.rename ( 'R_E999_P00_SCAM', ("R_" + EXXX_PXX + "__SCAM"))
    cmds.rename ( 'C_E999_P00__HCNS', ("C_"+EXXX_PXX + "__HCNS"))
# LOCKEO
def lockeado () :
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.tx") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.ty") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.tz") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.rx") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.ry") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.rz") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.v") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.INTERAXIAL") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.ZEROP") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.CONVERGENCE") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.FocalLenght") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.NearClip") , l=1 )
    cmds.setAttr ( ("C_"+EXXX_PXX+"__CNT.FarClip") , l=1 )

# ---------------------------------------------------------------------------------------------------

objetosSeleccionados = cmds.ls(sl=True)
indexSel = 0 ;
hayNombreMalo = False
noTieneKeys = False
objsConProb=[]

for cam in objetosSeleccionados:
    if matchStr ('UD??_E???_P??_CAM',cam)==False:
        hayNombreMalo=True
        objsConProb.append(cam)


    if cmds.keyframe(cam,q=True)>0:
        listaKeyframes =   borrarDuplicados ( cmds.keyframe(cam,q=True)  )
        cantidadKeyframes = len ( listaKeyframes )
        if cantidadKeyframes<2:
            noTieneKeys = True
            objsConProb.append(cam)
    cuantosK = ( cmds.keyframe(cam,q=True) )
    if cuantosK==None:
        objsConProb.append(cam)

if ( (len(objetosSeleccionados) ) !=0 ) and ( (len(objsConProb) ) == 0 ):
    for i in range( len (objetosSeleccionados) ):

        lista1 = cmds.listRelatives (objetosSeleccionados[i],s=1)
        if cmds.objectType( lista1[0]  , isType= 'camera' ) :
            if objetosSeleccionados[i] != 'front':
                if objetosSeleccionados[i] != 'top':
                    if objetosSeleccionados[i] != 'side':
                        if objetosSeleccionados[i] != 'persp':
                            ## SI LOS PADRES NO ESTAN EN 0,0,0  ó  si estan escalados no conecto y bakeo
                            padresDeSel = cmds.listRelatives( objetosSeleccionados[indexSel], fullPath=1 )
                            padresDeSelSplit = (padresDeSel[0][1:]).split('|')
                            padresDeSelSplitEditado = padresDeSelSplit[0:len(padresDeSelSplit)-2]
                            checkTR=0
                            checkS=1
                            EXXX_PXX = objetosSeleccionados[indexSel] [5: len ( objetosSeleccionados[indexSel] )-4 ]
                            print (objetosSeleccionados[indexSel],EXXX_PXX,)
                            if len (padresDeSelSplitEditado)!=0:
                                for padre in padresDeSelSplitEditado:
                                    coorTGlobales = cmds.xform ( padre, q =1, worldSpace = 1,  t = 1 )
                                    coorRGlobales = cmds.xform ( padre, q =1, worldSpace = 1,  ro = 1)
                                    coorSGlobales = cmds.xform ( padre, q =1, worldSpace = 1,  scale = 1)
                                    if ((coorTGlobales [0]==0) & (coorTGlobales [1]==0) & (coorTGlobales [2]==0) & (coorRGlobales [0]==0) & (coorRGlobales [1]==0) & (coorRGlobales [2]==0) & (coorSGlobales [0]==1) & (coorSGlobales [1]==1) & (coorSGlobales [2]==1) ) == False:
                                        checkTR+=1
                                        checkS+=1
                            if ( (checkTR==0) and (checkS==1) ) or ( len (padresDeSelSplitEditado)==0):
                                print (' CONECTA !\n\n')
                                mel.eval( 'file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;"  -pr "M:/PH_SCRIPTS/SCENES_RIG/IMPORTRIGS/rig_esterocam_final.ma" ')
                                conectToOtherNode( objetosSeleccionados[i] , "C_E999_P00__CNT" )
                                focalLength = cmds.camera ( objetosSeleccionados[indexSel] , q=True , fl=True )
                                cmds.setAttr ( "C_E999_P00__CNT.FocalLenght", focalLength )
                                renombrado ()
                                lockeado ()
                                indexSel+=1
                            else:
                                print (" BAKEA\n")
                                mel.eval( 'file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;"  -pr "M:/PH_SCRIPTS/SCENES_RIG/IMPORTRIGS/rig_esterocam_final.ma" ')
                                listaKeyframes =   borrarDuplicados (   cmds.keyframe(objetosSeleccionados[i],q=True)  )
                                cantidadKeyframes = len ( listaKeyframes )
                                cmds.paneLayout('viewPanes', q=True, pane1=True)
                                cmds.isolateSelect (cmds.paneLayout('viewPanes', q=True, pane1=True), state=1 )

                                for i in range( cantidadKeyframes ):
                                    cmds.currentTime ( listaKeyframes[i] )
                                    # Q
                                    PosCamVieja = cmds.xform ( objetosSeleccionados[indexSel], q=1 , ws=1 , t=1 )
                                    RotCamVieja = cmds.xform ( objetosSeleccionados[indexSel], q=1 , ws=1 , ro=1 )
                                    focalLength = cmds.camera ( objetosSeleccionados[indexSel] , q=True , fl=True )

                                    # S
                                    cmds.move ( PosCamVieja[0] , PosCamVieja[1] , PosCamVieja[2] , 'C_E999_P00__CNT',a=1 )
                                    cmds.rotate ( RotCamVieja[0] , RotCamVieja[1] , RotCamVieja[2] , 'C_E999_P00__CNT',a=1 )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.tx" )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.ty" )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.tz" )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.rx" )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.ry" )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.rz" )
                                    cmds.setAttr ( "C_E999_P00__CNT.FocalLenght", focalLength )
                                    cmds.setKeyframe ( "C_E999_P00__CNT.FocalLenght" )
                                    cmds.filterCurve  ('C_E999_P00__CNT_FocalLenght','C_E999_P00__CNT_translateX','C_E999_P00__CNT_translateY','C_E999_P00__CNT_translateZ','C_E999_P00__CNT_rotateX','C_E999_P00__CNT_rotateY','C_E999_P00__CNT_rotateZ')
                                renombrado ()
                                lockeado ()
                                indexSel+=1

        else:
            cmds.warning (objetosSeleccionados[indexSel] + " NO ES UNA CAMARA")
    cmds.isolateSelect (cmds.paneLayout('viewPanes', q=True, pane1=True), state=0 )
else:
    cmds.warning ("NO HAY NADA SELECCIONADO. O LAS CAMS ESTAN MAL NOMBRADAS y/o NO TIENEN KEYS. LAS SELECCIONE PARA QUE LAS MIRES")
    cmds.select (objsConProb)
