# ##################################################################################
#                               Animation Control Selector
#                                 Luca Fiorentini 2012
#                               luca.fiorentini@gmail.com
#                                         v1.3.4
# ##################################################################################
#
# To create the shelf and the buttons run
#
# import animSelector
# animSelector.install()
#
# If you wish to manually call the UIs:
# MAIN ASSIGN WINDOW
# animSelector.SetupUI()
#
# PICKER WINDOW
# animSelector.PickerUI()
#
# TO DO:
# *check if while pressing the add buttons the user has two different chars selected
# 
# ##################################################################################

# ##################################################################################
#                                    ChangeLog
# ##################################################################################
# > animSelector 1.3.5
#
# *Fixed button order and color when saved in the original file (the one that gets referenced)
#   Now it gets loaded correctly and remember the layout.
#   Please note that if you have more than one "charName" in the original scene only the first one will work
#
# ##################################################################################
# > animSelector 1.3.4
#
# *Picker window is now dockable
#    Please note that this is available only from Maya 2011.
#    If you don't like it, you can switch to the old window from the preferences
#
# *Changed namespaces finding algorithm
#
# *Added scrollbar to picker
#
# *Removing sets from the picker now checks for namespace
#
# *Added 'Rename Button' to picker window
#
# *Fixed a bug on 'get name from picker'
#
# *Cancel button on namespace chooser window now properly cancel the import
#
# *Fixed a bug on Maya2011
#    The 'fcc' flag for dockControl is not available on Maya2011. The picker will not mantain his position betwee sessions
#    in this version.
#
# *Removed 'keyable=True' flag on custom attributes
#
# ##################################################################################
# > animSelector 1.3.3
#
# *Changed custom attribute names
#    Seems that some people had issues with the "Morpheus Rig" because we we using the same naming convention (Argh!)
#    I changed the names to something more specific.
#    Please keep in mind that old setups will not work anymore.
#    However, you can update them to the new version from the update menu un the setup window.
#
# *Improved namespace handling when importing
#    You can now export a setup from a non referenced file and import in a referenced one  
#
# *Button colors and position is exported with the setup now
#
# ##################################################################################
# > animSelector 1.3.2
#
# *New button on the setup window
#    There is a small button near the "char name" field on the setup window.
#    It fills the "char name" field with the current active tab on the picker
#    (if the window is open).
#    This was a request to keep consistency with weird and long names
#    (like superMarioPartyVersionNoPants)
#
# *Preferences window
#    You can now modify the colors and the names for the "Change buttons color" menu.
#    The idea is that you can use the color name as the menu entry, or a body part
#    (like 'head' for red, 'left' for green ecc ecc)
#    Added picker buttons size
#
# *Extra > Backup hotkey on picker
#    Now you can backup your current hotkeys before assigning new ones.
# ##################################################################################
# >animSelector 1.3.1
#
# *New names for the functions
#    I have renamed the functions to make them more intuitive:
#    
#    SETUP WINDOW    
#    animSelector.SetupUI
#   
#    PIKER WINDOW
#    animSelector.PickerUI    
#    
# *Preferences window
#    There is a preference window accesible from the "Edit" menu on the setup window.
#    Now you can chose the "hotkey selection toggle' (replace, toggle or add) from there.
#    
# *UI get saved with the scene
#    Buttons' color and position now get saved with the scene
# ##################################################################################
# > animSelector 1.3
#
# *Import/Export
#    Added an import/export function in case you can't modify the reference file.
#    The setup of the character can be exported to an external file (from the picker
#    window) and then re-imported in another shot.
#    There are two types of import (the can be chosen from the 'File' menu on the 
#    setup window).
#    The normal import let you import the data back and re assing it to the same character.
#    In case the namespaces are different between the shots, a window will popup 
#    letting you chose the correct one.
#    There is also another import: 'Import and remap to new character'. This option 
#    lets you assign the setup to another character in the scene.
#    The controls have to be the same, so it should be
#    A) A second reference of the same file (like when you do duplicate reference 
#       from the reference editor
#    B) A similar setup from the original file (like of crowds or extras)
#    
# *Draggable Piker's Button
#    Buttons on the picker are draggable, letting you reorganize the window as you 
#    prefer (like most used buttons on top).
#    The behavior of the drag and drop is like this:
#    if you have buttons A, B, C and D and you drop button D on the lower half of 
#    button B, D will go below button B.
#    if you drop it on the upper half, it will go over button B
#    FOR NOW BUTTON'S POSITION WILL RESET WHEN YOU CLOSE THE WINDOW
#    
# *Colorable Buttons
#    Now you can change the color of the buttons on the picker. Just right click and
#    chose 'Change button color'
#    FOR NOW BUTTON'S COLOR WILL RESET WHEN YOU CLOSE THE WINDOW
#    
# *Maya like selection behavior
# I changed the way you select the controls when you click the button.
#
#    - Normal click will replace the selection (select -r)
#    - Shift + click will toggle the selection (select -tgl)
#    - Ctrl + click will remove the object from the selection (select -d)
#    - Shift + Ctrl + click will add the object to the selection (select -add)
#
# *Help
#    There is a 'Help' entry in the menu. Text is still missing
# ##################################################################################
# > animSelector 1.1.0
#
# *Hotkey selection behavior
#    Added the ability to change the hotkey behavior when calling the picker:
#       - animSelector.checkCtrlNamesUI() is TOGGLE,
#       - animSelector.checkCtrlNamesUI(1) is REMOVE
#       - animSelector.checkCtrlNamesUI(2) is ADD
# ##################################################################################
# > animSelector 1.0.0
#  
# *First release
# ##################################################################################

import ast
import gc
import maya.cmds as mc
import maya.mel
import os
import re
import sys

from maya.OpenMaya import MGlobal

try: import simplejson as json
except ImportError: import json

