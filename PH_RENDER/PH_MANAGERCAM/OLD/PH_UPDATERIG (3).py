# Update Rig v1.1 - 23/07/2015
# Actualiza los rigs stereos en transform y parametros de stereoscopia.
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
    str1=str1.upper()
    str2=str2.upper()
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

objetosSeleccionados = cmds.ls('SCAM_*_Control')
indexSel = 0 ;
hayNombreMalo = False
noTieneKeys = False
objsConProb=[]

for cam in objetosSeleccionados:
    if matchStr ('SCAM_E???_P??_Control',cam)==False:
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
        if cmds.objectType( lista1[0]  , isType= 'nurbsCurve' ) :

            ## SI LOS PADRES NO ESTAN EN 0,0,0  ó  si estan escalados no conecto y bakeo
            padresDeSel = cmds.listRelatives( objetosSeleccionados[indexSel], fullPath=1 )
            padresDeSelSplit = (padresDeSel[0][1:]).split('|')
            padresDeSelSplitEditado = padresDeSelSplit[0:len(padresDeSelSplit)-2]
            checkTR=0
            checkS=1
            EXXX_PXX = (objetosSeleccionados[indexSel] [5: len ( objetosSeleccionados[indexSel] )-8 ]).upper()
            interaxial = cmds.getAttr ( objetosSeleccionados[0]+'.INTERAXIAL' )
            zerop = cmds.getAttr ( objetosSeleccionados[0]+'.ZEROP' )
            convergence = cmds.getAttr ( objetosSeleccionados[0]+'.CONVERGENCE' )
            focallenght = cmds.getAttr ( objetosSeleccionados[0]+'.FocalLenght' )
            nearclip = cmds.getAttr ( objetosSeleccionados[0]+'.NearClip' )
            farclip = cmds.getAttr ( objetosSeleccionados[0]+'.FarClip' )

            if len (padresDeSelSplitEditado)!=0:
                for padre in padresDeSelSplitEditado:
                    coorTGlobales = cmds.xform ( padre, q =1, worldSpace = 1,  t = 1 )
                    coorRGlobales = cmds.xform ( padre, q =1, worldSpace = 1,  ro = 1)
                    coorSGlobales = cmds.xform ( padre, q =1, worldSpace = 1,  scale = 1)
                    if ((coorTGlobales [0]==0) & (coorTGlobales [1]==0) & (coorTGlobales [2]==0) & (coorRGlobales [0]==0) & (coorRGlobales [1]==0) & (coorRGlobales [2]==0) & (coorSGlobales [0]==1) & (coorSGlobales [1]==1) & (coorSGlobales [2]==1) ) == False:
                        checkTR+=1
                        checkS+=1
            if ( (checkTR==0) and (checkS==1) ) or ( len (padresDeSelSplitEditado)==0):
                print ('\n\n CONECTA !\n\n')
                mel.eval( 'file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;"  -pr "M:/PH_SCRIPTS/SCENES_RIG/IMPORTRIGS/rig_esterocam_final.ma" ')
                conectToOtherNode( objetosSeleccionados[i] , "C_E999_P00__CNT" )

                cmds.setAttr ( "C_E999_P00__CNT.INTERAXIAL", interaxial )
                cmds.setKeyframe ( "C_E999_P00__CNT.INTERAXIAL" )

                cmds.setAttr ( "C_E999_P00__CNT.ZEROP", zerop )
                cmds.setKeyframe ( "C_E999_P00__CNT.ZEROP" )

                cmds.setAttr ( "C_E999_P00__CNT.CONVERGENCE", convergence )
                cmds.setKeyframe ( "C_E999_P00__CNT.CONVERGENCE" )

                cmds.setAttr ( "C_E999_P00__CNT.FocalLenght", focallenght )
                cmds.setKeyframe ( "C_E999_P00__CNT.FocalLenght" )

                cmds.setAttr ( "C_E999_P00__CNT.NearClip", nearclip )
                cmds.setKeyframe ( "C_E999_P00__CNT.NearClip" )

                cmds.setAttr ( "C_E999_P00__CNT.FarClip", farclip )
                cmds.setKeyframe ( "C_E999_P00__CNT.FarClip" )


                renombrado ()
                lockeado ()
                indexSel+=1
            else:
                print (" \n\nBAKEA\n\n")
                mel.eval( 'file -import -type "mayaAscii"  -ignoreVersion -ra true -mergeNamespacesOnClash true -namespace ":" -options "v=0;"  -pr "M:/PH_SCRIPTS/SCENES_RIG/IMPORTRIGS/rig_esterocam_final.ma" ')
                listaKeyframes =   borrarDuplicados (   cmds.keyframe(objetosSeleccionados[i],q=True)  )
                cantidadKeyframes = len ( listaKeyframes )
                mel.eval("paneLayout -e -manage false $gMainPane")
                for i in range( cantidadKeyframes ):
                    cmds.currentTime ( listaKeyframes[i] )
                    # Q
                    PosCamVieja = cmds.xform ( objetosSeleccionados[indexSel], q=1 , ws=1 , t=1 )
                    RotCamVieja = cmds.xform ( objetosSeleccionados[indexSel], q=1 , ws=1 , ro=1 )
                    # S
                    cmds.move ( PosCamVieja[0] , PosCamVieja[1] , PosCamVieja[2] , 'C_E999_P00__CNT',a=1 )
                    cmds.rotate ( RotCamVieja[0] , RotCamVieja[1] , RotCamVieja[2] , 'C_E999_P00__CNT',a=1 )
                    cmds.setKeyframe ( "C_E999_P00__CNT.tx" )
                    cmds.setKeyframe ( "C_E999_P00__CNT.ty" )
                    cmds.setKeyframe ( "C_E999_P00__CNT.tz" )
                    cmds.setKeyframe ( "C_E999_P00__CNT.rx" )
                    cmds.setKeyframe ( "C_E999_P00__CNT.ry" )
                    cmds.setKeyframe ( "C_E999_P00__CNT.rz" )

                    cmds.setAttr ( "C_E999_P00__CNT.INTERAXIAL", interaxial )
                    cmds.setKeyframe ( "C_E999_P00__CNT.INTERAXIAL" )

                    cmds.setAttr ( "C_E999_P00__CNT.ZEROP", zerop )
                    cmds.setKeyframe ( "C_E999_P00__CNT.ZEROP" )

                    cmds.setAttr ( "C_E999_P00__CNT.CONVERGENCE", convergence )
                    cmds.setKeyframe ( "C_E999_P00__CNT.CONVERGENCE" )

                    cmds.setAttr ( "C_E999_P00__CNT.FocalLenght", focallenght )
                    cmds.setKeyframe ( "C_E999_P00__CNT.FocalLenght" )

                    cmds.setAttr ( "C_E999_P00__CNT.NearClip", nearclip )
                    cmds.setKeyframe ( "C_E999_P00__CNT.NearClip" )

                    cmds.setAttr ( "C_E999_P00__CNT.FarClip", farclip )
                    cmds.setKeyframe ( "C_E999_P00__CNT.FarClip" )

                    cmds.filterCurve  ('C_E999_P00__CNT_FocalLenght','C_E999_P00__CNT_translateX','C_E999_P00__CNT_translateY','C_E999_P00__CNT_translateZ','C_E999_P00__CNT_rotateX','C_E999_P00__CNT_rotateY','C_E999_P00__CNT_rotateZ')

                renombrado ()
                lockeado ()
                indexSel+=1

        else:
            cmds.warning (objetosSeleccionados[indexSel] + " NO ES UNA CURVA")
    mel.eval("paneLayout -e -manage true $gMainPane")
else:
    cmds.warning ("NO HAY NADA SELECCIONADO. O LAS CURVAS ESTAN MAL NOMBRADAS y/o NO TIENEN KEYS. LAS SELECCIONE PARA QUE LAS MIRES.")
    cmds.select (objsConProb)
