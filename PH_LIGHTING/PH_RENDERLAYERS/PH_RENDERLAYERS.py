# -*- encoding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import sys


path='M:\PH_SCRIPTS\PH_LIGHTING\PH_RENDERLAYERS'
if not path in sys.path:
    sys.path.append(path)
try:
    import PH_PACKSHADERS
except ImportError:
    print 'No pude cargar el modulo de shader pack'

#Busco el shaderGroup de un material
def obtenerSG(shader=None):
    if shader:
        if mc.objExists(shader):
            sgq = mc.listConnections(shader, d=True, et=True, t='shadingEngine')
        else:
            agq=shader
        if sgq:
            print sgq
            return sgq[0]
    return None

#Asigna material a una lista de objetos.
def asignarSHDaListaObjetos(objList=None, shader=None):
    shaderSG = obtenerSG(shader)
    if objList:
        if shaderSG:
            try:
                mc.sets(objList, e=True, forceElement=shaderSG)
            except:
                pass
        else:
            print 'NO ENCONTRO EL SHADING GROUP.'

#Override de render layer pasandole solo un material.
def renderLayerConTodoUnMaterial(layerName=None,mat=None):
    mel.eval('hookShaderOverride('+'"'+layerName+'"'+',"",'+'"'+str(mat)+'"'+');')

#conecta o re conecta
def conectar(el=None,con=None):
    try:
        desconectado=False
        conectado=False
        if mc.isConnected(el,con):
            mc.warning('EXISTE UNA CONEXION ENTRE EL ('+ el +') CON ('+con+')')
            mc.disconnectAttr(el,con)
            mc.warning('DESCONECTE EL ('+ el +') CON ('+con+')')
            desconectado=True
            conectado=True
        else:
            mc.warning('NO EXISTE LA CONEXION ENTRE (' + el+') CON (' + con+')')
            conectado=False
        if desconectado:
            mc.connectAttr(el,con,f=True)
            mc.warning('CONEXION CON EXICO DE ('+ el +') CON ('+con+')')
            conectado=True
        return conectado
    except:
        mc.warning('PUEDE QUE NO EXISTA ESA CONEXION O ESTA MAL NOMBRADA')

#Seteo y hace Override de atributos del render options de arnold
def overrideArnoldRenderOptions(renderLayer=None,attr=None,value=None):
    mc.editRenderLayerAdjustment('defaultArnoldRenderOptions.'+str(attr), layer=renderLayer)
    mc.setAttr('defaultArnoldRenderOptions.'+str(attr), value)

def createAov(nameNodoAov=None,nombreAOV=None):
    aovLGRP=cmds.createNode('aiAOV',name=nombreAOV)
    cmds.setAttr(aovLGRP)

    aov_list = mc.getAttr('defaultArnoldRenderOptions.aovList',size=True)

    someInListID=0
    for aov in range(aov_list):
        #mc.listConnections('defaultArnoldDriver.message')
         if mc.isConnected(aovLGRP+'.message','defaultArnoldRenderOptions.aovList[' + str(aov) + ']'):
            someInListID+=1
    #Conexion con ID
    if  someInListID<=0:
        mc.connectAttr( aovLGRP+'.message','defaultArnoldRenderOptions.aovList[' + str(aov_list) + ']', force=True)
        mc.setAttr( aovLGRP+'.type',5 )
        mc.setAttr( aovLGRP+'.name',nombreAOV, type='string' )
        mc.connectAttr('defaultArnoldDriver.message', aovLGRP+'.outputs[0].driver',force=True)
        mc.connectAttr('defaultArnoldFilter.message', aovLGRP+'.outputs[0].filter',force=True)
        #mc.connectAttr( IDSHD+'.outColor', nameNodoAov+'.defaultValue',force=True)
        mc.select(cl=1)
    else:
        print 'Ya existe la conexion entre '+nombreAOV

def crearShadowShd():
    msg='Si no existe el SHADOW__SHD no podras seguir.\nÂ¿Quieres que lo cree por ti?'
    mc.warning(msg)
    configButtom=mc.confirmDialog(title='SHADOW__SHD',message=msg, button=['Sipi','No'], defaultButton='Sipi', cancelButton='No', dismissString='No',icon='icon')
    if configButtom == 'Sipi':
        try:
            nombreNodoaiaov = mc.createNode( "alSurface", n= 'SHADOW__SHD')
            mc.setAttr(nombreNodoaiaov+'.specular1Strength',0)
        except Exception:
            mc.warning('Puede que no tengas el alSurface para usarlo.')
    if configButtom =='No':
        mc.warning('Se cancelo la creacion del SHADOW__SHD')
    return configButtom

