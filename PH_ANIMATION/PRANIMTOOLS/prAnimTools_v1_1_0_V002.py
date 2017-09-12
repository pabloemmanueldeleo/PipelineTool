"""------prAnimTools------"""                
#ver. 1.0 --- Oct 26th 2012
#created by Tan Pang Ren
#ver. 1.1 --- Nov 7th 2012
# ---- added stick forward and stick backward functionality
"""www.livingillusions.wordpress.com"""
###---------USES----------###
#solving simple animation production issues like feet sliding when importing walkcycles
#and
#simple and straightforward grabbing of objects.  

################# INSTRUCTIONS ######################
# open script editor , Python Tab 
# copy "prAnimTols.py" into script Editor (Python Tab) and run script 


import maya.cmds as cmd

class Fixit():
    def __init__(self):
        self.DaLocator=[]
        self.CurrentSelection=''
        
    #create UI
    def uiMain(self):
        if cmd.window('prSnaps', exists=True):
            cmd.deleteUI('prSnaps')
        cmd.window('prSnaps', title='prAnimTools ver 1.1', s=False, width= 300, height=100, bgc=(0.4,0.4,0.4), toolbox=1 )
        cmd.showWindow('prSnaps')
        cmd.columnLayout('clayout1', adjustableColumn =1, columnOffset=('both', 10))
        cmd.text(label = 'Snap functions:', align='left')
        cmd.rowLayout('rlayout1', numberOfColumns=4,height = 35)
        
        cmd.button( 'targetBtn', 
                        label='Target',
                        width=60,
                        command = lambda *args: self.makingLocator() 
                        )
        cmd.button( 'stickitBtnBk', 
                        label='- Stick',
                        width=50, enableBackground = True ,backgroundColor = [255,0,0],
                        command = lambda *args: self.stickitback() 
                        )
        cmd.button( 'stickitBtnFr', 
                        label='Stick +',
                        width=50, enableBackground = True ,backgroundColor = [255,0,0],
                        command = lambda *args: self.stickitfront() 
                        )        
                        
        cmd.button( 'delLoc', 
                        label='Clean Up',
                        width=70,
                        command = lambda *args: self.deleteLoc() 
                        )
        cmd.setParent("..")#rowlayout1 close
        
        cmd.text(label = 'Grab functions:', align = 'left')
    
        cmd.rowLayout('rlayout2', numberOfColumns=3,height = 30)
        
        cmd.button ('selectGrab',
                        label='Grab',
                        width = 60,enableBackground = True, backgroundColor = [0,100,100],
                        command = lambda *args: self.grab()
                        )
        cmd.button('releaseGrab',
                        label = 'Release',
                        width = 80,
                        command = lambda *args: self.releaseGrab() )
        cmd.setParent("..")#rowlayout2 close
         
            
           
    #DaLocator = [] #some global list. not important. 
    #CurrentSelection = '' #floating current selection    
    
    def makingLocator(self): 
        #global DaLocator # an addition to test out   
        #global CurrentSelection
        #Step 1 make a locator that is in the exact location as the Target.
        try:
            selection = cmd.ls(selection=True)[0]
            
            #print selection
        except:
            cmd.confirmDialog(title='Error dialog', message='Please Select a Target', messageAlign='left',
                    button='Ok', defaultButton='Ok', dismissString='Ok', icon='warning')
        else:
            #query selction's loction in worldspace
            worldTrans = cmd.xform(selection, worldSpace=True, query=True,translation=True)
            worldRot = cmd.xform(selection, worldSpace=True, query=True,rotation=True)
            
            #create locator in some position
            theLocator = cmd.spaceLocator(n='prAwesomeLocator')[0]
            #print theLocator
            cmd.setAttr(theLocator+'.translate',worldTrans[0],worldTrans[1],worldTrans[2],type = 'double3')
            cmd.setAttr(theLocator+'.rotate',worldRot[0],worldRot[1],worldRot[2],type = 'double3')
            #DaLocator.append(selection)
            self.DaLocator.append(theLocator) #i have no idea how this managed to work although DaLocator is global value
            self.CurrentSelection = selection
        
    
    def stickitfront(self):
        #Step 2 parent constraint and remove , the parent constraint then move one frame forward.
        #So the idea is click this as many times as you need to stick the foot
        
        theConstraint = cmd.parentConstraint ( self.DaLocator[-1], self.CurrentSelection , n ='myConstraint_parent',mo=False )[0]
        currentFrame = cmd.currentTime(query=True)
        cmd.setKeyframe (self.CurrentSelection)
        cmd.currentTime( currentFrame+1 , edit = True)#switched the order, so it keys first before moving on to next frame
        cmd.delete(theConstraint)
    
    def stickitback(self):
    
        theConstraint = cmd.parentConstraint ( self.DaLocator[-1], self.CurrentSelection , n ='myConstraint_parent',mo=False )[0]
        currentFrame = cmd.currentTime(query=True)
        cmd.setKeyframe (self.CurrentSelection)
        cmd.currentTime( currentFrame-1 , edit = True)#switched the order, so it keys first before moving on to next frame
        cmd.delete(theConstraint)
    
    def deleteLoc(self):
        #delete locator
        #the unfortunate consequence of creating a locator is the need to delete it. 
        #global DaLocator   #if you manipulate global values , you have to state that it is global 
        
        try:
            #print DaLocator[0] 
            #print DaLocator[1]
            for items in self.DaLocator :
                cmd.delete(items)
            
            self.DaLocator = []
        except:
            cmd.error("There are no locators to delete")
    
    def checkLocators(self):
        #global DaLocator
    
        locX = cmd.ls('prAwesomeLocator*',type='locator')##works
        for items in locX :
            self.DaLocator.append(cmd.listRelatives(items, parent = True)[0])
