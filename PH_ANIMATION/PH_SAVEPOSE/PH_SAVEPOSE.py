import maya.cmds as cmds

annotationDict = {}
timeRange = [0,0]


def SaveFrameRange(option):
    timeRange[0] = cmds.playbackOptions(query=True, min=True)
    timeRange[1] = cmds.playbackOptions(query=True, max=True)
    selectedItem = cmds.textScrollList('timeRange', query=True, si=True)
    
    if option == "Save":
        itemName = raw_input("Name your animation")
    if itemName in annotationDict:
        print "Use a unique name!"
    elif itemName == "":
        print "Nothing entered"
    else:
        annotationDict[itemName] = str(timeRange)
        cmds.textScrollList('timeRange', edit=True, append=itemName )
    
    if option == "Restore":
        frameRange = eval( annotationDict[selectedItem[0] ] )
        cmds.playbackOptions(min= frameRange[0], max= frameRange[1] )
    
    if option == "Delete":
        print "Deleting " + selectedItem
        del annotationDict[selectedItem[0] ]
        cmds.textScrollList('timeRange', edit=True, removeItem= selectedItem)


def HelperUI():

    helperWindow = cmds.window(t="Animation Helper")
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    
    #tab 1
    child1 = cmds.rowColumnLayout(backgroundColor=(.2,.3,.4), numberOfColumns=3)
    scrollList = cmds.textScrollList('timeRange', selectCommand=lambda *args:SaveFrameRange )
    cmds.button( label='Set Frame Range', command=lambda *args:SaveFrameRange("Save") )
    cmds.button( label='Restore Frame Range', command=lambda *args:SaveFrameRange("Restore") )
    cmds.button( label='Remove Frame Range', command=lambda *args:SaveFrameRange("Delete") )
    cmds.setParent( '..' ) 
    
    #tab 2
    child2 = cmds.rowColumnLayout(backgroundColor=(.3,.4,.2), numberOfColumns=3)
    cmds.text( label="Save Selection") 
    cmds.button( label='Save', command="do something" ) 
    cmds.setParent( '..' )
    
    #tab 3
    child3 = cmds.rowColumnLayout(backgroundColor=(.4,.2,.3), numberOfColumns=3)
    cmds.setParent('..')
    
    #name the tabs and call them
    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Frame Range'), (child2, 'Selection Sets'), (child3, 'Other')) )
    cmds.showWindow( helperWindow )

HelperUI()