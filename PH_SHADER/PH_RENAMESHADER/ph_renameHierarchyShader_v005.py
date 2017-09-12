import maya.cmds as cmds

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
    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
            # Si esta lo agrego
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output
    
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
                    #Filtros para renombrar
                    if thisNodeType == "place2dTexture":
                        nNode = "P2D"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == "place3dTexture":
                        nNode = "P3D"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == "shadingEngine":
                        nNode = "SGP"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == "displacementShader":
                        nNode = "DISPSH"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'file':
                        nNode = 'FILE'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == "bump2d":
                        nNode = "BP2D"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == "aiBump2d":
                        nNode = "AIBP2D"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'noise':
                        nNode = 'NOISE'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == "aiUserDataColor":
                        nNode = "AIUDC"
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'layeredTexture':
                        nNode = 'LAYTX'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'remapHsv':
                        nNode = 'REMPH'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'multiplyDivide':
                        nNode = 'MPD'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'remapValue':
                        nNode = 'REMV'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'plusMinusAverage':
                        nNode = 'PMA'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'ramp':
                        nNode = 'RAMP'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')
                    elif thisNodeType == 'stucco':
                        nNode = 'STC'
                        cmds.rename(listNodesHeredados[node], shaderName.upper() + '_' + nNode + '_')