def onOffAOV(AovON=None,listAOVs=None):
    #prende y apaga aov y hace overraid
    state=False
    if listAOVs:
        copado1=False
        for AOV in listAOVs:
            mc.editRenderLayerAdjustment(str(AOV)+'.enabled')
            mc.setAttr(str(AOV)+'.enabled',0)
        for AOV in listAOVs:
            for avosName in AovON:
                getAOV=mc.getAttr(AOV+'.name')
                if str(avosName) in str(getAOV):
                    mc.setAttr(str(AOV)+'.enabled',1)
                    print 'ameo Te deje con overraid y prendido el ' + str(getAOV)
                copado1=True
                state=True
        if copado1 == False:
            mc.warning('No encontre un aov con el nombre '+ avosName)
        return state
    else:
        mc.warning('No existe ningun aov creado.')
        return state

##########################################################
#LAYERS
##########################################################

#LAYER SHADOW
def renderLayerShadow(*args):
    matFix='lambert1'
    mat="SHADOW__SHD"
    layerName="CHARS_SHADOWS"
    states=[False,False,False,False,False,False]

    if mc.objExists(mat):

        try:
            mc.setAttr(mat+'.specular1Strength',0)
        except:
            pass
        states[0]=True

        listaSTANDIN=mc.ls(type='aiStandIn')
        listaMESH=mc.ls(type='mesh')
        listAOVs=mc.ls(type='aiAOV')

        if mc.objExists(layerName):
            mc.warning('Ya se creo el renderLayer '+layerName)
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            states[1]=True
        else:
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            #creo el renderLayer con mesh y standin de toda la escena.
            mc.select(listaSTANDIN,listaMESH)
            RLAY=mc.createRenderLayer( name=layerName,g=False)
            mc.select(cl=1)
            mc.warning('Ahi te cree un renderLayer llamado ' + layerName)
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            states[1]=True

        #seteo que el mesh no emita sombras ni reciba
        if listaMESH:
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            for MSH in listaMESH:
                #MSH=MSH.encode('latin-1')
                mc.setAttr(str(MSH)+'.castsShadows',0)
                mc.setAttr(str(MSH)+'.receiveShadows',1)
                mc.setAttr(str(MSH)+'.primaryVisibility',1)
            states[2]=True

        #seteoque le de bola a los shaders del mismo standing, que no genere sombras
        if listaSTANDIN:
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            for STANDIN in listaSTANDIN:
                mc.setAttr(str(STANDIN)+'.overrideShaders', 1)
                mc.setAttr(str(STANDIN)+'.castsShadows', 0)
                mc.setAttr(str(STANDIN)+'.overrideCastsShadows', 1)
            states[3]=True

        #Set AOVS visibility
        if listAOVs:
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            v=onOffAOV(['shadow','OCCLUSION'],listAOVs)

        if v:
            states[4]=True
        else:
            states[4]=False

        if mc.objExists(layerName):
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
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
            overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
            states[5]=True
        else:
            mc.warning('No existe el layer '+layerName)

        #SI NO SE CUMPLEN TODAS LAS CONDICIONES NO SE AGREGARAN LOS ITEMS AL LAYER
        try:
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            if 'aiAOV_shadow_group_1' in listAOVs:
                conectar('SHADOW__SHD.message','aiAOV_shadow_group_1.defaultValue')
            else:
                mc.warning('NO SE ENCONTRO EL aiAOV_shadow_group_1 EN LOS AOVS')

            #Aplico material a los standins
            asignarSHDaListaObjetos(listaSTANDIN,matFix)
            asignarSHDaListaObjetos(listaSTANDIN,mat)
            #Aplico material a los meshes
            asignarSHDaListaObjetos(listaMESH,matFix)
            asignarSHDaListaObjetos(listaMESH,mat)
            #por las dudas hago un override al renderlayer con el material
            renderLayerConTodoUnMaterial(layerName,mat)
        except:
            states=[False,False,False,False,False,False]

    else:
        coco=crearShadowShd()
        if coco=='Sipi':
            renderLayerShadow()

