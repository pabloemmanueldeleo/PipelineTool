import maya.cmds as mc
import maya.mel as mel

#Busco el shaderGroup de un material
def obtenerSG(shader=None):
    if shader:
        if mc.objExists(shader):
            sgq = mc.listConnections(shader, d=True, et=True, t='shadingEngine')
            if sgq:
                return sgq[0]
    return None
#Asigna material a una lista de objetos.
def asignarSHDaListaObjetos(objList=None, shader=None):
    shaderSG = obtenerSG(shader)
    if objList:
        if shaderSG:
            mc.sets(objList, e=True, forceElement=shaderSG)
        else:
            print 'NO ENCONTRO EL SHADING GROUP.'
    else:
        print 'CHABON SELECCIONA UNO O MAS OBJETOS.'
#Override de render layer pasandole solo un material.
def renderLayerConTodoUnMaterial(layerName=None,mat=None):
    mel.eval('hookShaderOverride('+'"'+layerName+'"'+',"",'+'"'+str(mat)+'"'+');')
#Seteo y hace Override de atributos del render options de arnold
def overrideArnoldRenderOptions(renderLayer=None,attr=None,value=None):
    try:
        mc.editRenderLayerAdjustment('defaultArnoldRenderOptions.'+str(attr), layer=renderLayer)
        mc.setAttr('defaultArnoldRenderOptions.'+str(attr), value)
    except:
        print 'Puede que ese atributo no exista o este mal escrito.'



listaSTANDIN=mc.ls(type='aiStandIn')
listaMESH=mc.ls(type='mesh')
listAOVs=mc.ls(type='aiAOV')

mat="SHADOW__SHD"
layerName="CHARS_SHADOWS_"

mc.setAttr(mat+'.specular1Strength',0)

mc.select(listaSTANDIN,listaMESH)
RLAY=mc.createRenderLayer( name=layerName,g=False)
mc.select(cl=1)

for MSH in listaMESH:
    mc.setAttr(str(MSH)+'.castsShadows',0)
    mc.setAttr(str(MSH)+'.receiveShadows',0)

for STANDIN in listaSTANDIN:
    mc.setAttr(str(STANDIN)+'.overrideShaders', 1)
    mc.setAttr(str(STANDIN)+'.castsShadows', 0)
    mc.setAttr(str(STANDIN)+'.overrideCastsShadows', 1)

#Set AOVS visibility
for AOV in listAOVs:
    mc.setAttr(str(AOV)+'.enabled',0)
    if 'shadow' in AOV or 'OCCLUSION' in AOV:
        mc.setAttr(str(AOV)+'.enabled',1)

#set Arnold Render Options
overrideArnoldRenderOptions(layerName,'GIRefractionSamples',0)
overrideArnoldRenderOptions(layerName,'GIDiffuseSamples',0)
overrideArnoldRenderOptions(layerName,'GIGlossySamples',0)
overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
overrideArnoldRenderOptions(layerName,'GIDiffuseDepth',0)
overrideArnoldRenderOptions(layerName,'GIGlossyDepth',0)
overrideArnoldRenderOptions(layerName,'GIReflectionDepth',0)
overrideArnoldRenderOptions(layerName,'GIDiffuseDepth',0)
overrideArnoldRenderOptions(layerName,'GIRefractionDepth',0)


asignarSHDaListaObjetos(listaSTANDIN,mat)
asignarSHDaListaObjetos(listaMESH,mat)
renderLayerConTodoUnMaterial(layerName,mat)
