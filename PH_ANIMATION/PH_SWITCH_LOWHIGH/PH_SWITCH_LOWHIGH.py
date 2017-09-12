import maya.cmds as mc

def start():
    sel=mc.ls(type='mesh')
    for o in sel:
        mc.displaySmoothness(o,divisionsU= 0,divisionsV= 0,pointsWire= 4,pointsShaded= 1,polygonObject= 1)
        mc.setAttr(o+'.displaySubdComps',0)
        mc.setAttr(o+'.smoothLevel',1)
        try:
            mc.setAttr(o+'.aiSubdivIterations',2)
            print 'copado'
        except:
            pass

def switch():
    objS = mc.ls (sl=1)
    if len (objS)!=0 and ":" in objS[0]:
        try:
            grupoObjQ = mc.listRelatives (objS[0],p=1)
            splitPath = grupoObjQ[0].split(":")
            pathAux=''
            for i in range( len(splitPath)-1 ):
                pathAux+=splitPath[i]+":"
            estadoVisQ = mc.getAttr (pathAux+"PROXY_Geometries.visibility")

            for obj in objS:
                if ":" in obj:
                    grupoObj = mc.listRelatives (obj,p=1)
                    splitPath = grupoObj[0].split(":")
                    pathAux=''
                    for i in range( len(splitPath)-1 ):
                        pathAux+=splitPath[i]+":"
                    print pathAux+"PROXY_Geometries.visibility"
                    mc.setAttr (pathAux+"PROXY_Geometries.visibility", not (estadoVisQ) )
                    mc.setAttr (pathAux+"Geometries.visibility", estadoVisQ )
                else:
                    print obj, " NO TIENE NAMESPACE."
        except:
            pass
    else:
        mc.warning("NO TENES SELECCION O ALGO EN LA SELECCION NO TIENE NAMESPACE")
