import maya.cmds as cmds
import maya.mel as mel
from functools import partial
lights = []
swatches = []
main_layout = ''
light_layout = ''
opt = 0
WIDTH = 800
HEIGHT = 600
#contadores para nombre de luz
contSpot=0
contDir=0
contPoint=0
contArea=0
contAmb=0

def UI(*args):
    """creates window for UI"""
    # check to see if window exists
    if (cmds.window('PH_MANAGERLIGHTS', exists=True)):
        cmds.deleteUI('PH_MANAGERLIGHTS')

    # create window
    window = cmds.window('PH_MANAGERLIGHTS', title='PH_MANAGERLIGHTS', w=WIDTH, h=HEIGHT, mxb=False, mnb=False, sizeable=True)
    
    create_layout()
    
    cmds.showWindow(window)
    
def create_layout():
    """generates the rows/columns/buttons for the UI"""
    num_lights = len(lights)
    global main_layout
    main_layout = cmds.scrollLayout(verticalScrollBarThickness=16, horizontalScrollBarThickness=0)
    # create buttons
    cmds.rowLayout( numberOfColumns=10, h=40)
    cmds.button(label='Spotlight', w=80, command=partial(add_light, 'spot'))
    cmds.button(label='Directional', w=80, command=partial(add_light, 'dir'))
    cmds.button(label='Point', w=80, command=partial(add_light, 'point'))
    cmds.button(label='Ambient', w=80, command=partial(add_light, 'amb'))
    cmds.button(label='Area', w=80, command=partial(add_light, 'area'))
    cmds.text(label='', w=40)
    cmds.button(label='Organize', w=80, command=organize)
    cmds.button(label='Basic Lights', w=80, command=basic)
    cmds.text(label='', w=40)
    cmds.button(label='Refresh', w=80, al='right', command=refresh)
    cmds.setParent('..')
    # create column labels
    cmds.rowColumnLayout(nc=12, 
                         columnWidth=[(1, 60), (2, 150), (3, 100), (4, 100), (5, 60), (6, 60), (7, 60), (8, 60), (9, 60), (10, 100), (11, 60), (12, 60)],
                         cs=[(1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10)])
    cmds.text(label='Enabled', w=60, al='left')
    cmds.text(label='Name', w=130, al='left')
    cmds.text(label='Type', w=60, al='left')
    cmds.text(label='Intensity', al='left')
    cmds.text(label='Color', w=60, al='left')
    cmds.text(label='Cone', w=60, al='left')
    cmds.text(label='Penumbra', w=60, al='left')
    cmds.text(label='Diffuse', w=60, al='left')
    cmds.text(label='Spec', w=60, al='left')
    cmds.text(label='Temperature Color', w=60, al='left')
    cmds.text(label='Select', w=60, al='left')
    cmds.text(label='Point At', w=60, al='left')
    cmds.setParent('..')
    create_lights()

def create_lights():
    """populates the UI with a row for each light in the scene"""
    global lights
    lights = cmds.ls(type='light')
    
    global swatches
    swatches = []
    
    global main_layout
    cmds.setParent(main_layout)
    
    global light_layout
    light_layout = cmds.rowColumnLayout(nc=12,
                                        columnWidth=[(1, 60), (2, 150), (3, 100), (4, 100), (5, 60), (6, 60), (7, 60), (8, 60), (9, 60), (10, 100), (11, 60), (12, 60)],
                                        cs=[(1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10)], rs=(1, 10))
    
    # create rows of individual lights
    for i, light in enumerate(lights):
        # 1 - enabled
        enabled = cmds.getAttr(light + '.visibility')
        cmds.checkBox(label='',
                      v=enabled,
                      onc=partial(turn_on, light, 'visibility'),
                      ofc=partial(turn_off, light, 'visibility'),
                      al='center', w=40)
        # 2 - name
        cmds.textField(light + 'name',
                       tx=cmds.listRelatives(light, type='transform', p=True)[0],
                       w=130,
                       cc=partial(rename, light),
                       ec=partial(rename, light))
        # 3 - type
        cmds.text(label=cmds.nodeType(light),
                  w=130,
                  al='left')
        # 4 - intensity
        cmds.floatField(light + 'intensity',
                        v=cmds.getAttr(light + '.intensity'),
                        cc=partial(update_float, light, 'intensity'),
                        ec=partial(update_float, light, 'intensity'),
                        w=60)
        # 5 - color
        swatch = cmds.canvas(rgbValue=cmds.getAttr(light + '.color')[0],
                             w=40,
                             h=20,
                             pressCommand=partial(color_picker, light, i))
        swatches.append(swatch)
        # 6 - cone angle
        if(cmds.nodeType(light) == 'spotLight'):
            cmds.floatField(light + 'coneAngle',
                            v=cmds.getAttr(light + '.coneAngle'),
                            cc=partial(update_float, light, 'coneAngle'),
                            ec=partial(update_float, light, 'coneAngle'),
                            w=60)
        else:
            cmds.floatField(v=0, w=60, en=0)
        
        # 7 - penumbra angle
        if(cmds.nodeType(light) == 'spotLight'):
            cmds.floatField(light + 'penumbraAngle',
                            v=cmds.getAttr(light + '.penumbraAngle'),
                            cc=partial(update_float, light, 'penumbraAngle'),
                            ec=partial(update_float, light, 'penumbraAngle'),
                            w=60)
        else:
            cmds.floatField(v=0, w=60, en=0)
        # 8 - diffuse
        if(cmds.nodeType(light) != 'ambientLight'):
            cmds.checkBox(label='',
                          v=cmds.getAttr(light + '.emitDiffuse'),
                          onc=partial(turn_on, light, 'emitDiffuse'),
                          ofc=partial(turn_off, light, 'emitDiffuse'),
                          al='center',
                          w=40)
        else:
            cmds.checkBox(label='', en=0)
        
        # 9 - spec
        if(cmds.nodeType(light) != 'ambientLight'):
            cmds.checkBox(label='',
                          v=cmds.getAttr(light + '.emitSpecular'),
                          onc=partial(turn_on, light, 'emitSpecular'),
                          ofc=partial(turn_off, light, 'emitSpecular'),
                          al='center',
                          w=40)
        else:
            cmds.checkBox(label='', en=0)

        # 10 - Temperature Color
        if cmds.nodeType(luz) == 'directionalLight' or cmds.nodeType(luz) == 'areaLight' or cmds.nodeType(luz) == 'spotLight':
            cmds.floatField(light + 'Temperature',v=cmds.getAttr(light + '.aiColorTemperature'),
                            cc=partial(update_float, light, 'aiColorTemperature'),
                            ec=partial(update_float, light, 'aiColorTemperature'),
                            w=60)

        # 11 - select
        cmds.button(label='Select', command=partial(select, light), al='center', w=40)
        # 12 - point at
        if(cmds.nodeType(light) != 'ambientLight' and cmds.nodeType(light) != 'pointLight'):
            cmds.button(label='Point', command=partial(aim, light), al='center', w=40)
        else:
            cmds.button(label='Point', en=0, w=40)
        
    cmds.setParent('..')
        