#LAYER LIGHT
def renderLayerLighting(*args):
    matFix='lambert1'
    mat="SHADOW__SHD"
    layerName="CHARS_LIGHTS"
    states=[False,False,False,False,False,False]

    if mc.objExists(mat):
        mc.setAttr(mat+'.specular1Strength',0)
        states[0]=True

        listaSTANDIN=mc.ls(type='aiStandIn')
        listaMESH=mc.ls(type='mesh')
        listAOVs=mc.ls(type='aiAOV')

        if mc.objExists(layerName):
            mc.warning('Ya se creo el renderLayer '+layerName)
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            states[1]=True
        else:
            #creo el renderLayer con mesh y standin de toda la escena.
            mc.select(listaSTANDIN,listaMESH)
            RLAY=mc.createRenderLayer( name=layerName,g=False)
            mc.select(cl=1)
            mc.warning('Ahi te cree un renderLayer llamado ' + layerName)
            mc.editRenderLayerGlobals( currentRenderLayer=layerName )
            states[1]=True

        #seteo que el mesh no emita sombras ni reciba
        if listaMESH:
            for MSH in listaMESH:
                #MSH=MSH.encode('latin-1')
                mc.setAttr(str(MSH)+'.castsShadows',1)
                mc.setAttr(str(MSH)+'.receiveShadows',1)
                mc.setAttr(str(MSH)+'.primaryVisibility',1)
            states[2]=True

        #seteoque le de bola a los shaders del mismo standing, que no genere sombras
        if listaSTANDIN:
            for STANDIN in listaSTANDIN:
                mc.setAttr(str(STANDIN)+'.overrideShaders', 1)
                mc.setAttr(str(STANDIN)+'.castsShadows', 1)
                mc.setAttr(str(STANDIN)+'.overrideCastsShadows', 1)
            states[3]=True

        #Set AOVS visibility
        if listAOVs:
            v=onOffAOV(['light_group'],listAOVs)
            if v:
                states[4]=True
        else:
            states[4]=False

        if mc.objExists(layerName):
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
            overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
            states[5]=True
        else:
            mc.warning('No existe el layer '+layerName)

        #SI NO SE CUMPLEN TODAS LAS CONDICIONES NO SE AGREGARAN LOS ITEMS AL LAYER
        if states==[True,True,True,True,True,True]:
            #Aplico material a los standins
            asignarSHDaListaObjetos(listaSTANDIN,matFix)
            asignarSHDaListaObjetos(listaSTANDIN,mat)
            #Aplico material a los meshes
            asignarSHDaListaObjetos(listaMESH,matFix)
            asignarSHDaListaObjetos(listaMESH,mat)
            #por las dudas hago un override al renderlayer con el material
            renderLayerConTodoUnMaterial(layerName,mat)
        else:
            states=[False,False,False,False,False,False]
    else:
        coco=crearShadowShd()
        if coco=='Sipi':
            renderLayerLighting()

def forceShadow():
    layerName="CHARS_SHADOWS"
    mat="SHADOW__SHD"
    matFix='lambert1'
    listaSTANDIN=mc.ls(type='aiStandIn')
    listaMESH=mc.ls(type='mesh')
    #Aplico material a los standins
    asignarSHDaListaObjetos(listaSTANDIN,matFix)
    asignarSHDaListaObjetos(listaSTANDIN,mat)
    #Aplico material a los meshes
    asignarSHDaListaObjetos(listaMESH,matFix)
    asignarSHDaListaObjetos(listaMESH,mat)
    #por las dudas hago un override al renderlayer con el material
    renderLayerConTodoUnMaterial(layerName,mat)
##########################################################
#EXTRA
##########################################################

#selecciono la hiearchy dentro de la seleccion
def selectH(*args):
    geoH=[]
    listSel=[]
    objs=mc.ls(sl=1)
    for obj in objs:
        geos=mc.listRelatives(mc.listRelatives(obj,allParents=True,fullPath=True)[0],parent=True)
        for g in geos:
            chld=mc.listRelatives(g, allDescendents=True)
            for c in chld:
                geoH.append(c)
    mc.select(geoH)
    return geoH

