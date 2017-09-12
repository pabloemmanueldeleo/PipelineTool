import maya.cmds as cmds
#Lista de nodos para renombrar.
listNodes={
#UtilityNodes:
'MMX': 'multMatrix',
'CND': 'condition',
'MDN': 'multiplyDivide',
'MDL': 'multDoubleLinear',
'PLS': 'plusMinusAverage',
'DSN': 'distanceDimShape',
'ANG': 'angleBetween',
'CPM': 'closestPointOnMesh',
'VCP': 'vectorProduct',
'PTH': 'motionPath',
'POC': 'pointOnCurve',
'CPC': 'closestPointOnCurve',
'CRVI': 'curveInfo',
'RCT': 'rayContact',
'DIS': 'displayNode',
'BLC': 'blendColors',
'DSB': 'distanceBetween',
'CLM': 'clamp',
'TRF': 'transform',
'BLW': 'blendWeighted',
'SPI': 'samplerInfo',
'RVS': 'reverse',
'3DP': 'place3dTexture',
'STR': 'setRange',
'2DP': 'place2dTexture',
'CON': 'contrast',
'GAM': 'gammaCorrect',
'H2R': 'hsvToRgb',
'LUM': 'luminance',
'RMP': 'remapColor',
'RMH': 'remapHsv',
'RMV': 'remapValue',
'R2H': 'rgbToHsv',
'SMR': 'smear',
'SFL': 'surfaceLuminance',
'PRT': 'particleSamplerInfo',
'IMP': 'imagePlane',
'BMP2D': 'bump2d',
'BMP3D': 'bump3d',
'HEI': 'heightField',
'PRJ': 'projection',
'ADD':'addDoubleLinear',
'EXPR':'expression',
#Materials:
'MTBLN': 'blinn',
'MTANI': 'anisotropic',
'MTHAI': 'hairTubeShader',
'MTLMB': 'lambert',
'MTLAY': 'layeredShader',
'MTOCE': 'oceanShader',
'MTPHO': 'phong',
'MTPHOE': 'phongE',
'MTRAM': 'rampShader',
'MTSHA': 'shadingMap',
'MTSUR': 'surfaceShader',
'MTBCK': 'useBackground',
'SHDG':'shadingEngine',
'STNC':'stencil',
#Textures:
'TXBUL': 'bulge',
'TXCHE': 'checker',
'TXCLT': 'cloth',
'TXFIL': 'file',
'TXF2D': 'fluidTexture2D',
'TXFRA': 'fractal',
'TXGRI': 'grid',
'TXMOV': 'movie',
'TXMOU': 'mountain',
'TXNOI': 'noise',
'TXOCE': 'ocean',
'TXPSD': 'psdFileTex',
'TXRAM': 'ramp',
'TXWAT': 'water',
'TXBRO': 'brownian',
'TXCLO': 'cloud',
'TXCRA': 'crater',
'TXF3D': 'fluidTexture3D',
'TXGRA': 'granite',
'TXLEA': 'leather',
'TXMAR': 'marble',
'TXROC': 'rock',
'TXSNO': 'snow',
'TXSOL': 'solidFractal',
'TXSTU': 'stucco',
'TXVOL': 'volumeNoise',
'TXWOO': 'wood',
'TXLAY': 'layeredTexture',
#MentalRay:
'MIAM':'mia_material',
'MIAMX':'mia_material_x',
'MIAMXP':'mia_material_x_passes',
'SSS': 'misss_fast_skin_maya',
'SSTEX': 'mentalrayTexture',
'LMAP': 'misss_fast_lmap_maya',
'BPASST': 'mib_passthrough_bump_map',
'TVECT': 'mib_texture_vector',
'BBYN': 'mib_bump_basis',
'MRIBL': 'mentalrayIblShape',
#Arnold:
'AISDL':'aiSkyDomeLight',
'AIRSW':'aiRaySwitch',
'AIBRN':'aiBarndoor',
'AIGBO':'aiGobo',
'AILBL':'aiLightBlocker',
'AILDK':'aiLightDecay',
'AIDIS':'aiDisplacement',
'AIAO':' aiAmbientOcclusion',
'AIHIR':'aiHair',
'AISDR':'aiStandard',
'AIUTL':'aiUtility',
'AIWRE':'aiWireframe',
'AIFOG':'aiFog',
'AIVSC':'aiVolumeScattering',
'AISKY':'aiSky',
'AIRSW':'aiRaySwitch',
'AIUDC':'aiUserDataColor',
#Alshader:
'ALFN':'alFlowNoise'
}
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # Si esta lo agrego
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def ph_renameHierarchyShader():

    shaders = []
    renameList = []
    
    #Nodos de maya listado
    shaderList = cmds.listNodeTypes('shader')
    texList = cmds.listNodeTypes ('texture')
    utilList = cmds.listNodeTypes ('utility')
    
    
    #Lista de nodos que no se deben cambiar
    defaultShaders = {"initialShadingGroup",
                      "initialParticleSE",
                      "lambert1",
                      "particleCloud1",
                      "shaderGlow1",
                      "time1",
                      }
    
    #Comprobar si son shaders lo que selecciono
    for sel in cmds.ls(sl=True):
        for shaderType in shaderList:
            selType = cmds.nodeType(sel)
            #Si es un shader agregar a la lista de shader
            if shaderType and selType == shaderType:
                shaders.append(sel)
            shaders = remove_duplicates(shaders)
    
    print 'Seleccionastes ' + str( len( shaders ) ) + ' shaders.'
    
    #Si el nodo existe, lo borro de la lista.
    if 'displacementShader' in shaderList:
        #Lo busco en la lista
        indexNodo = shaderList.index('displacementShader')
        del shaderList[indexNodo]
        print 'Se borro el nodo displacemetShader exitosamente.' + "\n"
    
    #Uno las listas de nodos a renombrar
    renameList = texList + utilList
    
    #Funcion para Eliminar duplicados en la lista
    
    shaders = remove_duplicates(shaders)
    print 'Se borraron shaders duplicados en la seleccion.'
    
    #Variables colector de nodos y nombre de shaders nuevos
    listNodesHeredados = []
    newShaderNameList=[]
    
    #Por cada shader busco el nombre y saco para poner el suf y pref
    for shader in shaders:
        #Posicion de la lista
        cont          =+ 0
        #Obtengo el prefix y sustituyo por nada
        shdSufixList  = ("_mat","Mtl","_Mat","Mat",'__mat','__Mat','__MAT','__SHD', '_SHD')
        posSufixList  = ('__','_')
        curSG  = []
        shdNamePrefix = shader.split( shdSufixList[ cont ] )[-1]
        #Guardo el nombre del nodo
        shaderName    = shader.split( posSufixList[ cont ] )[0]
        #Divido el nombre con ultima palabra separada
        for posiblesuff in shdSufixList or posSufixList:
    
            if posiblesuff == shdNamePrefix:
                print 'No es necesario cambiar el nombre.'
            else:
                shader = cmds.rename(shader, shaderName.upper() + "__SHD")
    
        #Leeo todas las conecciones del shader en el hyperShade hacia la derecha-->
        shaderNetworks = cmds.hyperShade(objects=(shader),
                                            noTransforms=True, noShapes=True,
                                            listUpstreamNodes = (shader),
                                            listDownstreamNodes = (shader))
    
        #Leeo todas las conecciones del shader en el hyperShade hacia la izquierda <-- 
        listNodesHeredados = cmds.hyperShade(objects=(shader),
                                            noTransforms=True,
                                            noShapes=True,
                                            listUpstreamNodes = (shader))
    
        #Si el nodo existe, lo borro de la lista.
        if 'defaultColorMgtGlobals' in listNodesHeredados:
            #Lo busco en la lista
            xNodo = listNodesHeredados.index('defaultColorMgtGlobals')
            del listNodesHeredados[xNodo]
            print 'Se borro el nodo defaultColorMgtGlobals exitosamente.' + "\n"
    
        listNodesHeredados = remove_duplicates( listNodesHeredados )
        print 'Hay' + str( shaders )
        #busco el shaderGrop
        for shaderNetwork in shaderNetworks:
            nodo = cmds.nodeType( shaderNetwork )
            if nodo == 'shadingEngine':
                curSG = shaderNetwork
                newSGname = cmds.rename( curSG, (shaderName.upper()) + '__SGP' )
                cmds.warning( 'Se cambio el nombre del nodo de shadingGroup a :' + newSGname )
            else:
                print shaderName + ' no tiene shadingGroup asignado.'
            
        #newShaderNameList.append( shader )
        sizeSW = range(len(listNodesHeredados ))
    
        for index in listNodesHeredados:
            #print index
            thisNodeType = str( cmds.nodeType( index ) )
    
            for node in list(sizeSW):
                #chequeamo si el nodo es una refenrencia para ver si esto se puede renombrar
                refCheck = cmds.referenceQuery( listNodesHeredados[node], isNodeReferenced=True )
                if( refCheck ):
                    print ( listNodesHeredados[node] + " solo puede ser renombrado en el archivo original por que es una referencia.\n" )
                else:
                    thisNodeType = cmds.nodeType( listNodesHeredados[node] )
                    nNode=''
                    #busco en el diccionario y renombro si existe el nodo
                    for suf, nod in listNodes.items():
                        #Filtros para renombrar
                        if thisNodeType in nod:
                            nNode=suf
                            cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')