def refresh(*args):
    """deletes the light layout and regenerates"""
    global lights
    global light_layout
    cmds.deleteUI(light_layout)
    light_layout = ''
    lights = cmds.ls(type='light')
    create_lights()

def update_float(light, kind, *args):
    """generic function that updates float values"""
    sel_light = cmds.listRelatives(cmds.textField(light + 'name', q=True, tx=True), s=True)[0]
    cmds.setAttr(sel_light + '.' + kind, args[0])
    
def turn_off(light, kind, *args):
    """turns off a light"""
    sel_light = cmds.listRelatives(cmds.textField(light + 'name', q=True, tx=True), s=True)[0]
    cmds.setAttr(sel_light + '.' + kind, False)
    
def turn_on(light, kind, *args):
    """turns on a light"""
    sel_light = cmds.listRelatives(cmds.textField(light + 'name', q=True, tx=True), s=True)[0]
    cmds.setAttr(sel_light + '.' + kind, True)
    
def select(light, *args):
    """selects a light in the viewport"""
    sel_light = cmds.textField(light + 'name', q=True, tx=True)
    cmds.select(sel_light)
    
def aim(light, *args):
    """creates a constraint to aim the light, then removes the constraint"""
    sel_light = cmds.textField(light + 'name', q=True, tx=True)
    sel_obj = cmds.ls(sl=True)
    if (sel_obj and sel_light not in sel_obj):
        aim = cmds.aimConstraint(sel_obj, sel_light, aim=[0, 0, -1])
        cmds.delete(aim)
    
def rename(light, *args):
    """renames a light"""
    cmds.select(cmds.listRelatives(light, type='transform', p=True))
    new_name = cmds.rename(cmds.textField(light + 'name', q=True, tx=True))
    cmds.textField(light + 'name', e=True, tx=new_name)
    
def organize(*args):
    """parents all lights under a top-level 'lights' node"""
    if(not cmds.ls('LIGHTS__GRP')):
        cmds.group(name='LIGHTS__GRP', em=True, w=True)
    cmds.parent(cmds.ls(type='light'), 'LIGHTS__GRP', absolute=True)
    
