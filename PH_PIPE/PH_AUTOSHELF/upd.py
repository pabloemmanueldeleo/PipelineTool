#upd
import maya.cmds as cmds
import maya.mel as mel
global shelves
shelves=[
    'shelf_PH_FIX',
    'shelf_PH_LIGHTING',
    'shelf_PH_MODEL',
    'shelf_PH_RENDER',
    'shelf_PH_RIG',
    'shelf_PH_SHADER',
    'shelf_PH_VFX',
	'shelf_PH_ANIM',
    ]
def theShelves():
    global shelves
    for shelf in shelves:
        if (cmds.shelfLayout (shelf.split('shelf_')[1],q=1,ex=1) ):
            cmds.deleteUI(shelf.split('shelf_')[1], lay=1) 
            mel.eval('loadNewShelf "M:/PH_SCRIPTS/SHELF/'+ shelf + '.mel";')
        else:    
            mel.eval('loadNewShelf "M:/PH_SCRIPTS/SHELF/'+ shelf + '.mel";')
    
def printShelves():
	global shelves
	for shelf in shelves:
		print shelf

def shelfGabo():
    global shelves
    for shelf in shelves:
        if (cmds.shelfLayout ("Gabo",q=1,ex=1) ):
            cmds.deleteUI("Gabo", lay=1) 
            mel.eval('loadNewShelf "M:/Maya_Script/shelf_Gabo.mel";')
        else:    
            mel.eval('loadNewShelf "M:/Maya_Script/shelf_Gabo.mel";')	
		
def printDefs():
	print '.theShelves(): actualiza shelfs'
	print '.printShelves(): muestra los shelves que se actualizarían con .theShelves()'
	print '.shelfGabo(): carga shelf Gabo de Maya_Script. si existe, lo borra primero.'
	
	
	
	
	
	
	
	
	
	
	
	
	