#seteo los atributos shadow
def reciveS(*args):
    global switch
    sel=mc.ls(sl=1)
    if sel:
        for o in sel:
            mc.setAttr(o+'.castsShadows',1)
            mc.setAttr(o+'.receiveShadows',1)
            mc.setAttr(o+'.primaryVisibility',0)

#seteo los atributos shadow
def primaryV(*args):
    global switch
    sel=mc.ls(sl=1)
    if sel:
        for o in sel:
            mc.setAttr(o+'.castsShadows',1)
            mc.setAttr(o+'.receiveShadows',1)
            mc.setAttr(o+'.primaryVisibility',1)

def crearAttr(name=None,defauld=None,obj=None):
    if obj==None:
        sel=mc.ls(sl=1)
    else:
        sel=obj
    for s in sel:
        try:
            s=cmds.listRelatives(s,children=True)[0]
        except:
            s=s
        if mc.objectType(s) == 'directionalLight' or mc.objectType(s)=='pointLight' or mc.objectType(s)=='spotLight':
            attrs=mc.listAttr(s)
            for a in attrs:
                if not str(a)==name:
                    ojo=False
                else:
                    ojo=True
            if not ojo:
                i = pm.ls(s)
                attrNew=i[0].addAttr(name, at='long',dv=defauld)
                #attrNew=mc.addAttr(s,ln=name,at='byte',dv=defauld)
                mc.warning( 'Se creo un atributo nuevo para la luz llamado ' + str(name))
            else:
                mc.warning('ya existe un atributo con el nombre '+ a)
        else:
            mc.warning(s+' no es un shape')

def attr(*args):

    crearAttr('mtoa_constant_lightGroup',1)

def cleanUp(*args):
    print 'cleanUp'
    try:
        mel.eval('source "M:/PH_SCRIPTS/PH_LIGHTING/PH_RENDERLAYERS/fixRenderLayerOutAdjustmentErrors.mel"')
        mel.eval('fixRenderLayerOutAdjustmentErrors;')
    except:
        pass

def aovshaders(*args):
    reload(PH_PACKSHADERS)
    PH_PACKSHADERS.packShaders()

def barraProgresoSuma(steps=1,condicion=False):
    global barraProgreso
    mc.progressBar( barraProgreso,edit=True,beginProgress=True,    isInterruptable=True,status='ameeoo dejame penzar...', maxValue=100 )
    while mc.progressBar(barraProgreso, query=True,progress=True) < 100:
        mc.progressBar(barraProgreso, edit=True, step=int(steps))
        if mc.progressBar(barraProgreso, query=True, isCancelled=True ):
            break
    else:
        mc.progressBar(barraProgreso, edit=True, endProgress=True)

def selectStanding(*args):
    listaSTANDIN=mc.ls(type='aiStandIn')
    mc.select(listaSTANDIN)

def selectMesh(*args):
    listaMESH=mc.ls(type='mesh')
    mc.select(listaMESH)
def seteoRenderArnold(*args):
    #para todas las escenas.
    seteos=[
    mc.setAttr('defaultArnoldDriver.ai_translator', 'exr', type='string'),
    mc.setAttr('defaultArnoldDriver.exrCompression', 3),
    mc.setAttr('defaultArnoldDriver.halfPrecision', 1),
    mc.setAttr('defaultArnoldDriver.autocrop', 0),
    mc.setAttr('defaultRenderGlobals.periodInExt', 2),
    mc.setAttr('defaultRenderGlobals.extensionPadding', 4),
    mc.setAttr('defaultResolution.width', 2048),
    mc.setAttr('defaultResolution.height', 858),
    mc.setAttr('defaultResolution.deviceAspectRatio', 2.387),
    mc.setAttr('defaultArnoldRenderOptions.AASamples', 4),
    mc.setAttr('defaultArnoldRenderOptions.GIDiffuseSamples', 0),
    mc.setAttr('defaultArnoldRenderOptions.GIGlossySamples', 1),
    mc.setAttr('defaultArnoldRenderOptions.GIRefractionSamples', 1),
    mc.setAttr('defaultArnoldRenderOptions.sssBssrdfSamples', 0),
    mc.setAttr('defaultArnoldRenderOptions.volumeIndirectSamples', 0),
    mc.setAttr('defaultArnoldRenderOptions.GITotalDepth', 6),
    mc.setAttr('defaultArnoldRenderOptions.GIDiffuseDepth', 0),
    mc.setAttr('defaultArnoldRenderOptions.GIGlossyDepth', 1),
    mc.setAttr('defaultArnoldRenderOptions.GIReflectionDepth', 1),
    mc.setAttr('defaultArnoldRenderOptions.GIRefractionDepth', 4),
    mc.setAttr('defaultArnoldRenderOptions.textureAutomip', 0),
    mc.setAttr('defaultArnoldRenderOptions.textureAcceptUnmipped', 0),
    mc.setAttr('defaultArnoldRenderOptions.autotile', 0),
    mc.setAttr('defaultArnoldRenderOptions.textureAcceptUntiled', 0),
    mc.setAttr('defaultArnoldRenderOptions.use_existing_tiled_textures', 1),
    mc.setAttr('defaultArnoldRenderOptions.textureMaxMemoryMB', 8192)]