def basic(*args):
    """creates a basic 6 light light rig for interiors, probably unnecessary now..."""
    if(not cmds.ls('LIGHTS__GRP')):
            cmds.group(name='LIGHTS__GRP', em=True, w=True)
    cool = [.8, .85, 1]
    warm = [1, .88, .8]
    north = cmds.directionalLight(n=('lFill_fromSouthOnNorth__LGDIR'), rgb=cool, i=.2)
    cmds.setAttr(cmds.listRelatives(north,type='transform',p=True)[0] + '.ry', 180)
    south = cmds.directionalLight(n='lFill_fromNorthOnSouth__LGDIR', rgb=cool, i=.2)
    east = cmds.directionalLight(n='lFill_fromWestOnEast__LGDIR', rgb=cool, i=.2)
    cmds.setAttr(cmds.listRelatives(east,type='transform',p=True)[0] + '.ry', 90)
    west = cmds.directionalLight(n='lFill_fromEastOnWest__LGDIR', rgb=cool, i=.2)
    cmds.setAttr(cmds.listRelatives(west,type='transform',p=True)[0] + '.ry', -90)
    sky = cmds.directionalLight(n='lFill_fromFloorOnSky__LGDIR', rgb=warm, i=.1)
    cmds.setAttr(cmds.listRelatives(sky,type='transform',p=True)[0] + '.rx', 90)
    floor = cmds.directionalLight(n='lFill_fromSkyOnFloor__LGDIR', rgb=cool, i=.2)
    cmds.setAttr(cmds.listRelatives(floor,type='transform',p=True)[0] + '.rx', -90)
    amb = cmds.ambientLight(n='lAmb_onSet__LGAMB', i=.01)
    cmds.parent(cmds.ls(type='light'), 'LIGHTS__GRP', absolute=True)
    refresh()
    
def change_decay(light, *args):
    """changes the decay type of light"""
    sel_light = cmds.listRelatives(cmds.textField(light + 'name', q=True, tx=True), s=True)[0]
    global opt
    if (args[0] == 'No Decay'):
        opt = 0
    elif (args[0] == 'Linear'):
        opt = 1
    elif (args[0] == 'Quadratic'):kind
        opt = 2
    elif (args[0] == 'Cubic'):
        opt = 3
    else:
        opt = int(args[0])
    cmds.optionMenu('decay' + light, edit=True, sl = opt + 1)
    cmds.setAttr(sel_light + '.decayRate', opt)
    
def color_picker(light, index, *args):
    """brings up the color picker UI to select a color for a light"""
    sel_light = cmds.listRelatives(cmds.textField(light + 'name', q=True, tx=True), s=True)[0]
    curr_color = cmds.getAttr(sel_light + '.color')
    cmds.colorEditor(rgbValue=curr_color[0])
    if cmds.colorEditor(query=True, result=True):
        values = cmds.colorEditor(query=True, rgb=True)
        cmds.setAttr(sel_light + '.color', *values)
        cmds.canvas(swatches[index], e=True, rgbValue=cmds.getAttr(sel_light + '.color')[0])
        
def add_light(kind, *args):
    global contSpot
    global contDir
    global contPoint
    global contArea
    global contAmb
    """adds a new light, organizes it, and refreshes the UI"""
    if(not cmds.ls('LIGHTS__GRP')):
        cmds.group(name='LIGHTS__GRP', em=True, w=True)
    if kind == 'spot':
        nameLight = cmds.spotLight(name='RENAMEMEPLEASE' + str(contSpot)).encode("utf-8")
        cmds.select(nameLight)
        lightTrf = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        newName = cmds.rename(lightTrf, str(lightTrf) + '__LGSPO')
        contSpot=contSpot+1
        cmds.parent(newName, 'LIGHTS__GRP')
        refresh()
    elif kind == 'dir':
        nameLight = cmds.directionalLight(name='RENAMEMEPLEASE' + str(contDir)).encode("utf-8")
        cmds.select(nameLight)
        lightTrf = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        newName = cmds.rename(lightTrf, str(lightTrf) + '__LGDIR')
        contDir=contDir+1
        cmds.parent(newName, 'LIGHTS__GRP')
        refresh()
    elif kind == 'point':
        nameLight = cmds.pointLight(name='RENAMEMEPLEASE' + str(contPoint)).encode("utf-8")
        cmds.select(nameLight)
        lightTrf = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        newName = cmds.rename(lightTrf, str(lightTrf) + '__LGPOI')
        contPoint=contPoint+1
        cmds.parent(newName, 'LIGHTS__GRP')
        refresh()
    elif kind == 'amb':
        nameLight = cmds.ambientLight(name='RENAMEMEPLEASE' + str(contAmb)).encode("utf-8")
        cmds.select(nameLight)
        lightTrf = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        newName = cmds.rename(lightTrf, str(lightTrf) + '__LGAMB')
        contAmb=contAmb+1
        cmds.parent(newName, 'LIGHTS__GRP')
        refresh()
    elif kind == 'area':
        nameLight = cmds.shadingNode('areaLight',name='RENAMEMEPLEASE' + str(contArea), asLight=True).encode("utf-8")
        cmds.select(nameLight)
        nameLight = cmds.rename(nameLight, 'RENAMEMEPLEASE' + str(contArea) + '__LGARE' )
        lightTrf = cmds.listRelatives(nameLight)[0]
        newName = cmds.rename(lightTrf, str(lightTrf) + '__LGARESH')
        contArea=contArea+1
        cmds.parent(nameLight, 'LIGHTS__GRP')
        refresh()
def main():
    if cmds.pluginInfo('mtoa.mll',q=True, l=True ):
        print 'Arnold it is ON'
    else:
        cmds.loadPlugin( 'mtoa.mll' )
        print 'Arnold ON'
    """calls the UI function to generate the UI"""
    UI()
main()