class SetupUI():
    # Main Window and preferences
    def __init__(self, *args):
        spacer = 16

        self.name = "setupUI"
        self.title = "animSelector :: Setup"

        # Begin creating the UI
        if (mc.window(self.name, q=1, exists=1)): mc.deleteUI(self.name)
        self.window = mc.window(self.name, title=self.title, menuBar=True, mnb=False, mxb=False, s=False, rtf=1, bgc=[.125,.125,.125])
        mc.menu(label='File', tearOff=False)
        mc.menuItem(label='Import', c=Callback(self.importData, importSwitch=1), ann='Import setup to the same namespace/character.')
        mc.menuItem(label='Import and remap to new character', c=Callback(self.importData, importSwitch=0), ann='Import setup to the same character but with a different namespace. This is usefull, for example, for a duplicated reference.')
        mc.menuItem(d=True)
        mc.menuItem(label='Help', c=HelpUI, ann='Open help window')
        
        mc.menu(label='Edit', tearOff=False)
        mc.menuItem(label='Preferences', c=PrefsUI, ann='Color and Selection preferences.')
        
        mc.menu(label='Update', tearOff=False)
        mc.menuItem(label='Update Setups', c=updateSetup, ann='Update old setups to work with the latest version of the tool')

        self.form = mc.formLayout(bgc=[.25,.25,.25])
        self.emptyBlackLine = mc.text('', bgc=[.125,.125,.125], h=1 )
        self.charText = mc.textFieldButtonGrp(label='Char Name', cal=(1, 'left'), cw3=(65,176,16), bl='<', bc=self.fillCharName, ann='Input character name. Button on the right is to get the "Character Name" from the Picker\'s active tab')
        self.ctrlText = mc.textFieldGrp(label='Ctrl Name', cal=(1, 'left'), cw2=(65,196), ann='Input control name. Spaces will be removed')
        self.setButton = mc.button(label='Replace', width=100, command=self.replaceAttributes, bgc=[.375,.375,.375])
        self.addButton = mc.button(label='Add', width=100, command=self.addAttributes, bgc=[.375,.375,.375])
        self.removeButton = mc.button(label='Remove', width=100, command=self.removeAttributes, bgc=[.375,.375,.375])
        self.selectNoAttrButton = mc.button(label='Select objs without attribute', width=150, command=self.selectMissingAttributes, bgc=[.375,.375,.375])
        self.pickerButton = mc.button(label='Picker', width=150, command=PickerUI, bgc=[.375,.375,.375])

        # Attach elements to form
        mc.formLayout(  self.form,
                        edit=True,
                        attachForm=[
                            (self.emptyBlackLine, 'top', 0),
                            (self.emptyBlackLine, 'left', 0),
                            (self.emptyBlackLine, 'right', 0),
                            (self.charText, 'left', spacer),
                            (self.charText, 'right', spacer),
                            (self.ctrlText, 'left', spacer),
                            (self.ctrlText, 'right', spacer),],
                        attachControl=[
                            (self.charText, 'top', spacer, self.emptyBlackLine),
                            (self.ctrlText, 'top', spacer, self.charText),
                            (self.setButton, 'top', spacer, self.ctrlText),
                            (self.addButton, 'top', spacer, self.ctrlText),
                            (self.addButton, 'left', 0, self.setButton),
                            (self.removeButton, 'top', spacer, self.ctrlText),
                            (self.removeButton, 'left', 0, self.addButton),
                            (self.selectNoAttrButton, 'top', 0, self.removeButton),
                            (self.pickerButton, 'top', 0, self.removeButton),
                            (self.pickerButton, 'left', 0, self.selectNoAttrButton)]
                    )

        mc.showWindow(self.window)
        mc.window(self.window, e=1, w=303, h=162)
        
        #SET DEFAULT PREFERENCES
        # COLORS
        if not mc.optionVar(q='animSelector_firstColor_name'):    mc.optionVar(sv=['animSelector_firstColor_name',    'red'])
        if not mc.optionVar(q='animSelector_firstColor_color'):   mc.optionVar(sv=['animSelector_firstColor_color',   '[.68, .135, .135]'])
        if not mc.optionVar(q='animSelector_secondColor_name'):   mc.optionVar(sv=['animSelector_secondColor_name',   'green'])
        if not mc.optionVar(q='animSelector_secondColor_color'):  mc.optionVar(sv=['animSelector_secondColor_color',  '[.2, .6, .23]'])
        if not mc.optionVar(q='animSelector_thirdColor_name'):    mc.optionVar(sv=['animSelector_thirdColor_name',    'blue'])
        if not mc.optionVar(q='animSelector_thirdColor_color'):   mc.optionVar(sv=['animSelector_thirdColor_color',   '[.08, .36, .5]'])
        if not mc.optionVar(q='animSelector_fourthColor_name'):   mc.optionVar(sv=['animSelector_fourthColor_name',   'cyan'])
        if not mc.optionVar(q='animSelector_fourthColor_color'):  mc.optionVar(sv=['animSelector_fourthColor_color',  '[.24, .6, .6]'])
        if not mc.optionVar(q='animSelector_fifthColor_name'):    mc.optionVar(sv=['animSelector_fifthColor_name',    'magenta'])
        if not mc.optionVar(q='animSelector_fifthColor_color'):   mc.optionVar(sv=['animSelector_fifthColor_color',   '[.6, .24, .6]'])
        if not mc.optionVar(q='animSelector_sixthColor_name'):    mc.optionVar(sv=['animSelector_sixthColor_name',    'yellow'])
        if not mc.optionVar(q='animSelector_sixthColor_color'):   mc.optionVar(sv=['animSelector_sixthColor_color',   '[.775, .675, .225]'])
        if not mc.optionVar(q='animSelector_seventhColor_name'):  mc.optionVar(sv=['animSelector_seventhColor_name',  'white'])
        if not mc.optionVar(q='animSelector_seventhColor_color'): mc.optionVar(sv=['animSelector_seventhColor_color', '[.85, .85, .85]'])
        if not mc.optionVar(q='animSelector_eighthColor_name'):   mc.optionVar(sv=['animSelector_eighthColor_name',   'black'])
        if not mc.optionVar(q='animSelector_eighthColor_color'):  mc.optionVar(sv=['animSelector_eighthColor_color',  '[.1, .1, .1]'])

        # SELECTION
        if not mc.optionVar(q='animSelector_hotKeySelectionToggle'): mc.optionVar(iv=('animSelector_hotKeySelectionToggle', 0))
        
        # EXTRAS
        if not mc.optionVar(q='animSelector_pickerButtonsHeight'): mc.optionVar(iv=('animSelector_pickerButtonsHeight', 28))         #buttons
        if not mc.optionVar(q='animSelector_dockable'): mc.optionVar(iv=('animSelector_dockable', 1))                                           #dockable window
        if not mc.optionVar(q='animSelector_dockArea'): mc.optionVar(sv=('animSelector_dockArea', 'left'))                                     #dockable window position
        if not mc.optionVar(q='animSelector_dockFloating'): mc.optionVar(iv=('animSelector_dockFloating', 0))                                #dockable window floating
        
    # Procedure to create and set the attributes on the controls
    def setAttributes(self, charName, ctrlName, sel, setMode):
    
    ###############################################################
    #        Procedure to set the attributes on the controls.     #
    #       two modes are available through the setMode flag:     #
    #                    'replace' and 'add'                      #
    #          This procedure is also used by the import          #
    #          to restore the attributes on the controls          #
    ###############################################################
    
        if len(charName.split('_')) != 1 or len(ctrlName.split('_')) != 1:
            mc.warning('The use of "_" in Char and Ctrl names is allowed but discouraged.')
        
        if len(charName.split(' ')) != 1:
            charName = self.reformatString(charName, ' ')
            mc.textFieldGrp(self.charText, e=True, text=charName)
            mc.warning('No spaces allowed in names. String reformatted to %s and assigned to the object(s)' % charName)
            
        if len(ctrlName.split(' ')) != 1:
            ctrlName = self.reformatString(ctrlName, ' ')
            mc.textFieldGrp(self.ctrlText, e=True, text=ctrlName)
            mc.warning('No spaces allowed in names. String reformatted to %s and assigned to the object(s)' % ctrlName)
        
        attrList = ['animSelectorCharName','animSelectorCtrlName']

        #Check again for the attributes just in case the user changed the selection
        for obj in sel:
            ctrlNameList = []
            for attrs in attrList:
                
                if mc.objExists(obj + '.' + attrs):
                    pass
                
                else:
                    mc.addAttr(obj, longName=attrs, dataType="string")
                    mc.setAttr(obj + '.' + attrs, e=True, keyable=False)
                    
            if setMode == 'replace':
                mc.setAttr("%s.animSelectorCharName" % obj, charName, type="string")
                mc.setAttr("%s.animSelectorCtrlName" % obj, ctrlName, type="string")
            
            elif setMode == 'add':
                tempString = mc.getAttr('%s.animSelectorCtrlName' % obj)
                
                if not tempString:
                    newData = ctrlName
                
                else:
                    tempString = re.sub(r'\s', '', tempString)
                    tempString = tempString.split(',')
                    ctrlNameList.append(ctrlName)
                    ctrlNameList.extend(tempString)
                    ctrlNameList = list(set(ctrlNameList))
                    newData = ', '.join(ctrlNameList)
                
                mc.setAttr('%s.animSelectorCharName' % obj, charName, type='string')
                mc.setAttr('%s.animSelectorCtrlName' % obj, newData, type='string')

    # Procedure for REMOVE button
    def removeAttributes(self, *args):
    ###############################################################
    #     Procedure to remove attributes from selected objects    #
    #           Just in case you want to clean the scene          #
    ###############################################################

        #Check if something is selected
        if len(mc.ls(sl=True)) == 0:
            mc.warning('No object selected')
            return 0

        #Is selection is != than 0 remove the attributes
        else:
            attrList = ['animSelectorCharName', 'animSelectorCtrlName']
            for obj in mc.ls(sl=True):
                for attr in attrList:
                    try:
                        mc.deleteAttr(obj, at=attr)
                        MGlobal.displayInfo('[INFO] %s removed from %s' % (attr, obj))
                    except:
                        mc.warning('%s has not %s attribute, skipped' % (obj, attr))

    # Procedure for ADD button
    def addAttributes(self, *args):
        charName = mc.textFieldGrp(self.charText, q=True, text=True)
        ctrlName = mc.textFieldGrp(self.ctrlText, q=True, text=True)
        sel = mc.ls(sl=True)
        self.setAttributes(charName, ctrlName, sel, 'add')

    # Procedure for REPLACE button
    def replaceAttributes(self, *args):
        charName = mc.textFieldGrp(self.charText, q=True, text=True)
        ctrlName = mc.textFieldGrp(self.ctrlText, q=True, text=True)
        sel = mc.ls(sl=True)
        self.setAttributes(charName, ctrlName, sel, 'replace')

    # Procedure for SELECT OBJS WITHOUT ATTRIBUTE button
    def selectMissingAttributes(self, *args):

    ###############################################################
    #     Procedure to select objects that miss the attribute     #
    #               or that have it set to 'none'                 #
    ###############################################################
    
        objList = []
        attrList = ['animSelectorCharName','animSelectorCtrlName']
        
        #Setting up the progress bar. Some time checking takes a few seconds with a lot of stuff in the scene
        x = len(mc.ls(type='transform'))
        counter = 0
        window = mc.window(t="Checking scene...")
        mc.columnLayout()
        progressControl = mc.progressBar(maxValue=x, width=300)
        mc.showWindow( window )
        mc.window(window, e=1, w=302, h=26)
        
        # Check the shapes to use transforms only from nurbsCurves, locators and meshes
        # I'm quite sure there's a smarter way to do this xD
        for obj in mc.ls(type='transform'):
            objFlag = 0
            objShape = mc.pickWalk(obj, direction='down')
            objType = ['nurbsCurve','locator','mesh']
            progressInc = mc.progressBar(progressControl, edit=True, pr=counter+1)
            
            # Check the attributes
            if mc.nodeType(objShape[0]) in objType:
                for attrs in attrList:
                    if mc.objExists(obj + '.' + attrs):
                        if mc.getAttr(obj + '.' + attrs) != '': pass
                        else: objFlag = 1
                    else: objFlag = 1

            # Make a list with the object to select
            if objFlag: objList.append(obj)
            counter = counter + 1 

        mc.deleteUI(window)
        
        # Workarond for 'select -r' with an empty list
        if len(objList) != 0:
            mc.select(objList, r=True)
        else:
            mc.select(cl=True)
            MGlobal.displayInfo('[INFO] All objects are with the attribute')

    # Procedure to fill the "Char Name" text field with the active
    # tab name on the picker window
    def fillCharName(self, *args):

        #Get PickerUI instance
        for obj in gc.get_objects():
            if isinstance(obj, PickerUI):
                self.myPickerUi = obj
                
        try:
            myIndex = mc.tabLayout(self.myPickerUi.tabLayout, q=True, sti=True)
            myActiveTab = mc.tabLayout(self.myPickerUi.tabLayout, q=True, tl=True)[myIndex - 1]
            mc.textFieldButtonGrp(self.charText, e=True, text=myActiveTab)
        except:
            MGlobal.displayInfo('[INFO] You need the picker to be visible to get the name from it')
        
    # Procedure to convert a list to a single string. Items are separated
    # by capitalizing the first letter
    def reformatString(self, data, checker):
        wordList = data.split(checker)
        newData = ''
        for member in wordList:
            if newData == '':
                newData += member
            else:
                newData += member.capitalize()
                 
        return newData
        
    # Procedure for IMPORT button
    def importData(self, importSwitch, *args):

        myFile = mc.fileDialog( m=0, directoryMask='*.animSelectorData' )
        myTitles = ['Chose new character namespace', 'Unable to find namespace']

        if myFile:
            with open(myFile, 'r') as f:
                myDictionary = json.load(f)

            # if not mc.namespaceInfo(myDictionary.keys()[0], fullName=True) or not importSwitch:
            if not myDictionary.keys()[0] in mc.namespaceInfo(ls=True) or not importSwitch:
                newNs = mc.layoutDialog(title=myTitles[importSwitch], ui=namespaceChooser)
                if newNs == 'animSelectorNamespaceCancel':
                    MGlobal.displayInfo('[INFO] Import Cancelled')
                    return

                myDictionary = replaceNamespace(myDictionary.keys()[0], newNs, myDictionary)
            
            myNamespace = myDictionary.keys()[0]
            myCharacter = [item for item in myDictionary[myNamespace].keys() if not item == 'uiData'][0]
            myUiData = myDictionary[myNamespace]['uiData']
            for myControlName in myDictionary[myNamespace][myCharacter]:
                self.setAttributes(myCharacter, myControlName, myDictionary[myNamespace][myCharacter][myControlName], 'add')

            # for myNamespace in myDictionary:
                # for myCharacter in myDictionary[myNamespace]:
                    # for myControlName in myDictionary[myNamespace][myCharacter]:
                        # self.setAttributes(myCharacter, myControlName, myDictionary[myNamespace][myCharacter][myControlName], 'add')

            if myUiData:
                if not mc.objExists('animSelectorUiData'):
                    mc.createNode('blindDataTemplate', n='animSelectorUiData')

                if not mc.objExists('animSelectorUiData.data'):
                    mc.addAttr('animSelectorUiData', longName='data', dataType="string")
                    mc.setAttr('animSelectorUiData.data', e=True, keyable=False)
                    
                myUiString = mc.getAttr('animSelectorUiData.data')
                if myUiString:
                    myUiDictionary = ast.literal_eval(myUiString)
                else:
                    myUiDictionary = {}
                    
                # myUiDictionary.setdefault(myNamespace, myUiData)
                myUiDictionary[myNamespace] = myUiData
                
                mc.setAttr('animSelectorUiData.data', myUiDictionary, type='string')
                
                        
            MGlobal.displayInfo('[INFO] %s imported successfully' % myDictionary[myDictionary.keys()[0]].keys()[0])
                
        else:
            MGlobal.displayInfo('[INFO] Import cancelled')
            