##########################################################
#UI
##########################################################

#ventana de PH_MANAGER_RENDERLAYER
def winLayer():
    winRenderLayer='PH_RENDERLAYER'
    v=' v1.7.4'
    global barraProgreso

    if mc.window(winRenderLayer, q=True, exists=True):
        mc.deleteUI(winRenderLayer)
    boxB=150
    boxB2=80
    boxB3=30
    verdemarino=(0.24,0.75,0.5)
    azul=(0.15,0.27,0.49)
    naranja=(0.85,0.67,0.2)
    mc.window(winRenderLayer, title=winRenderLayer + v)
    mc.rowColumnLayout(numberOfRows=1)
    mc.rowColumnLayout(numberOfColumns=1)
    mc.separator(height=10, style='singleDash')
    mc.text(label='RENDER LAYERS')
    mc.separator(height=10, style='singleDash')
    mc.button(label='(CREAR) CHARS_SHADOW',c=renderLayerShadow,width=boxB,height=boxB2,backgroundColor=verdemarino,enable=0)
    mc.button(label='(CREAR) CHARS_LIGHTS',c=renderLayerLighting,width=boxB,height=boxB2,backgroundColor=azul,enable=0)
    mc.separator(height=10, style='singleDash')
    mc.text(label='SET GEO')
    mc.separator(height=10, style='singleDash')
    mc.button(label='SELECT HIEARCHY',c=selectH,annotation='Selecciona toda la jerarqui­a de la seleccion.',width=boxB2,height=boxB3)
    mc.button(label='SELECT ALL MESH',c=selectMesh,annotation='Selecciona todos los mesh en la escena.',width=boxB2,height=boxB3)
    mc.button(label='SELECT ALL STANDIN',c=selectStanding,annotation='Selecciona todos los standin en la escena.',width=boxB2,height=boxB3)
    mc.separator(height=10, style='singleDash')
    mc.text(label='ATTRIBUTE SPREAD SHEET')
    mc.separator(height=10, style='singleDash')
    mc.button(label='RECEIVE SHADOW',c=reciveS,annotation='Prende: castsShadows,receiveShadows\nApaga: primaryVisibility',width=boxB2,height=boxB3)
    mc.button(label='PRIMARY VISIBILITY',c=primaryV,annotation='Prende: castsShadows,receiveShadows,primaryVisibility',width=boxB2,height=boxB3)
    mc.button(label='ADD ATTRIBUTE',c=attr,annotation='Te crea un atributo nuevo en las luces seleccionadas.',width=boxB2,height=boxB3)
    mc.separator(height=10, style='singleDash')
    mc.text(label='AOVs+SHADERS ESENCIALES')
    mc.separator(height=10, style='singleDash')
    mc.button(label='PACK AOVs+SHADERS',c=aovshaders,annotation='Crea varios shader de arnold y aov (Asegurate que tengas el arnold como motor principal).')
    mc.text(label=' ')
    mc.rowLayout(nc=3)
    mc.text(label=' Progreso ')
    barraProgreso=mc.progressBar( width=150, minValue=0, maxValue=100)
    mc.setParent('..')
    mc.text(label=' ')
    #mc.button(label='CLEANUP LAYERS',c=cleanUp,annotation='Trata de limpiar las conexiones no validas de los layers,siempre chequiar por las dudas.',width=boxB,height=boxB2,backgroundColor=naranja)
    mc.showWindow(winRenderLayer)
winLayer()