#---------------------------------------------------------------------------------#
    def grab(self):
        objectsSelected = []
        selection = cmd.ls(selection = True)
        #finding constraints
        #naming constraints
        findConstraint = cmd.ls('grabber*',type='parentConstraint')#list all parent constraints before tt's named *grabber
        counter=len(findConstraint)
        DaGrabber = 'grabber_'+str(counter)
        
        for item in selection :
            if len(selection) == 2 :
                objectsSelected.append(item)
            elif len(selection)>2 or len(selection)<2:
                cmd.error ("please select exactly 2 objects : a parent and a child")
        
        # the Grab
        DaParentLocator = self.makingParentLocator(selection[-1]) 
        theGrab = cmd.parentConstraint( objectsSelected[0], DaParentLocator, n=DaGrabber, mo=True)[0]
        currentFrame = cmd.currentTime(query=True)
        previousFrame = currentFrame - 1
        #key the locator to display Grabber0
        cmd.setKeyframe(DaParentLocator,time=currentFrame)
        cmd.setKeyframe(DaParentLocator,time=previousFrame)
        cmd.setKeyframe(objectsSelected[1],time=currentFrame)
        temp=cmd.listAttr(DaParentLocator,keyable=True)[-1]
    
        if not temp==DaGrabber :
            newAttr=cmd.renameAttr(DaParentLocator+'.'+temp,DaGrabber)
            cmd.setKeyframe(DaParentLocator,at=newAttr, value =0,time=previousFrame)
            cmd.setKeyframe(DaParentLocator,at=newAttr, value =1,time=currentFrame)
    
    def releaseGrab(self):
        theSelection = (cmd.ls(selection = True, shortNames=True))
        theGrabTransform = cmd.listRelatives(theSelection, parent=True)
        if len(theSelection) != 1 :
            cmd.error (" please select exactly 1 grabbed object")
        else :
            if str(theGrabTransform[0]).split('_')[0] == 'prGrabLocator': 
                theGrabTransform = cmd.listRelatives(theSelection, parent=True)
                constraintAttr = cmd.listAttr(theGrabTransform,keyable=True)[-1]
                currentFrame = cmd.currentTime(query=True)
                nextFrame = currentFrame + 1
                cmd.setKeyframe(theGrabTransform,time=currentFrame)
                cmd.setKeyframe(theGrabTransform,at=constraintAttr, value =1,time=currentFrame)    
                cmd.setKeyframe(theGrabTransform,time=nextFrame)
                cmd.setKeyframe(theGrabTransform,at=constraintAttr, value =0,time=nextFrame)
                cmd.setKeyframe(theSelection,time=currentFrame)
            else:
                cmd.error("Please select a previously Grabbed object")
            
	def bakeAttrAndTrf(obj,Attr):
		
    
    def makingParentLocator(self,thechildobject): 
        #global DaLocator # an addition to test out   
        #global CurrentSelection
        #Step 1 make a locator that is in the exact location as the Target.
        try:
            selection = thechildobject #cmd.ls(selection=True)[0]
        except:
            cmd.confirmDialog(title='Error dialog', message='Please Select a Target', messageAlign='left',
                button='Ok', defaultButton='Ok', dismissString='Ok', icon='warning')
        #print selection
        else:
            #query selction's loction in worldspace
            worldTrans = cmd.xform(selection, worldSpace=True, query=True,translation=True)
            worldRot = cmd.xform(selection, worldSpace=True, query=True,rotation=True)
                
            #create locator in some position
            counter = cmd.ls('prGrabLocator*',type='locator')#lists number of locators named prGrabLocator
            theLocator = cmd.spaceLocator(n='prGrabLocator_'+str(len(counter)))[0]
            #print theLocator
            cmd.setAttr(theLocator+'.translate',worldTrans[0],worldTrans[1],worldTrans[2],type = 'double3')
            cmd.setAttr(theLocator+'.rotate',worldRot[0],worldRot[1],worldRot[2],type = 'double3')
            cmd.parent(selection, theLocator)
            return theLocator

x=Fixit()
x.checkLocators()
x.uiMain() 