class PickerUI():

    def __init__(self, selCom=0):

        noMattes = 0
        self.mayaVersion = maya.mel.eval('getApplicationVersionAsFloat')
        self.labelHeight = 35
        self.buttonHeight = mc.optionVar(q='animSelector_pickerButtonsHeight')
        self.dockable = mc.optionVar(q='animSelector_dockable')
        self.dockArea = mc.optionVar(q='animSelector_dockArea')
        self.dockFloating = mc.optionVar(q='animSelector_dockFloating')
        self.buttonList = {}

		#SET SELECTION TOGGLE FOR HOTKEYS
        selCom = mc.optionVar(q='animSelector_hotKeySelectionToggle')
        if selCom == 1:     selCom = 'tgl'
        elif selCom == 2:   selCom = 'add'
        else:               selCom = 'r'			

        # This procedure builds the layout for every tab
        def createLayout(obj, tabParent, animSelectorData, grp, charNamespace, selCom):
        
            labelCount = 0
            buttonCount = 0
            
            self.tabMainLayout = mc.columnLayout(adj=True, parent=tabParent)
                       
            mc.text(label=charNamespace, p=self.tabMainLayout, manage=False)
            mc.text(label=grp, h=self.labelHeight, bgc=[.125,.125,.125], p=self.tabMainLayout)
            labelCount+=1
            
            self.draggableLayout = mc.columnLayout(adj=True, parent=self.tabMainLayout)
            for member in sorted(animSelectorData[grp]):
                self.dragPlaceHolder = mc.columnLayout(adj=True, parent=self.draggableLayout, dropCallback=self.dropButton)
                selButton = mc.button(label=member, command=Callback(self.selectButton, animSelectorData[grp][member]), h=(self.buttonHeight), bgc=[.4, .4, .4], dragCallback=self.dragButton, p=self.dragPlaceHolder)
                self.buttonList.setdefault(charNamespace, {}).setdefault(member, [selButton, self.dragPlaceHolder])
                
                #SET UP THE POPUP
                mc.popupMenu()
                mc.menuItem(l='Remove set from scene', c=Callback(self.stripObject, obj, member, 1, selButton, charNamespace))
                mc.menuItem(l='Remove set from selection', c=Callback(self.stripObject, obj, member, 0, selButton, charNamespace ))
                
                mc.menuItem(d=True)
                
                mc.menuItem(l='Rename button', c=Callback(self.renameControls, obj, member, selButton, charNamespace))
                mc.menuItem(l='Change button color', sm=True)
                colorVariables =[
                            ['First',      mc.optionVar(q='animSelector_firstColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_firstColor_color'))],
                            ['Second',     mc.optionVar(q='animSelector_secondColor_name'),     ast.literal_eval(mc.optionVar(q='animSelector_secondColor_color'))],
                            ['Third',      mc.optionVar(q='animSelector_thirdColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_thirdColor_color'))],
                            ['Fourth',     mc.optionVar(q='animSelector_fourthColor_name'),     ast.literal_eval(mc.optionVar(q='animSelector_fourthColor_color'))],
                            ['Fifth',      mc.optionVar(q='animSelector_fifthColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_fifthColor_color'))],
                            ['Sixth',      mc.optionVar(q='animSelector_sixthColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_sixthColor_color'))],
                            ['Seventh',    mc.optionVar(q='animSelector_seventhColor_name'),    ast.literal_eval(mc.optionVar(q='animSelector_seventhColor_color'))],
                            ['Eighth',     mc.optionVar(q='animSelector_eighthColor_name'),     ast.literal_eval(mc.optionVar(q='animSelector_eighthColor_color'))],
                            ['Extra',      'Reset',                                             [.4, .4, .4]]
                        ]
                
                for color in colorVariables:
                    mc.menuItem(l=color[1], c=Callback(self.changeButtonColor, selButton, color[2]))
                mc.setParent('..', menu=True)
                
                mc.menuItem(d=True)

                mc.menuItem(l='Assign ALT hotkey', sm=True)
                for n in range(0,10):
                    mc.menuItem(l='Alt+%i' % n, c=Callback(self.assignHotkey, n, animSelectorData[grp][member], member, grp, 'alt', selCom))
                mc.setParent('..', menu=True)

                mc.menuItem(l='Assign CTRL hotkey', sm=True)
                for n in range(0,10):
                    mc.menuItem(l='Ctrl+%i' % n, c=Callback(self.assignHotkey, n, animSelectorData[grp][member], member, grp, 'ctrl', selCom))
                
                buttonCount+=1
                    
            winH = (labelCount * self.labelHeight)+(buttonCount * self.buttonHeight)
            
            mc.tabLayout( self.tabLayout, edit=True, tabLabel=(self.tabMainLayout, grp))

            self.extraButtons = mc.rowLayout(nc=3, adj=1, p=self.tabMainLayout)
            mc.button(label='HotKeysToShelf', command=Callback(self.getHotkeys, charName), h=self.buttonHeight, bgc=[.5,.225,.5 ], p=self.extraButtons)
            mc.button(label='Export', command=Callback(self.exportData, charName, charNamespace), h=self.buttonHeight, w=65, bgc=[.125,.125,.125 ], p=self.extraButtons)
            # End of "every tab" layout
            
        # Build the dictionary with all the data
        self.animSelectorData = getDataBack()
        
        self.name = "pickerUI"
        self.title = "animSelector :: Picker"
        self.dockName = "pickerDock"

        # Begin creating the UI
        if (mc.window(self.name, q=1, exists=1)):
            mc.deleteUI(self.name)
        self.window = mc.window(self.name, title=self.title, menuBar=True, width=200)

        if not self.mayaVersion < 2011:
                if mc.dockControl(self.dockName, q=True, exists=1):
                    mc.deleteUI(self.dockName)
        
        # self.mainWindowLayout = mc.columnLayout(adj=1)
        self.mainWindowLayout = mc.formLayout()
        
        if len(self.animSelectorData) == 0:
            self.emptyLayout = mc.rowLayout(adj=1)
            mc.text(label='No selection attributes in the scene.\nPlease add them in the reference files\nor in the actual working scene', w=(300), h=(100), bgc=(.125,.125,.125), p=self.emptyLayout)
            noMattes = 1
        else:
            self.tabLayout = mc.tabLayout(p=self.mainWindowLayout, scr=True, cr=True)
            mc.formLayout(self.mainWindowLayout, e=True, attachForm=((self.tabLayout, 'top', 0), (self.tabLayout, 'bottom', 0),(self.tabLayout, 'left', 0),(self.tabLayout, 'right', 0)))
            for charNamespace in sorted(self.animSelectorData):
                for charName in self.animSelectorData[charNamespace]:
                    createLayout(charName, self.tabLayout, self.animSelectorData[charNamespace], charName, charNamespace, selCom)
                    
            mc.menu(label='Extras', tearOff=False)
            mc.menuItem(label='Backup Hotkeys', c=self.backupHotkeys, ann='Backup current alt/ctrl 0-9 hotkeys to shelf')
            mc.menuItem(d=True)
            mc.menuItem(label='Help', c=HelpUI, ann='Open help window')
        

        if noMattes:
            mc.showWindow(self.window)
            mc.window(self.window, e=1, w=(301), h=(100))
        # print self.mayaVersion
        else:
            if self.mayaVersion < 2011 or not self.dockable:
                mc.showWindow(self.window)
                mc.window(self.window, e=1, w=250)
            
            elif self.mayaVersion < 2012:
                mc.dockControl(self.dockName, label=self.title, area=self.dockArea, floating=self.dockFloating, content=self.window, allowedArea=['left', 'right'])
                mc.dockControl(self.dockName, e=1, w=250)
            
            else:
                mc.dockControl(self.dockName, label=self.title, area=self.dockArea, floating=self.dockFloating, content=self.window, allowedArea=['left', 'right'], fcc=Callback(self.saveDockState, self.dockName))
                mc.dockControl(self.dockName, e=1, w=250)
        
            self.restoreCustomUi()
        
   
    def saveDockState(self, dockName):
        self.dockArea = mc.dockControl(dockName, q=1, area=True)
        self.dockFloating = mc.dockControl(dockName, q=1, floating=True)
            
        mc.optionVar(sv=('animSelector_dockArea', self.dockArea))
        mc.optionVar(iv=('animSelector_dockFloating', self.dockFloating))
   
    # Procedure to define the hotkeys
    def assignHotkey(self, keyNum, sel, ctrlName, charName, modifier, selCom):
        if modifier == 'alt':    
            mc.nameCommand('%s_%s_nc' % (charName, ctrlName), ann='hotkey for %s_%s' % (charName, ctrlName), command='select -%s %s' % (selCom, ' '.join(sel)))
            mc.hotkey(k=keyNum, altModifier=True, n='%s_%s_nc' % (charName, ctrlName))
        elif modifier == 'ctrl':
            mc.nameCommand('%s_%s_nc' % (charName, ctrlName), ann='hotkey for %s_%s' % (charName, ctrlName), command='select -%s %s' % (selCom, ' '.join(sel)))
            mc.hotkey(k=keyNum, ctrlModifier=True, n='%s_%s_nc' % (charName, ctrlName))

    # Procedure to backup the hotkeys
    def backupHotkeys(self, *args):
        myString = 'import maya.cmds as mc\n'

        try:
            topShelf = maya.mel.eval('$nul = $gShelfTopLevel')
        except:
            MGlobal.displayInfo('[WARNING] Unable to find main shelf. Check if you have them visible')
            return 0
        
        for a in range(10):
            if mc.hotkey(a, q=True, alt=True):
                myString += 'mc.hotkey(k=%s, altModifier=True, n=\'%s\')\n' % (a, mc.hotkey(a, q=True, name=True, alt=True))
            if mc.hotkey(a, q=True, ctl=True):
                myString += 'mc.hotkey(k=%s, ctrlModifier=True, n=\'%s\')\n' % (a, mc.hotkey(a, q=True, name=True, ctl=True))
        
        newShelfName = 'animSelector'
        allShelves = mc.shelfTabLayout(topShelf, query=True, tabLabelIndex=True)

        if newShelfName not in allShelves:
            animSelectorShelf = maya.mel.eval('addNewShelfTab %s' % newShelfName)
        else:
            animSelectorShelf = mc.shelfTabLayout(topShelf, e=True, st=newShelfName)        

        mc.shelfButton(parent=newShelfName, i='animSelector_empty.png', c=myString, label='backup', imageOverlayLabel='backup')
    
    # Procedure for SAVE HOTKEYS TO SHELF button 
    def getHotkeys(self, tab):

        altDiz = {}
        ctrlDiz = {}

        for k in range(0,9):
            altNc = mc.hotkey( k, altModifier=True, name=True, query=True )
            ctrlNc = mc.hotkey( k, ctrlModifier=True, name=True, query=True )
            
            #BUILD ALT DICTIONARY
            if altNc:
                for n in range(1, mc.assignCommand(query=True, numElements=True) + 1):
                    if mc.assignCommand(n, query=True, name=True) == altNc and mc.assignCommand(n, query=True, name=True).split('_')[0] == tab:
                        altDiz[k] = [mc.assignCommand(n, query=True, name=True),  mc.assignCommand(n, q=True, command=True), n]
                        
            #BUILD CTRL DICTIONARY
            if ctrlNc:
                for n in range(1, mc.assignCommand(query=True, numElements=True) + 1):
                    if mc.assignCommand(n, query=True, name=True) == ctrlNc and mc.assignCommand(n, query=True, name=True).split('_')[0] == tab:
                        ctrlDiz[k] = [mc.assignCommand(n, query=True, name=True), mc.assignCommand(n, q=True, command=True), n]
        
        #BUILD THE COMMAND STRING
        shelfCommand = 'import maya.cmds as mc\n'
        for k in altDiz:
            shelfCommand += "mc.hotkey(k=%i, altModifier=True, n='%s')\n" % (k, altDiz[k][0])
        for k in ctrlDiz:
            shelfCommand += "mc.hotkey(k=%i, ctrlModifier=True, n='%s')\n" % (k, ctrlDiz[k][0])
            
        #SAVE THE BUTTON TO SHELF
        if len(altDiz) or len(ctrlDiz):
            try:
                topShelf = maya.mel.eval('$nul = $gShelfTopLevel')
            except:
                MGlobal.displayInfo('[WARNING] Unable to find main shelf. Check if you have them visible')
                return 0

            newShelfName = 'animSelector'
            allShelves = mc.shelfTabLayout(topShelf, query=True, tabLabelIndex=True)

            if newShelfName not in allShelves:
                animSelectorShelf = maya.mel.eval('addNewShelfTab %s' % newShelfName)
            else:
                MGlobal.displayInfo('[INFO] animSelector shelf already exists')
                animSelectorShelf = mc.shelfTabLayout(topShelf, e=True, st=newShelfName)

            # currentShelf = mc.tabLayout(topShelf, q=1, st=1)
            mc.shelfButton(parent=newShelfName, i='animSelector_empty.png', c=shelfCommand, label=tab, imageOverlayLabel=tab)
                        
            print 'Those are the hotkeys that have been assigned:\n--------------------------------------------------------------------'
            for a in altDiz:
                print ('Alt+%i to %s\ncurrent command is: "%s"\n' % (a, altDiz[a][0], altDiz[a][1]))
                
            for c in ctrlDiz:
                print ('Ctrl+%i to %s\ncurrent command is: "%s"\n' % (c, ctrlDiz[c][0], ctrlDiz[c][1]))

            MGlobal.displayInfo('[INFO] Hotkeys for %s saved to the shelf, open script editor for details' % (tab))

            return 1
        else:
            MGlobal.displayInfo('[WARNING] No hotkeys currently assigned to %s, nothing to save to the shelf' % (tab))
            return 0
    
    # Procedure to remove attributes from the scene
    # If chooser == to 0 > remove from all objects in the scene
    # If chooser == to 1 > remove from selection
    def stripObject(self, stripChar, stripCtrl, chooser, selButton, charNamespace):
    
        # 1 for all / 0 for selection
        if chooser:
            objectList = mc.ls(type='transform')
        else:
            objectList = mc.ls(sl=True)
        
        for obj in objectList:
            # check for both attributes to exist
            if obj.split(':')[0] == charNamespace or len(obj.split(':')) == 1:
                if mc.objExists('%s.animSelectorCharName' % obj) & mc.objExists('%s.animSelectorCtrlName' % obj):
                    charName = mc.getAttr(obj + ('.animSelectorCharName'))
                    ctrlName = mc.getAttr(obj + ('.animSelectorCtrlName'))
                    
                    cleanList = []
                    
                    attributeList = ctrlName.split(',')
                    
                    for attribute in attributeList:
                        cleanList.append(re.sub(r'\s', '', attribute))
                    if stripChar == charName:
                        if stripCtrl in cleanList:
                            cleanList.remove(stripCtrl)
                        newData = ', '.join(cleanList)
                        mc.setAttr(obj + ".animSelectorCtrlName", newData, type="string")
                        if not mc.getAttr('%s.animSelectorCtrlName' % obj):
                            try:
                                mc.deleteAttr(obj, at='animSelectorCharName')
                                MGlobal.displayInfo('[INFO] %s removed from %s' % ('animSelectorCharName', obj))
                            except:
                                mc.warning('%s has not %s attribute, skipped' % (obj, 'animSelectorCharName'))
                            try:
                                mc.deleteAttr(obj, at='animSelectorCtrlName')
                                MGlobal.displayInfo('[INFO] %s removed from %s' % ('animSelectorCtrlName', obj))
                            except:
                                mc.warning('%s has not %s attribute, skipped' % (obj, 'animSelectorCtrlName'))
        
        # hide the button when all attributes are removed
        if chooser:
            mc.button(selButton, e=True, vis=0)            
        else:
            MGlobal.displayInfo('Reload the UI to update')

    # Procedure to rename a control name both on the picker and on the controls
    def renameControls(self, uiCharName, uiCtrlName, buttonPath, charNamespace):
        
        result = mc.promptDialog( title='Rename Set', message='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
        if result == 'OK':
            myNewControlName = mc.promptDialog(query=True, text=True)
            if myNewControlName.split(' ') > 1:
                noSpaces = myNewControlName.split(' ')

                cleanString = ''
                
                for item in noSpaces:
                    if not cleanString:
                        cleanString += item
                    else:
                        cleanString += item.capitalize()

                myNewControlName = cleanString
        else:
            return
        
        objectList = mc.ls(type='transform')
        for obj in objectList:
            if obj.split(':')[0] == charNamespace or len(obj.split(':')) == 1:
                if mc.objExists('%s.animSelectorCharName' % obj) & mc.objExists('%s.animSelectorCtrlName' % obj):
                    charName = mc.getAttr(obj + ('.animSelectorCharName'))
                    ctrlName = mc.getAttr(obj + ('.animSelectorCtrlName'))
                    
                    cleanList = []
                    
                    attributeList = ctrlName.split(',')
                    
                    for attribute in attributeList:
                        cleanList.append(re.sub(r'\s', '', attribute))
                        
                    myNewList = [myNewControlName if x==uiCtrlName else x for x in cleanList]
                    myNewString = ', '.join(myNewList)
                    mc.setAttr(obj + ".animSelectorCtrlName", myNewString, type="string")
                    
                    mc.button(buttonPath, e=True, l=myNewControlName)
                    self.saveUiData(self.tabLayout)
            
    # Procedure to export setup data to an external file
    def exportData(self, grp, ns):
        destFile = mc.fileDialog( m=1, directoryMask='*.animSelectorData' )
        
        if destFile:
            myDictionary = dict( [(k,j) for k,j in getDataBack().items() if k == ns])

            if mc.objExists('animSelectorUiData.data'):
                myString = mc.getAttr('animSelectorUiData.data')
                myUiDictionary = ast.literal_eval(myString)
                myDictionary.setdefault(ns, {}).setdefault('uiData', myUiDictionary[ns])
                
            
            with open(destFile, 'w') as f:
                json.dump(myDictionary, f, sort_keys=True, indent=4)
                
            MGlobal.displayInfo('[INFO] %s exported to %s' % (grp, destFile))

        else:
            MGlobal.displayInfo('[INFO] Export cancelled')

    # Procedure to change button color on the picker window
    def changeButtonColor(self, selButton, color):
        mc.button(selButton, e=True, bgc=color)
        self.saveUiData(self.tabLayout)

    # Dummy procedure to use with 'dropButton'
    def dragButton(self, draggedButton, x, y, modifier):
        pass
        
    # Procedure to implement 'drag and drop' of buttons on picker window
    def dropButton(self, draggedButton, droppedButton, messages, x, y, dragType):

        draggedButton = mc.button(draggedButton, q=True, p=True)
        
        if draggedButton == droppedButton:
            return

        myParentLayout = mc.layout(draggedButton, q=True, p=True)
        
        myTempLayout = mc.columnLayout(manage=False, parent=self.mainWindowLayout)
        myDraggedLayout = mc.columnLayout(manage=False, parent=self.mainWindowLayout)
        
        allMyButtons = mc.layout(myParentLayout, q=True, ca=True)

        #UNPARENT
        for myButton in allMyButtons:
            if myButton == draggedButton.split('|')[-1]:
                mc.layout(myButton, e=True, p=myDraggedLayout)
            else:
                mc.layout(myButton, e=True, p=myTempLayout)
                
        #REPARENT
        allMyTempButtons = mc.layout(myTempLayout, q=True, ca=True)
        myDroppedButton = mc.layout(myDraggedLayout, q=True, ca=True)
        
        for myTempButton in allMyTempButtons:
            if myTempButton != droppedButton.split('|')[-1]:
                mc.layout(myTempButton, e=True, p=myParentLayout)
            else:
                if y < self.buttonHeight / 2:
                    mc.layout(myDroppedButton[0], e=True, p=myParentLayout)
                    mc.layout(myTempButton, e=True, p=myParentLayout)
                else:
                    mc.layout(myTempButton, e=True, p=myParentLayout)
                    mc.layout(myDroppedButton[0], e=True, p=myParentLayout)

        mc.deleteUI(myDraggedLayout)
        mc.deleteUI(myTempLayout)
        self.saveUiData(self.tabLayout)

    # Procedure to impement 'Maya like selection behavior' on picker's window
    # Now you can replace, add and toggle selection from the UI with ctrl and shift
    def selectButton(self, objects, *args):

        mods = mc.getModifiers()
        if (mods == 1):
            mc.select(objects, tgl=True)
        elif (mods == 4):
            mc.select(objects, d=True)
        elif (mods == 5):
            mc.select(objects, add=True)
        else:
            mc.select(objects, r=True)

    # Procedure to save customized UI with the scene. Data is hold
    # by a 'blindDataTemplate' node (animSelectorUiData.data)
    def saveUiData(self, tabs):
    
        customUiData = {}
    
        for tabMainLayout in mc.tabLayout(tabs, q=True, ca=True):
            namespaceText, characterText, draggableLayout, extraButtons = mc.columnLayout(tabMainLayout, q=True, ca=True)
            myNamespace = mc.text(namespaceText, q=True, l=True)
            myCharacter = mc.text(characterText, q=True, l=True)
            myButtons = [[mc.button(mc.columnLayout(myPlaceHolder, q=True, ca=True)[0], q=True, l=True), mc.button(mc.columnLayout(myPlaceHolder, q=True, ca=True)[0], q=True, bgc=True)] for myPlaceHolder in mc.columnLayout(draggableLayout, q=True, ca=True)]
            
            customUiData.setdefault(myNamespace, myButtons)
        
        # HACK FOR FOCUS
        currSel = mc.ls(sl=True)
        
        if not mc.objExists('animSelectorUiData'):
            mc.createNode('blindDataTemplate', n='animSelectorUiData')

        if not mc.objExists('animSelectorUiData.data'):
            mc.addAttr('animSelectorUiData', longName='data', dataType="string")
            mc.setAttr('animSelectorUiData.data', e=True, keyable=False)
        
        # if mc.objExists('animSelectorUiData'):
            # if mc.objExists('animSelectorUiData.data'):
                # pass
            # else:
                # mc.addAttr('animSelectorUiData', longName='data', dataType="string")
                # mc.setAttr('animSelectorUiData.data', e=True, keyable=False)
        # else:
            # mc.createNode('blindDataTemplate', n='animSelectorUiData')
            # mc.addAttr('animSelectorUiData', longName='data', dataType="string")
            # mc.setAttr('animSelectorUiData.data', e=True, keyable=False)

        mc.setAttr('animSelectorUiData.data', customUiData, type='string')
        
        if currSel:
            mc.select(currSel, r=True)
        else:
            mc.select(cl=True)
            
    # Procedure to restore the custom UI from animSelectorUiData
    def restoreCustomUi(self, *args):
    
        dFullTemp = {}
        dTemp = {}
        for oUiData in mc.ls(type='blindDataTemplate'):
            if oUiData.split(':')[-1] == 'animSelectorUiData' and len(oUiData.split(':')) == 2:
                # print 'inside uiData loop'
                sNamespace = oUiData.split(':')[0]
                
                sMyTempString = mc.getAttr('%s.data' % oUiData)
                dTemp = ast.literal_eval(sMyTempString)
                dTemp[sNamespace] = dTemp.pop(dTemp.keys()[0])
                dFullTemp.update(dTemp)
                
        if dFullTemp:
            # print 'dFullTemp exists'
            if not mc.objExists('animSelectorUiData'):
                print 'animSelect node not exists'
                mc.createNode('blindDataTemplate', n='animSelectorUiData')

            if not mc.objExists('animSelectorUiData.data'):
                # print 'data attr not exists'
                mc.addAttr('animSelectorUiData', longName='data', dataType="string")
                mc.setAttr('animSelectorUiData.data', e=True, keyable=False)
                
                mc.setAttr('animSelectorUiData.data', '{}', type='string')
    
    
        if mc.objExists('animSelectorUiData.data'):
            myString = mc.getAttr('animSelectorUiData.data')
            myDictionary = ast.literal_eval(myString)
            
            if dFullTemp:
                dFullTemp.update(myDictionary)
                myDictionary = dFullTemp
            
            myList = []
            for tabMainLayout in mc.tabLayout(self.tabLayout, q=True, ca=True):
                namespaceText, characterText, draggableLayout, extraButtons = mc.columnLayout(tabMainLayout, q=True, ca=True)
                myList.append(mc.text(namespaceText, q=True, l=True))
            
            # for myNamespace in myDictionary:
            for myNamespace in (set(myList) & set(myDictionary)):
            
                tempButtonsLayout = mc.columnLayout(manage=False, p=self.mainWindowLayout)
                
                for myButton in myDictionary[myNamespace]:
                    # TRY TO RESTORE BUTTONS' COLOR AND POSITION 
                    try:
                        mc.button(self.buttonList[myNamespace][myButton[0]][0], e=True, bgc=myButton[1])
                    except:
                        pass

                    # UNPARENT LAYOUTS
                    try:
                        oldParent = mc.layout(self.buttonList[myNamespace][myButton[0]][1], q=True, p=True)
                        mc.layout(self.buttonList[myNamespace][myButton[0]][1], e=True, p=tempButtonsLayout)
                    except KeyError:
                        pass
                
                #REPARENT LAYOUTS
                try:
                    for myButton in mc.layout(tempButtonsLayout, q=True, ca=True):
                        mc.layout(myButton, e=True, p=oldParent)
                except:
                    pass
            
                mc.deleteUI(tempButtonsLayout)
    
class PrefsUI():
    # Main window
    def __init__(self, *args):
        self.name = 'animSelectorPrefsUI'
        self.title = 'animSelector :: Preferences'
        self.selectionBehavior = mc.optionVar(q='animSelector_hotKeySelectionToggle') + 1
        self.pickerButtonsHeight = mc.optionVar(q='animSelector_pickerButtonsHeight')
        self.dockable = mc.optionVar(q='animSelector_dockable')
        
        # Begin creating the UI
        if (mc.window(self.name, q=1, exists=1)): mc.deleteUI(self.name)
        self.window = mc.window(self.name, title=self.title, menuBar=False, s=False)

        self.mainWindowLayout = mc.columnLayout(adj=1)

        self.prefLayout = mc.columnLayout(adj=1, p=self.mainWindowLayout)
        mc.text(l='Custom Button Colors', h=25, bgc=[.125,.125,.125])
        colorVariables =[
                            ['First',      mc.optionVar(q='animSelector_firstColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_firstColor_color'))],
                            ['Second',     mc.optionVar(q='animSelector_secondColor_name'),     ast.literal_eval(mc.optionVar(q='animSelector_secondColor_color'))],
                            ['Third',      mc.optionVar(q='animSelector_thirdColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_thirdColor_color'))],
                            ['Fourth',     mc.optionVar(q='animSelector_fourthColor_name'),     ast.literal_eval(mc.optionVar(q='animSelector_fourthColor_color'))],
                            ['Fifth',      mc.optionVar(q='animSelector_fifthColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_fifthColor_color'))],
                            ['Sixth',      mc.optionVar(q='animSelector_sixthColor_name'),      ast.literal_eval(mc.optionVar(q='animSelector_sixthColor_color'))],
                            ['Seventh',    mc.optionVar(q='animSelector_seventhColor_name'),    ast.literal_eval(mc.optionVar(q='animSelector_seventhColor_color'))],
                            ['Eighth',     mc.optionVar(q='animSelector_eighthColor_name'),     ast.literal_eval(mc.optionVar(q='animSelector_eighthColor_color'))]
                        ]
                        
        mc.text(l='', p=self.prefLayout)
        for col in colorVariables:
            rl = mc.rowLayout(nc=2, p=self.prefLayout)
            n = mc.textFieldGrp('%s_name' % col[0],l=col[0], text=col[1], cal=[1, 'left'], cw2=[60, 90], p=rl)
            c = mc.colorSliderGrp('%s_color' % col[0], rgb=col[2], cw2=[15, 128], p=rl)

        mc.text(l='', p=self.prefLayout)    
        mc.text(l='Hotkey Behavior', h=25, bgc=[.125,.125,.125], p=self.prefLayout)
        mc.text(l='', p=self.prefLayout)
        self.hotKeysSelectionBehavior = mc.radioButtonGrp(  
                                                            label='Hotkey selection behavior:', 
                                                            labelArray3=['Remove', 'Toggle', 'Add'], 
                                                            numberOfRadioButtons=3, 
                                                            vr=True, 
                                                            sl=self.selectionBehavior, 
                                                            p=self.prefLayout
                                                         )
        mc.text(l='', p=self.prefLayout)
        
        mc.text(l='Extras', h=25, bgc=[.125,.125,.125], p=self.prefLayout)
        mc.text(l='', p=self.prefLayout)
        # mc.intField('pHeight', v=self.pickerButtonsHeight, p=self.prefLayout)
        mc.intSliderGrp('pHeight', field=True, label='Button height', minValue=12, maxValue=80, w=50, v=self.pickerButtonsHeight, p=self.prefLayout)
        mc.checkBoxGrp('pDock', columnWidth2=[143, 165], numberOfCheckBoxes=1, label='Dockable picker', label1='(Maya2011+)', v1=self.dockable, p=self.prefLayout)
        mc.text(l='', p=self.prefLayout)
        
        self.buttonLayout = mc.columnLayout(adj=True, p=self.mainWindowLayout)
        okButton = mc.button(l='Save', c=self.savePrefs, p=self.buttonLayout, w=100)
        mc.showWindow(self.window)
        
    # Procedure to save custom preferences to userPrefs.mel
    def savePrefs(self, *args):
    
        mc.optionVar(sv=['animSelector_firstColor_name', mc.textFieldGrp('First_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_firstColor_color', str(mc.colorSliderGrp('First_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_secondColor_name', mc.textFieldGrp('Second_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_secondColor_color', str(mc.colorSliderGrp('Second_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_thirdColor_name', mc.textFieldGrp('Third_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_thirdColor_color',str(mc.colorSliderGrp('Third_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_fourthColor_name', mc.textFieldGrp('Fourth_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_fourthColor_color', str(mc.colorSliderGrp('Fourth_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_fifthColor_name', mc.textFieldGrp('Fifth_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_fifthColor_color', str(mc.colorSliderGrp('Fifth_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_sixthColor_name', mc.textFieldGrp('Sixth_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_sixthColor_color', str(mc.colorSliderGrp('Sixth_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_seventhColor_name', mc.textFieldGrp('Seventh_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_seventhColor_color', str(mc.colorSliderGrp('Seventh_color', q=True, rgb=True))])

        mc.optionVar(sv=['animSelector_eighthColor_name', mc.textFieldGrp('Eighth_name', q=True, text=True)])
        mc.optionVar(sv=['animSelector_eighthColor_color', str(mc.colorSliderGrp('Eighth_color', q=True, rgb=True))])

        myValue = (mc.radioButtonGrp(self.hotKeysSelectionBehavior, q=True, sl=True)) - 1
        mc.optionVar(iv=('animSelector_hotKeySelectionToggle', myValue))
        
        myValue = mc.intSliderGrp('pHeight', q=True, v=True)
        mc.optionVar(iv=('animSelector_pickerButtonsHeight', myValue))

        myValue = mc.checkBoxGrp('pDock', q=True, v1=True)
        mc.optionVar(iv=('animSelector_dockable', myValue))
        
        mc.savePrefs(g=True)
        if (mc.window(self.name, q=1, exists=1)): mc.deleteUI(self.name)
        
class HelpUI():
    def __init__(self, *args):
        self.name = "animSelectorHelpUI"
        self.title = "animSelector :: Help"
        self.mainLabelHeight = 25
        
        self.helpData = {
            'general' : ['\nAnimSelector is a maya script that lets you create selection sets for' +
                        ' your rigs that can then be selected from a picker window.\n' +
                        '\n' +
                        'It is extremely useful both when your rig came with no GUI and when yo' +
                        'u need to extend the controls on an existing one.\n' +
                        '\n' +
                        'To use the script, copy "animSelector.py" and the "help" folder to you' +
                        'r maya script folder\n' +
                        '(on windows c:\Users\YOUR_USER_NAME\Documents\maya\scripts\)\n' +
                        'and the icons to your icon folder\n' +
                        '(on windows c:\Users\YOUR_USER_NAME\Documents\maya\YOUR_MAYA_VERSION\p' +
                        'refs\icons\).\n' +
                        'Then open Maya and type in the script editor (in a python tab)\n' +
                        '\n' +
                        '\n' +
                        'import animSelector\n' +
                        'animSelector.install()\n' +
                        ' \n' +
                        ' \n' +
                        'It will create a shelf tab and two buttons, one for the setup and one ' +
                        'for the picker.\n\n',
                        
                        '\n*Fast selection sets creation\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '*Namespace indipendent setups\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '*Import/Export of setup\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '*Draggable and re-organizable buttons on the picker\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '*Color customizable buttons on the picker\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '*Easy hotkey assignment to selection sets\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '*Hotkeys "per character" can be saved to shelf for easy switching\n',
                        
                        'animSelector v1.3.4 (April 2013)\n' +
                        '\n' +
                        '\n' +
                        'Original idea developed with:\n' +
                        'Lee Croudy,\n' +
                        'Alberto Gracia Galera,\n' + 
                        '\n' +
                        'Coded  by:\n' + 
                        'Luca Fiorentini,\n' + 
                        '\n' +
                        'Thanks to:\n' +
                        'Roberto Zincone,\n' +
                        'Bomb La Tour\n' +
                        'for beta testing\n' +
                        '\n' +
                        'Many many thanks to\n' +
                        'Ansgar Diewald\n' +
                        'for helping me out with the "drag \'n drop" code on the picker\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        '\n' +
                        'luca.fiorentini@gmail.com\n' +
                        'lucafiorentini.wordpress.com'],
                        
            'setup' : [ 'This is the main window and lets you setup the selection sets on your character.',

                        'A) Char Name: Input here the name of your character.\n' +
                        '\n' +
                        'B) Ctrl Name: Input here the name of selection sets.\n' +
                        '\n' +
                        'C) Replace: This button lets you assign the selected object(s) to a ne' +
                        'w or existing selection sets.  If any of the selected objects are pres' +
                        'ent in other selection sets they will be removed and reassigned only ' +
                        'to the named selection sets (in field B)\n' +
                        '\n' +
                        'D) Add: This button allows you to add selected objects to a new or exi' +
                        'sting selection sets.  Selected objects can be assigned multiple selec' +
                        'tion sets (eg. an FKwristLeft control can exist in the "HandLft", "FK"' +
                        '"armChainLft", and "All") \n' +
                        '\n' +
                        'E) Remove: This button lets you completely clear the selected object(s' +
                        ') from all the custom attributes (i.e.: they will not be in any select' +
                        'ion sets).\n' +
                        '\n' +
                        'F) Select Objs Without Attribute: This button lets you all the objects' +
                        ' that miss at least one selection sets attribute. It comes in handy wh' +
                        'en you want to check if all of your controls have been set.\n' +
                        '\n' +
                        'G) Picker: This button lets you open the picker window.\n' +
                        '\n' +
                        'H) Get Name:  This button let fill the "Char Name" field with the curr' +
                        'ently active picker tab in case you want to add a new selection sets a' +
                        'nd you want to avoid typos.\n',
                        
                        'I) File/Import:  The setup of the character can be exported to an exte' +
                        'rnal file (from the picker window) and then re-imported in another sho' +
                        't. The normal import lets you import the data back and re assing it to' +
                        ' the same character. In case the namespaces are different between the ' +
                        'shots, a window will popup letting you chose the correct one.\n' +
                        '\n' +
                        'L) File/Import and remap:  This option lets you assign the setup to an' +
                        'other character in the scene. The controls have to be the same, so it ' +
                        'should be \n' +
                        '    >> A second reference of the same file (like when you do duplicate' +
                        ' reference from the reference editor\n' +
                        '    >> A similar setup to the original file (like crowds or extras)\n' +
                        '\n' +
                        'M) File/Help:  Opens the "help" window.\n' +
                        '\n' +
                        'N) Edit/Preferences:  Opens the "preferences" window.\n' + 
                        '\n' + 
                        'O) Update: Attribute names have changed in v1.3.4 to improve compati' + 
                        'bility (like with "Malcom Rig".\n' +
                        'You can update the old setups to work with the new version with this function\n'],
                        
            'picker' : ['This is the picker window. From here you can select your controls back' +
                        '.\n' +
                        'Buttons on the picker are draggable, letting you reorganize the window' +
                        ' as you prefer (for example you can put the most used buttons on top).' +
                        '\n' +
                        'You can drag and drop with the middle mouse button and the behavior  i' +
                        's as follow:\n' +
                        'if you have buttons A, B, and C and you drop button C on the lower hal' +
                        'f of button B, it will go below button B, otherwise it will go over bu' +
                        'tton B\n' +
                        'If you want to open this window without opening the setup one, you can' +
                        ' use this python code:\n' +
                        '\n' +
                        'import animSelector\n' +
                        'animSelector.PickerUI()\n',
                        
                        'A) Tabs: Every character will be split in his own tab.\n' +
                        '\n' +
                        'B) Buttons: From here you can select your controls back. The selection' +
                        ' behavior is the same as in the viewport:\n' +
                        '    >> Click to select.\n' +
                        '    >> SHIFT + click to toggle the selection.\n' +
                        '    >> CTRL + click to deselect.\n' +
                        '\n' +
                        'C) Remove Set From Scene: This will remove the selection sets from all' +
                        ' the objects in the scene\n' +
                        '\n' +
                        'D) Remove Set From Selection: This will remove the selection sets from' +
                        ' the selected objects.\n' +
                        '\n' +
                        'E) Rename button: This will let you rename the button (and so the selec' +
                        'tion set) from the picker.\n' +
                        '\n' +
                        'F) Change Button Color: Is now possible to change the color of the but' +
                        'tons to create some "color groups"',
                        
                        'for easier access.\n' +
                        'The name of the colors and their values can be changed in the preferen' +
                        'ce window.\n'
                        '\n' + 
                        'G) Assign #### Hotkey: From here you can assign an hotkey to the selec' +
                        'tion of the selection sets. Hotkeys go from 0 to 9 and can use the CTR' +
                        'L or ALT modifier. The selection behavior (replace, toggle or add) can' +
                        ' be set in the preference window.\n' +
                        '\n' +
                        'H) Hotkeys To Shelf: Hotkeys for each tab (i.e. each character) can be' +
                        ' saved to the shelf being able to switch between them with just one cl' +
                        'ick.\n' +
                        '\n' +
                        'I) Export: The recommended workflow is to setup the file that will be ' +
                        'referenced, so the selection sets will be in every scene.\n' +
                        'However, if you are not able to, you can export the setup to an extern' +
                        'al file and import it in another scene.\n'],

            'preferences' : ['\nFrom here you can set your preferences for the tool.\n\n\n',

                            '\nA) Custom Button Colors: Here you can chose the label and the color to' +
                            ' use to color the picker s buttons.\n' +
                            '\n' +
                            'B) Hotkeys Behavior: Here you can chose the selection behavior (replac' +
                            'e, toggle or add) for the hotkeys.\n' +
                            '\n' +
                            'C) Button size: Here you can chose the size of the buttons on the picker.\n' +
                            '\n' +
                            'D) Dockable Picker: Check it if you want to be able to dock the picker to ' +
                            'the interface.\n' + 
                            'Please note that this will have NO effect on Maya versions prior to 2011\n\n' +
                            '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'],
            }

        # Begin creating the UI
        if (mc.window(self.name, q=1, exists=1)): mc.deleteUI(self.name)
        self.window = mc.window(self.name, title=self.title, menuBar=False, s=False)

        self.mainWindowLayout = mc.columnLayout(adj=1)
        self.tabLayout = mc.tabLayout(p=self.mainWindowLayout)

        #GENERAL TAB
        self.myLayout = mc.columnLayout(adj=1, p=self.tabLayout)
        self.myRow = mc.rowLayout(nc=2, p=self.myLayout)
        self.myColumn = mc.columnLayout(p=self.myRow)
        self.myTitle = mc.text(l='General Info and Features', w=580, bgc=[.125,.125,.125], h=self.mainLabelHeight, p=self.myColumn)
        self.myText = mc.text(self.helpData['general'][0], w=580, al='center', fn="boldLabelFont", ww=True, p=self.myColumn)
        self.myImage = mc.image( image=self.searchImage('animSelector_logo.jpg'), p=self.myRow)
        
        self.myRow = mc.rowLayout(nc=2, p=self.myLayout)
        
        self.myColumnL = mc.columnLayout(p=self.myRow)
        mc.text(l='Features', bgc=[.125,.125,.125], w=580, h=15, p=self.myColumnL)
        self.myText = mc.text(self.helpData['general'][1], w=580, h=360, al='center', fn="boldLabelFont", ww=True, p=self.myColumnL)
        
        self.myColumnR = mc.columnLayout(p=self.myRow)
        mc.text(l='About', bgc=[.125,.125,.125], w=200, h=15, p=self.myColumnR)
        self.myText = mc.text(self.helpData['general'][2], w=200, h=360, al='center', fn="smallBoldLabelFont", ww=True, bgc=[.15, .15, .15], p=self.myColumnR)
        # self.myText = mc.scrollField(tx=self.helpData['general'][2], w=200, h=360, ed=False, fn="smallBoldLabelFont", p=self.myColumnR)
        
        mc.tabLayout( self.tabLayout, edit=True, tabLabel=(self.myLayout, 'General'))

        #SETUP TAB
        self.myLayout = mc.columnLayout(adj=1, p=self.tabLayout)
        self.myTitle = mc.text(l='Setup Window', bgc=[.125,.125,.125], h=self.mainLabelHeight)
        self.myScroll = mc.scrollLayout(p=self.myLayout, h=650)
        self.myColumn = mc.columnLayout(p=self.myScroll)
        self.myText = mc.text(self.helpData['setup'][0], w=740, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        self.otherRow = mc.rowLayout(nc=2, cl2=['left', 'right'], p=self.myColumn)
        mc.text('                        ', p=self.otherRow)
        self.myImage = mc.image( image=self.searchImage('animSelector_setupWindow.jpg'), p=self.otherRow)
        mc.text(l='Widgets', bgc=[.125,.125,.125], w=740, h=15, p=self.myColumn)
        self.myRow = mc.rowLayout(nc=2, p=self.myColumn)
        self.myText = mc.text(self.helpData['setup'][1],w=410, al='left', fn="boldLabelFont", ww=True, p=self.myRow)
        self.myImage = mc.image( image=self.searchImage('animSelector_namespaceChooserWindow.jpg'), p=self.myRow)
        self.myText = mc.text(self.helpData['setup'][2],w=730, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        mc.tabLayout( self.tabLayout, edit=True, tabLabel=(self.myLayout, 'Setup'))
        
        #PICKER TAB
        self.myLayout = mc.columnLayout(adj=1, p=self.tabLayout)
        self.myTitle = mc.text(l='Picker Window', bgc=[.125,.125,.125], h=self.mainLabelHeight)
        self.myScroll = mc.scrollLayout(p=self.myLayout, h=650)
        self.myRowLayout = mc.rowLayout(nc=2, p=self.myScroll)
        self.myImage = mc.image( image=self.searchImage('animSelector_pickerWindow.jpg'))
        self.myColumn = mc.columnLayout()
        self.myText = mc.text(self.helpData['picker'][0], w=330, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        mc.text(l='Widgets', bgc=[.125,.125,.125], w=330, h=15, p=self.myColumn)
        self.myText = mc.text(self.helpData['picker'][1], w=330, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        self.myText = mc.text(self.helpData['picker'][2], w=755, al='left', fn="boldLabelFont", ww=True, p=self.myScroll)
        mc.tabLayout( self.tabLayout, edit=True, tabLabel=(self.myLayout, 'Picker'))
        
        # PREFERENCES TAB
        self.myLayout = mc.columnLayout(adj=1, p=self.tabLayout)
        self.myTitle = mc.text(l='Preferences Window', bgc=[.125,.125,.125], h=self.mainLabelHeight)
        self.myScroll = mc.scrollLayout(p=self.myLayout, h=600)
        self.myRowLayout = mc.rowLayout(nc=2, p=self.myScroll)
        self.myColumn = mc.columnLayout(p=self.myRowLayout)
        self.myText = mc.text(self.helpData['preferences'][0], w=400, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        mc.text(l='Widgets', bgc=[.125,.125,.125], w=400, h=15, p=self.myColumn)
        self.myText = mc.text(self.helpData['preferences'][1], w=400, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        self.myImage = mc.image( image=self.searchImage('animSelector_preferencesWindow.jpg'), p=self.myRowLayout)
        # mc.text(l='Widgets', bgc=[.125,.125,.125], w=330, h=15, p=self.myColumn)
        # self.myText = mc.text(self.helpData['picker'][1], w=330, al='left', fn="boldLabelFont", ww=True, p=self.myColumn)
        # self.myText = mc.text(self.helpData['picker'][2], w=755, al='left', fn="boldLabelFont", ww=True, p=self.myScroll)
        mc.tabLayout( self.tabLayout, edit=True, tabLabel=(self.myLayout, 'Preferences'))
        
        mc.showWindow(self.window)
        mc.window(self.window, e=1, w=800, h=600)
        
    def searchImage(self, imageName):
        for myPath in sys.path:
            myString = '%s/help/%s' % (myPath, imageName)
            if os.path.isfile(myString):
                return myString
                
# Class used to pass arguments to commands (like with buttons)
class Callback(object): 
        def __init__(self, func, *args, **kwargs): 
                self.func = func 
                self.args = args 
                self.kwargs = kwargs
        def __call__(self, *args): 
                return self.func( *self.args, **self.kwargs )

# Procedure used to build the nested dictionary to pass data to the UI                
def getDataBack():
    dizGroup = {}

    for obj in mc.ls(type='transform'):
        if mc.objExists(obj + ('.animSelectorCharName')):
        
            #THIS IS TO GET THE NAMESPACE OF THE OBJECT
            # BUT I AM SURE THERE IS A BETTER WAY, REMEMBER TO CHECK IT
            charNamespace = obj.split(':')
            charName = mc.getAttr(obj + ('.animSelectorCharName'))
            ctrlName = mc.getAttr(obj + ('.animSelectorCtrlName'))
            
            if len(charNamespace) > 1:
                charNamespace = charNamespace[0]
            else:
                charNamespace = charName
            
            #REMOVE WHITESPACES FROM ctrlName
            ctrlName = re.sub(r'\s', '', ctrlName)
            ctrlNameList = ctrlName.split(',')

            if charNamespace not in dizGroup:
                dizGroup[charNamespace] = {}
            
            if charName not in dizGroup[charNamespace]:
                dizGroup[charNamespace][charName] = {}
            
            for ctrl in ctrlNameList:
                if ctrl not in dizGroup[charNamespace][charName]:
                    dizGroup[charNamespace][charName][ctrl] = []
    
                dizGroup[charNamespace][charName][ctrl].append(obj)

    return dizGroup

def replaceNamespace(old, new, myDictionary):

    for myNamespace in myDictionary:
        for myCharacter in myDictionary[myNamespace]:
            for myControl in myDictionary[myNamespace][myCharacter]:
                tempList = []
                try:
                    for myValue in myDictionary[myNamespace][myCharacter][myControl]:
                        # NAMESPACE TO NAMESPACE
                        if len(myValue.split(':')) > 1:
                            tempList.append(myValue.replace('%s:' % old, '%s:' % new))
                        # NO NAMESPACE TO NAMESPACE
                        else:
                            nsList = ['%s:%s' % (new, myItem) for myItem in myValue.split('|')]
                            tempList.append('|'.join(nsList))
                    
                    myDictionary[myNamespace][myCharacter][myControl] = tempList
                # THIS IS TO IGNORE THE uiData VALUES IN THE DICTIONARY
                except TypeError:
                    pass
                
    myDictionary[new] = myDictionary.pop(old)

    return myDictionary
  
# Custom modal UI layout to chose the namespace. This is used by SetupUI.importData
def namespaceChooser():

    myList = []
    allReferences = mc.ls(r=True, rf=True)

    # for myReference in allReferences:
        # myList.append(mc.referenceQuery(myReference, ns=True, shn=True))

    myList = sorted(mc.namespaceInfo(lon=True))
    
    myColumnLayout = mc.columnLayout(adj=1)
    text = mc.text(l='List of namespaces in the scene:', bgc=[.125,.125,.125], h=35, p=myColumnLayout)
    textScroll = mc.textScrollList('namespaceTextScroll', numberOfRows=16, allowMultiSelection=False, append=myList, p=myColumnLayout)
    myRowLayout = mc.rowLayout(nc=2, p=myColumnLayout)
    # cancelButton = mc.button(l='Cancel', width=142, c='import maya.cmds as mc\nmc.layoutDialog( dismiss="Cancel" )', p=myRowLayout)
    cancelButton = mc.button(l='Cancel', width=142, c='import maya.cmds as mc\nmc.layoutDialog( dismiss="animSelectorNamespaceCancel" )', p=myRowLayout)
    okButton = mc.button(l='Ok', width=142, c='import maya.cmds as mc\nmc.layoutDialog( dismiss=(mc.textScrollList("namespaceTextScroll", q=True, si=True))[0])', p=myRowLayout)

def updateSetup(*args):
    updateCheck = False
    for ctrl in mc.ls(type='transform', l=True):
        
        if mc.objExists('%s.charName' % ctrl):
            myValue = mc.getAttr('%s.charName' % ctrl)
            
            if not mc.objExists('%s.animSelectorCharName' % ctrl):
                mc.addAttr(ctrl, longName='animSelectorCharName', dataType="string")
                mc.setAttr('%s.animSelectorCharName' % ctrl, e=True, keyable=False)
                
            mc.setAttr('%s.animSelectorCharName' % ctrl, myValue, type='string')
            mc.deleteAttr(ctrl, at='charName')
            updateCheck = True
            
        if mc.objExists('%s.ctrlName' % ctrl):
            myValue = mc.getAttr('%s.ctrlName' % ctrl)
            
            if not mc.objExists('%s.animSelectorCtrlName' % ctrl):
                mc.addAttr(ctrl, longName='animSelectorCtrlName', dataType="string")
                mc.setAttr('%s.animSelectorCtrlName' % ctrl, e=True, keyable=False)
                
            mc.setAttr('%s.animSelectorCtrlName' % ctrl, myValue, type='string')
            mc.deleteAttr(ctrl, at='ctrlName')
            updateCheck = True
            
    if updateCheck:
        MGlobal.displayInfo('[INFO] Setup updated')
    else:
        MGlobal.displayInfo('[INFO] Nothing to update')
        
def install():

    newShelfName = 'animSelector'
    mainShelf = maya.mel.eval('string $myMainShelf = $gShelfTopLevel;')
    allShelves = mc.shelfTabLayout(mainShelf, query=True, tabLabelIndex=True)

    if newShelfName not in allShelves:
        animSelectorShelf = maya.mel.eval('addNewShelfTab %s' % newShelfName)
    else:
        MGlobal.displayInfo('[INFO] animSelector shelf already exists')
        animSelectorShelf = mc.shelfTabLayout(mainShelf, e=True, st=newShelfName)
    
    shelfButtons = mc.shelfLayout(newShelfName, q=True, ca=True)
    
    if not shelfButtons or 'animSelector_setupButton' not in shelfButtons:
        mc.shelfButton('animSelector_setupButton', parent='animSelector', i='animSelector_setup.png', c='import animSelector\nanimSelector.SetupUI()', l='asd')
    
    if not shelfButtons or 'animSelector_pickerButton' not in shelfButtons:
        mc.shelfButton('animSelector_pickerButton', parent='animSelector', i='animSelector_picker.png', c='import animSelector\nanimSelector.PickerUI()')
        
    if not shelfButtons or 'animSelector_spacer' not in shelfButtons:
        mc.shelfButton('animSelector_spacer', parent='animSelector', i='animSelector_spacer.png', c='pass', w=4)    
        