#Autor - Irakli Kublashvili 2013

import maya.cmds as cmds
import maya.mel  as mel
import sys
import os
import shutil as shutil
from functools import partial
import platform
import ctypes
import re
import distutils.core



class IkRenderViewBatchRenderer:
    
    def __init__(self):
        
        self.disconnectAll_renderPasses('__init__')
   
    
    def disconnectAll_renderPasses(self, id):
       
        allRenderPasses = self.getAllCamerasLayersPasses()[2]
        allRenderLayers = self.getAllCamerasLayersPasses()[1]
        
        if allRenderLayers != None:
            for renderLayer in allRenderLayers:
                connectedRenderPass = cmds.listConnections(renderLayer+".renderPass")
                if connectedRenderPass != None:
                    for renderPass in connectedRenderPass:
                        cmds.disconnectAttr((renderLayer+".renderPass") ,(renderPass+".owner"), nextAvailable=True )
        if id == '__init__':     
            sys.stderr.write("<<RVBR: All Render Passes Disconnected>>\n")
        elif id == 'resetAll':
            sys.stderr.write("<<RVBR: All Settings Are Reset>>\n")

    
    def saveRenderSettings(self,*args):

        selectedCamera = self.getSelectedItemsFromList()[0]
        selectedRenderLayers = self.getSelectedItemsFromList()[1]
        selectedRenderPasses = self.getSelectedItemsFromList()[2]

        self.connectRenderPasses( selectedRenderLayers, selectedRenderPasses)
        
        saveSettingsButton = cmds.button(self.apllySettingsBtn, query=True, label=True)
        #cmds.button(self.apllySettingsBtn, edit=True, label="Save Settings")
        cmds.button(self.resetAllBtn, edit=True, enable=True)

        selectedRenderLayers = []
        selectedRenderPasses = []
        
        destinationDyrectory = cmds.textFieldButtonGrp(self.getDestinationDirectoryField, query=True, text=True)
        imageName = cmds.textField(self.outputfileName, query=True, text=True)
        customWidth = cmds.intField(self.customWidth, query=True, value=True)
        customHeight = cmds.intField(self.customHeight, query=True, value=True)
        imageSizePreset = cmds.optionMenuGrp(self.imageResolutionOptionMenu, query=True, value=True)
        imageFormat = cmds.optionMenuGrp(self.imageFormats, query=True, value=True)
        framePadding = cmds.intSliderGrp(self.faramePadding, query=True, value=True)
        selectedCamera = cmds.textScrollList(self.cameraSettingsTextScroll, query=True, selectItem=True)
        startFrame = cmds.floatField(self.cameraSettingsStartFrameValue, query=True, value=True)
        endFrame = cmds.floatField(self.cameraSettingsEndFrameValue, query=True, value=True)
        selectedLayers = cmds.textScrollList(self.layersTextsScroll, query=True, selectItem=True)
        getSelectedRenderPasses = cmds.textScrollList(self.cameraSettingsPassesTextScroll, query=True, selectItem=True)
        
        ## Add renderLayers to camera
        selectedRenderPasses_Attr = ""
        startEndFrames = (str(startFrame)+", " +str(endFrame)+";")
        
        if startFrame > endFrame :
            cmds.warning( "<<RVBR: Frame range is incorrect>>\n")#sys.stderr.write("<<Warning: Frame range is incorrect>>\n")
            cmds.button(self.renderButton,edit=True, enable=False)        
        elif not destinationDyrectory :
            cmds.warning( "<<RVBR: No destination path found to proceed>>\n")#sys.stderr.write("<<Warning: No destination path or output file name found to proceed>>\n")
        elif not imageName:
            cmds.warning( "<<RVBR: No output file name found to proceed>>\n")
        else:
            cmds.button(self.renderButton, edit=True, enable=True)
            masterLayer = "masterLayer"
           
            if getSelectedRenderPasses != None:
                for rpass in getSelectedRenderPasses:
                    selectedRenderPasses_Attr += (rpass+", ")

            if saveSettingsButton == "Save Settings":                
                for selectedLayer in selectedLayers:
                    if selectedLayer == "defaultRenderLayer":
                        selectedLayer = masterLayer
                           
                    cmds.addAttr(selectedCamera[0], longName=selectedLayer, dataType = "string")
                    cmds.setAttr((selectedCamera[0]+"."+selectedLayer),(selectedRenderPasses_Attr+";" + startEndFrames), type="string", channelBox=False )
                    cmds.setAttr((selectedCamera[0]+"."+selectedLayer), keyable=False, lock=True)
                    cmds.button(self.apllySettingsBtn, edit=True, label="Edit")
            
            ## Edit Attribute list
            if saveSettingsButton == "Edit":
                listAttributes = cmds.listAttr(selectedCamera[0], locked=True)
                for selectedLayer in selectedLayers:
                    if selectedLayer == "defaultRenderLayer":
                        selectedLayer = masterLayer 
                    if selectedLayer in listAttributes:
                        cmds.setAttr((selectedCamera[0]+"."+selectedLayer), keyable=False, lock=False)
                        cmds.setAttr((selectedCamera[0]+"."+selectedLayer),(selectedRenderPasses_Attr +";" +startEndFrames), type="string", channelBox=False )
                        cmds.setAttr((selectedCamera[0]+"."+selectedLayer), keyable=False, lock=True)
                    else:                        
                        cmds.addAttr(selectedCamera[0], longName=selectedLayer, dataType = "string")
                        cmds.setAttr((selectedCamera[0]+"."+selectedLayer),(selectedRenderPasses_Attr +";" +startEndFrames), type="string", channelBox=False )
                        cmds.setAttr((selectedCamera[0]+"."+selectedLayer), keyable=False, lock=True)     

            self.numebrOfSelectePasses = cmds.textScrollList(self.cameraSettingsPassesTextScroll, query=True, numberOfSelectedItems=True)

            if not getSelectedRenderPasses == None:
                for singlePass in getSelectedRenderPasses:
                    selectedRenderPasses.append(singlePass)
            
            getSelectedRenderLayerNames = cmds.textScrollList(self.layersTextsScroll, query=True, selectItem=True)
           
            for renderLayer in getSelectedRenderLayerNames:                                                            
                      selectedRenderLayers.append(renderLayer)
         
            #block layer settings layout 
            self.layerSettingsScrollEnableDisable("Save")
       
            cmds.button(self.renderButton,edit=True, enable=True)
        
        self.infoPannel("cameras")
   

    def doRender(self, *args):
       
        cmds.RenderViewWindow()
        cmds.showWindow("renderViewWindow")
       
        cmds.setAttr("defaultRenderGlobals.animation", 0)
        cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
        
        
        outputfileName = cmds.textField(self.outputfileName, query=True, text=True)
        destinationDirectory = cmds.textFieldButtonGrp(self.getDestinationDirectoryField, query=True, text=True)
        framePadding = cmds.intSliderGrp(self.faramePadding, query=True, value=True)
        tempImageFolder = self.getProjectPaths()
        renderableCameras = []

        selectedRenderLayers = self.getSelectedItemsFromList()[1]
        allCameras = self.getAllCamerasLayersPasses()[0]
        allRenderLayers = self.getAllCamerasLayersPasses()[1]
        allRenderPasses = self.getAllCamerasLayersPasses()[2]
        
        self.cleanUpImagesDirectory()
        self.createTempFolderAndMakeItHidden(tempImageFolder)
   
        currendetRenderer = cmds.getAttr("defaultRenderGlobals.currentRenderer")
        
        sys.stderr.write("<<RVBR: Rendering using "+ currendetRenderer+">>\n")
        
        # If render passes for Maya Software renderer are checked disable them and inform user about
        for layer in allRenderLayers:
            shadow = cmds.getAttr(layer+'.shadow')
            specular = cmds.getAttr(layer+'.specular')
            color = cmds.getAttr(layer+'.color')
            diffuse = cmds.getAttr(layer+'.diffuse')
            
            if shadow == 1 or specular == 1 or color == 1 or diffuse == 1:
                cmds.setAttr(layer+'.shadow', 0)
                cmds.setAttr(layer+'.color', 0)
                cmds.setAttr(layer+'.specular', 0)
                cmds.setAttr(layer+'.diffuse', 0)  
                cmds.warning( "RVBR: Render Passes for Maya Software Renderer are no longer supported. Disabling...\n")#sys.stderr.write("<<Warnig: Render Passes for Maya Software Renderer are no longer supported. Disabling...>>\n")
            
        
        if allCameras != None:
            for camera in allCameras:
                listAttributes = cmds.listAttr(camera, locked=True)
                if allRenderLayers != None:
                    for renderLayer in allRenderLayers:
                        if listAttributes != None:
                            if renderLayer == 'defaultRenderLayer':
                                renderLayer = "masterLayer"
                            if renderLayer in listAttributes:
                                renderableCameras.append(camera)
                           
        renderableCameras = sorted(set(renderableCameras))
        
        if renderableCameras != None:
            
            for camera in renderableCameras:
                renderLayersForRender = []
                listAttributes = cmds.listAttr(camera, locked=True)
                if allRenderLayers != None:
                        for renderLayer in allRenderLayers:
                            if renderLayer == 'defaultRenderLayer':
                                renderLayer = 'masterLayer'
                            if listAttributes != None:
                                if renderLayer in listAttributes:
                                    renderLayersForRender.append(renderLayer)
                 
                for renderLayer in renderLayersForRender:
                    
                    attributeSctring = cmds.getAttr(camera+'.'+renderLayer)
                    renderPasses =  attributeSctring.partition(';')[0]

                    startFrame = []
                    endFrame = []
                    attrString = cmds.getAttr(camera+'.'+renderLayer)
                    startEndFrames = attrString.partition(';')[2]
                    startFrame = startEndFrames.split(',')[0]
                    endFrame_temp = startEndFrames.split(',')[1]
                    endFrame = endFrame_temp.partition(';')[0]
                    
                    startFrame = float(startFrame)
                    endFrame = float(endFrame)
                    cmds.progressWindow(minValue=startFrame, maxValue=endFrame,	title='Rendering Process...', progress=0, status= 'Render Frame: 0',isInterruptable=True )
                    
                    if not  startFrame >= endFrame :                        
                        currentFrame = startFrame
                        timeSliderRange = endFrame
                        
                        cmds.playbackOptions(min = currentFrame, max=timeSliderRange)
                        ###################################################################### Here if renderLayer's name is masterLayer change it to defaultRenderLayer. Because It's just a nmae of attr
                        if renderLayer == 'masterLayer':                             
                                renderLayer = 'defaultRenderLayer'
                        cmds.editRenderLayerGlobals(currentRenderLayer= renderLayer)  
                        if renderLayer == 'defaultRenderLayer':
                                renderLayer = 'masterLayer'
                        ############################################################################ Then change it again

                        while currentFrame<=timeSliderRange:
                            
                            if cmds.progressWindow( query=True, isCancelled=True ):
                                break                     
   
                            mel.eval('renderWindowRenderCamera( "render", "renderView" , '+ '"' + camera + '"' + ')')
                            cmds.currentTime(currentFrame)

                            framePaddingNumber_temp = self.framePaddingNum (currentFrame, framePadding  )
                            
                            if framePaddingNumber_temp != None:
                                framePaddingNumber = framePaddingNumber_temp
                            else:
                                framePaddingNumber = ""    

                            # Check if destination directory is setted
                            if not destinationDirectory:
                                sys.stderr.write("<<RVBR: No destination path found to proceed>>\n")                            
                            else:                                     
                                destinationDirectory_temp = (destinationDirectory + '/'+renderLayer)
                                if os.path.exists(destinationDirectory_temp):
                                    pass
                                else:
                                    os.makedirs(destinationDirectory_temp)    
                                
                                #Check if folder contains rendered images
                                fileFormatDictionary = {"Alias PIX (als)":"als", "AVI (avi)":"avi", "Cineon (cin)":"cin", "DDS (dds)":"dds",
                                                    "EPS (eps)":"eps", "GIF (gif)":"gif", "JPEG (jpg)":"jpg", "Maya IFF (iff)":"iff", 
                                                    "Maya16 IFF (iff)":"iff", "PSD (psd)":"psd", "PSD Layered (psd)":"psd", 
                                                    "PNG (png)":"png", "Quantel (yuv)":"yuv", "RLA (rla)":"rla", "SGI (sgi)":"sgi",
                                                    "SGI16 (sgi)":"sgi", "Softimage (pic)":"pic", "Targa (tga)":"tga", 
                                                    "Tiff (tif)":"tif", "Tiff16 (tif)":"tif", "Windows Bitmap (bmp)":"bmp", "OpenEXR (exr)":"exr", "HDR (hdr)":"hdr"}
                                
                                #Creats a dictionary for file formats. Each format use it's own number and keys are values from optionMenuGrp 
                                rendererVersion = self.detectRendererVersion()
        
                                if rendererVersion == "mentalRay":
            
                                    fileFormatDictionary =  {"Alias PIX (als)":"als", "AVI (avi)":"avi", "Cineon (cin)":"cin", "DDS (dds)":"dds",
                                                    "EPS (eps)":"eps", "GIF (gif)":"gif", "JPEG (jpg)":"jpg", "Maya IFF (iff)":"iff", 
                                                    "Maya16 IFF (iff)":"iff", "PSD (psd)":"psd", "PSD Layered (psd)":"psd", 
                                                    "PNG (png)":"png", "Quantel (yuv)":"yuv", "RLA (rla)":"rla", "SGI (rgb)":"rgb",
                                                    "SGI16 (sgi)":"sgi", "Softimage (pic)":"pic", "Targa (tga)":"tga", 
                                                    "Tiff (tif)":"tif", "Tiff16 (tif)":"tif", "Windows Bitmap (bmp)":"bmp", "OpenEXR (exr)":"exr", "HDR (hdr)":"hdr"}
                                
                                
                                imageFormat = cmds.optionMenuGrp(self.imageFormats, query=True, value=True)
                                
                                if renderLayer == "masterLayer" and len(renderLayersForRender) == 1:
                                    fileNames = os.listdir(tempImageFolder)
                                else:    
                                    fileNames = os.listdir(tempImageFolder+"/"+renderLayer)
                                
                                renderedImage = []
                                
                                for file in fileNames:
                                                                      
                                    tempFile = file.partition(".")
                                    # If file in directory have extension and it have a similar extension as indicated in optionMenuGrp then proceed
                                    if tempFile[2] and tempFile[2] == fileFormatDictionary[imageFormat]:
                                        
                                        if outputfileName: #If outputFileName exists then rename it and add it to renderedImage variable
                                            tempImageAndPath = tempImageFolder + renderLayer + "/" + file                                           
                                            outputImageName  = tempImageFolder + renderLayer + "/" + outputfileName + "_" + camera+ "_" + str(framePaddingNumber) + str(int(currentFrame)) + "."  + fileFormatDictionary[imageFormat]                                            
                                            
                                            if len(renderLayersForRender) == 1 and renderLayer == 'masterLayer':
                                                outputImageName = tempImageFolder  + "/" + outputfileName + "_" + camera+ "_" + str(framePaddingNumber) + str(int(currentFrame)) + "."  + fileFormatDictionary[imageFormat]
                                                tempImageAndPath = tempImageFolder  + "/" + file
                                            
                                            
                                            os.rename(tempImageAndPath, outputImageName )
                                            renderedImage = outputImageName
                                            
                                            # Check if rendered image exists
                                            if len(renderedImage) == 0 : 
                                                sys.stderr.write("<<RVBR: No render images to proceed>>\n")                                            
                                            else:
                                                fullFilePathAndName = renderedImage    
                                                
                                                shutil.copy(fullFilePathAndName, destinationDirectory_temp)  # Copy file to destination folder
                                                
                                                os.remove(fullFilePathAndName) # Remove image from temp directory
                                            
   
                                        else:
                                            
                                            sys.stderr.write("<<RVBR: Please, enter output image name>>\n")
                                    
                                    ############################ If RenderPasses is used and format is not *exr ) #################################################
                                    elif renderPasses != '' and  imageFormat != "OpenEXR (exr)":
                                                                                   
                                        renderLayerDir = tempImageFolder + renderLayer 
                                        
                                        # If only defaultRenderLayer is in render layers list
                                        if len(selectedRenderLayers) == 1 and selectedRenderLayers[0] == 'defaultRenderLayer':
                                            tempRenderPassFile = os.listdir(tempImageFolder + '/' +file)
                                            tempRenderPassFullName = tempImageFolder + '/' + file  + '/' + tempRenderPassFile[0]                                
                                            renderPassImageFullName = tempImageFolder + '/'+ file + '/' + outputfileName +"_" +file + "_" + camera+ "_" + str(framePaddingNumber) + str(int(currentFrame)) + "."  + fileFormatDictionary[imageFormat] 
                                        else:
                                            tempRenderPassFile = os.listdir(renderLayerDir + '/' +file)
                                            tempRenderPassFullName = renderLayerDir + '/' + file  + '/' + tempRenderPassFile[0]                                
                                            renderPassImageFullName = renderLayerDir + '/'+ file + '/' + outputfileName +"_" +file + "_" + camera+ "_" + str(framePaddingNumber) + str(int(currentFrame)) + "."  + fileFormatDictionary[imageFormat] 

                                        
                                        renderLayerDir = renderLayerDir.replace('\\', '/')
                                        
                                        # Check if destination directory is setted
                                        if not destinationDirectory:
                                            sys.stderr.write("<<RVBR: No destination path found to proceed>>\n")                                        
                                        else:                                                 
                                            destinationDirectory_temp = (destinationDirectory + '/' +renderLayer + '/' + file)
                                            if os.path.exists(destinationDirectory_temp):
                                                pass
                                            else:
                                                os.makedirs(destinationDirectory_temp) 

                                        # Rename and copy image, then delete it
                                        os.rename(tempRenderPassFullName, renderPassImageFullName)
                                        destRenderPassImageFullName = destinationDirectory +'/'+ renderLayer + '/' + file +'/'+ outputfileName +"_" +file + "_" + camera+ "_" + str(framePaddingNumber) + str(int(currentFrame)) + "."  + fileFormatDictionary[imageFormat] 
                                        
                                        shutil.copy(os.path.normpath(renderPassImageFullName), os.path.normpath(destRenderPassImageFullName))
                                        os.remove(renderPassImageFullName)
                                        
                                        

                            cmds.progressWindow( edit=True, progress=currentFrame, status=( camera +': '+ renderLayer +': '+ ' Rendering Frame: ' + `int(currentFrame)` ) )
                            cmds.pause( seconds=1 )             
                            
                            currentFrame = currentFrame + 1
        shutil.rmtree(tempImageFolder)                                

        cmds.progressWindow(endProgress=1)   
        sys.stderr.write("<<RVBR: Rendering Complete>>\n")
    
    def createTempFolderAndMakeItHidden(self, tempImageFolder):
        
        platform = self.detectPlatform
        
        os.makedirs(tempImageFolder)
        
        platform = self.detectPlatform()
        
        #Add hidden attribute
        if platform == "Windows":
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(unicode(tempImageFolder), FILE_ATTRIBUTE_HIDDEN)
        
        
        elif platform == "OSX":
            
            tempImageFolder = tempImageFolder.rpartition('/')
            os.system('chflags hidden'+ ' '+ tempImageFolder[0] ) 
        
                        
    def connectRenderPasses(self, selectedRenderLayers, renderPasses):

            renderLayers = selectedRenderLayers
            renderPasses = renderPasses
            self.disConnectRenderPassForSelectedLayers(renderLayers,renderPasses )
            
            if renderLayers:
                counter = len(renderLayers)
            
                for renderLayer in renderLayers:
                    connectedRenderPass = cmds.listConnections((renderLayer+".renderPass"), exactType=True)
                    
                    if connectedRenderPass == None:
                        if renderPasses != None:
                            for renderPass in renderPasses:
                                ownerAttrList = cmds.listAttr(renderPass+'.owner', multi=True)
                                if ownerAttrList:
                                    for ownerAttr in ownerAttrList:
                                        index = ownerAttr.rpartition('r')[2]
                                        if index:
                                            index = str(index).translate(None,'[]')
                                            if index >= counter:
                                                counter +=1
                                cmds.connectAttr((renderLayer+".renderPass"),(renderPass+".owner"+"["+str(counter)+"]" ), force=True)
                    counter += 1
    
    
    def disConnectRenderPassForSelectedLayers(self, selectedRenderLayers, selectedRenderPasses):

        for renderLayer in selectedRenderLayers:
            connectedRenderPasses = cmds.listConnections((renderLayer+'.renderPass'), exactType=True)
            if connectedRenderPasses:
                for rendePass in connectedRenderPasses:
                    connectedRenderPass = cmds.listConnections((renderLayer+'.renderPass'), exactType=True)
                    if connectedRenderPass:
                        cmds.disconnectAttr((renderLayer+'.renderPass'), (rendePass+".owner"),nextAvailable=True ) 
                      
    
    def disConnectRenderPasses(self):
        
        selectedRenderLayers = self.getSelectedItemsFromList()[1]
        selectedRenderPasses = self.getSelectedItemsFromList()[2]
        
        renderLayers = []
        
        if selectedRenderLayers:
            if selectedRenderLayers == "ClearAll" and selectedRenderPasses == None: # If pressed "Rset All" button or "Save Settings" button without selecting any render passes then list all layers for disconnect.
                renderLayers = cmds.ls(exactType ="renderLayer")
            else:
                renderLayers = selectedRenderLayers # If presses "Save Setting" button with some render passes selected 
            
                
            for renderLayer in renderLayers:
                connectedRenderPasses = cmds.listConnections((renderLayer+".renderPass"), exactType=True) 
                if not connectedRenderPasses == None:
                    for renderPass in connectedRenderPasses:
                        cmds.disconnectAttr((renderLayer+".renderPass"),(renderPass+".owner"), nextAvailable=True)
    
    
    def disconnectSelectedRenderPass(self, id, *args):
        
        if id == "deselect":
            cmds.textScrollList(self.cameraSettingsPassesTextScroll, edit=True, deselectAll=True)
            cmds.button(self.deselectRPassesBtn, edit=True, enable=False)
        # Create/Remove Button callback
        cmds.button(self.createRemoveRenderPassesBtn, edit=True, label="Create", command=self.createRenderPasses)
        cmds.popupMenu(self.renderPassesPopupMenu, edit=True, button=1, deleteAllItems=False) 
        
        
        self.renderPassMenuItemIteration("secondary_call")  
    
    
    def removeRenderPass(self, selectedRenderPass,  *args):

        currentRenderPass = selectedRenderPass

        cmds.delete(selectedRenderPass)
        self.refreshRenderPasses()
        
        cmds.button(self.createRemoveRenderPassesBtn, edit=True, label="Create", command=self.createRenderPasses)
        cmds.popupMenu(self.renderPassesPopupMenu, edit=True, button=1, deleteAllItems=False) 
        
        
        self.renderPassMenuItemIteration("secondary_call")  


    def getRenderPasses(self):

        currentRenderLayer = self.getRenderLayers()[1] # get current renderLayer
        renderPasses = cmds.ls(exactType ="renderPass")
        
        connectedRenderPasses = []
        
        if renderPasses:
            connectedRenderPasses = cmds.listConnections((currentRenderLayer+".renderPass"), exactType=True)
        
        
        return [renderPasses, connectedRenderPasses] 
    
    
    def createRenderPasses(self, renderPassesDictionary , *args):
        
        operatingSystem = self.detectPlatform()
        presetsPath = ""
        vNum = cmds.about(version=True) #get version of Maya
        
        if operatingSystem == "Windows":
            if vNum == '2013 x64':
                vNum = '2013'
            if vNum == '2012 x64':
                vNum = '2012'    
            presetsPath = 'C:/Program Files/Autodesk/Maya'+vNum+'/presets/attrPresets/renderPass/'
        elif operatingSystem == "OSX":
            if vNum == '2014 x64':
                vNum = '2014'
            if vNum == '2013 x64':
                vNum = '2013'
            if vNum == '2012 x64':
                vNum = '2012'                   
            presetsPath =  '/Applications/Autodesk/maya'+vNum+'/Maya.app/Contents/presets/attrPresets/renderPass/'   
        else:
            sys.stderr.write("<<RVBR: Unsupported Operating System>>\n")
        
        key = renderPassesDictionary
        
        renderPassesNameDictionary = {"Blank":"Blank", "2D Motion Vector":"mv2DToxik", "3D Motion Vector":"mv3D", "Ambient Irradience":"ambientIrradiance", "Ambient Material Color":"ambientRaw", "Ambient Occlusion": "AO",
                                    "Ambient":"ambient", "Beauty Without Reflections and Refractions":"beautyNoReflectRefract", "Beauty":"beauty","Camera Depth Remaped": "depthRemapped", "Camera Depth":"depth", 
                                    "Coverage":"coverage","Custom Color":"customColor", "Custom Depth":"customDepth", "Custom Label":"customLabel", "Custom Vector":"customVector", "Diffuse Material Color":"diffuseMaterialColor",
                                    "Diffuse Without Shadows":"diffuseNoShadow","Diffuse":"diffuse", "Direct Irradiance Without Shadows":"directIrradianceNoShadow", "Direct Irradiance":"directIrradiance", 
                                    "Glow Source":"glowSource", "Incandescence":"incandescence", "Incidence (Light/Normal)":"incidenceLN","Indirect":"indirect", "Light Volume":"volumeLight",  
                                    "Material Incidence (Camera/Normal)":"incidenceCNMat", "Material Normal (Camera spae)":"normalCamMaterial", "Material Normal (Object space)":"normalObjMaterial","Material Normal (World space)":"normalWorldMaterial",
                                    "Matte":"matte","Normalized 2D Motion Vector":"mv2DNormRemap", "Object Incidence (Camera/Norma)":"incidenceCN", "Object Normal (Camera space)":"normalCam","Object Normal (Object space)":"normalObj",
                                    "Object Normal (World space)": "normalWorld", "Object Volume":"volumeObject", "Opacity":"opacity","Raw Shadow":"shadowRaw", "Reflected Material Color":"reflectedMaterialColor",
                                    "Reflection":"reflection","Refraction Material Color":"refractionMaterialColor", "Refraction":"refraction", "Scatter":"scatter", "Scene Volume":"volumeScene", "Shadow":"shadow", 
                                    "Specular Without Shadows":"specularNoShadow", "Specular":"specular","Translucence Without Shadows":"translucenceNoShadow", "Translucence":"translucence", "UVPass":"UVPass", 
                                    "World Position":"worldPosition"}
       
        renderPassesTypeDictionary = {"Blank":"blank.mel", "2D Motion Vector": "2DMotionVector.mel", "3D Motion Vector":"3DMotionVector.mel", "Ambient Irradience":"ambientIrradiance.mel", "Ambient Material Color":"ambientMaterialColor.mel", 
                                      "Ambient Occlusion": "ambientOcclusion.mel","Ambient":"ambient.mel", "Beauty Without Reflections and Refractions":"beautyWithoutReflectionsRefractions.mel", "Beauty":"beauty.mel",
                                      "Camera Depth Remaped": "cameraDepthRemapped.mel", "Camera Depth":"cameraDepth.mel", "Coverage":"coverage.mel","Custom Color":"customColor.mel", "Custom Depth":"customDepth.mel", 
                                      "Custom Label":"customLabel.mel", "Custom Vector":"customVector.mel", "Diffuse Material Color":"diffuseMaterialColor.mel",  "Diffuse Without Shadows":"diffuseWithoutShadows.mel",
                                      "Diffuse":"diffuse.mel", "Direct Irradiance Without Shadows":"directIrradianceWithoutShadows.mel", "Direct Irradiance":"directIrradiance.mel", "Glow Source":"glowSource.mel", 
                                      "Incandescence":"incandescence.mel", "Incidence (Light/Normal)":"incidenceLightNorm.mel","Indirect":"indirect.mel", "Light Volume":"lightVolume.mel",
                                      "Material Incidence (Camera/Normal)":"incidenceCamNormMaterial.mel", "Material Normal (Camera spae)":"normalCamMaterial.mel", "Material Normal (Object space)":"normalObjMaterial.mel",
                                      "Material Normal (World space)":"normalWorldMaterial.mel","Matte":"matte.mel","Normalized 2D Motion Vector":"normalized2DMotionVector.mel", "Object Incidence (Camera/Norma)":"incidenceCamNorm.mel", 
                                      "Object Normal (Camera space)":"normalCamMaterial.mel","Object Normal (Object space)":"normalObjMaterial.mel","Object Normal (World space)": "normalWorldMaterial.mel", 
                                      "Object Volume":"objectVolume.mel", "Opacity":"opacity.mel","Raw Shadow":"rawShadow.mel", "Reflected Material Color":"reflectedMaterialColor.mel","Reflection":"reflection.mel",
                                      "Refraction Material Color":"refractionMaterialColor.mel", "Refraction":"refraction.mel", "Scatter":"scatter.mel", "Scene Volume":"sceneVolume.me", "Shadow":"shadow.mel", 
                                      "Specular Without Shadows":"specularWithoutShadows.mel", "Specular":"specular.mel","Translucence Without Shadows":"translucenceWithoutShadows.mel", "Translucence":"translucence.mel", "UVPass":"UV.mel", 
                                      "World Position":"worldPosition.mel"}
       

        rawRenderPass = cmds.shadingNode( "renderPass", asRendering=True)
        mel.eval('applyAttrPreset '+ '"'+rawRenderPass+ '"' + ' "'+ (presetsPath + renderPassesTypeDictionary[key])+'"'+ " 1;" )
        cmds.rename(rawRenderPass,renderPassesNameDictionary[key] )
                                                
        self.refreshRenderPasses()
        
        cmds.select(clear=True)


    def refreshRenderPasses(self ,*args):

        renderPasses = self.getRenderPasses()
        
        cmds.textScrollList(self.cameraSettingsPassesTextScroll, edit=True, removeAll=True)
        cmds.textScrollList(self.cameraSettingsPassesTextScroll, edit=True, append=renderPasses[0])


    def getProjectPaths(self):
        
        # Get temporal directory of rendered image. 
        currentProject = cmds.workspace(fullName=True)
        imagesDirectory = cmds.workspace('images', query=True, fileRuleEntry=True)
        
        # If realtive path
        if imagesDirectory == "images":
            tempImageFolder = currentProject + "/"+ imagesDirectory + "/tmp/"
        
        # If absolute path
        else:
           tempImageFolder = cmds.workspace('images', query=True, fileRuleEntry=True)+"/tmp/"
        
        
        return  tempImageFolder   
        
    
    #Get path for save output files
    def getPath(self, *args):
        
        directoryPath = cmds.fileDialog2(fileMode=3)
        cmds.textFieldButtonGrp(self.getDestinationDirectoryField, edit=True, text=directoryPath[0], editable=False)
        
        
    def closeMainWindow(self,mainWindow,*args):
        
        cmds.deleteUI(mainWindow)
        
    
    # resolution function
    def imageResolution(self, *args):
        
        customResolution = cmds.checkBox(self.activateCustomResolutionCheckBox, query=True, value=True)
        customResolutionWidth = cmds.intField(self.customWidth, query=True, value=True)
        customResolutionHeight = cmds.intField(self.customHeight, query=True, value=True)
        imageResolutionPreset = cmds.optionMenuGrp(self.imageResolutionOptionMenu, query=True, value=True)
        
        
        
        imageResoutionDictionary = {"320x240": [320,240,1.333,1.000],"640x480":[640,480,1.333,1.000], "1k Square":[1024,1024,1.000,1.000], "2k Square":[2048,2048,1.000,1.000],
                                    "3k Square":[3072, 3072,1.000,1.000],"4k Square":[4096,4096,1.000,1.000],"CCIR PAL/Quantel PAL":[720, 576, 1.333,1.066],
                                    "CCIR 601/Quantel NTSC":[720,486,1.333,0.900], "Full 1024":[1024,768,1.333,1.000],"Full 1280/Screen":[1280,1024,1.333,1.066],
                                    "HD 540":[960,540,1.777,1.000], "HD 720":[1280,720,1.777,1.000],"HD 1080":[1920,1080,1.777,1.000], "NTCS 4D":[646,485,1.333,1.001],
                                    "PAL 768":[768,576,1.333,1.001],"PAL 780":[780,576,1.333,0.984] }
        
        
        
        if customResolution:
            cmds.setAttr("defaultResolution.width", customResolutionWidth)
            cmds.setAttr("defaultResolution.height", customResolutionHeight)
            cmds.setAttr("defaultResolution.deviceAspectRatio", imageResoutionDictionary[imageResolutionPreset][2])
            cmds.setAttr("defaultResolution.pixelAspect", imageResoutionDictionary[imageResolutionPreset][3])   
        
        else:
            cmds.setAttr("defaultResolution.width", imageResoutionDictionary[imageResolutionPreset][0])
            cmds.setAttr("defaultResolution.height", imageResoutionDictionary[imageResolutionPreset][1])
            cmds.setAttr("defaultResolution.deviceAspectRatio", imageResoutionDictionary[imageResolutionPreset][2])
            cmds.setAttr("defaultResolution.pixelAspect", imageResoutionDictionary[imageResolutionPreset][3])   
        
        
    # File format functin
    def renderImageFormats(self,value, *args):
        
        #Creats a dictionary for file formats. Each format use it's own number and keys are values from optionMenuGrp 
        fileFormatDictionary = {"Alias PIX (als)":6, "Cineon (cin)":11, "DDS (dds)":35,
                                "EPS (eps)":9, "GIF (gif)":0, "JPEG (jpg)":8, "Maya IFF (iff)":7, 
                                "Maya16 IFF (iff)":10, "PSD (psd)":31, "PSD Layered (psd)":36, 
                                "PNG (png)":32, "Quantel (yuv)":12, "RLA (rla)":2, "SGI (sgi)":5,
                                "SGI16 (sgi)":13, "Softimage (pic)":1, "Targa (tga)":19, 
                                "Tiff (tif)":3, "Tiff16 (tif)":4, "Windows Bitmap (bmp)":20, "HDR (hdr)":100, "OpenEXR (exr)":101}
        
        
        #Creats a dictionary for file formats. Each format use it's own number and keys are values from optionMenuGrp 
        rendererVersion = self.detectRendererVersion()
        
        if rendererVersion == "mentalRay":
            
            fileFormatDictionary = {"Alias PIX (als)":6, "Cineon (cin)":11, "DDS (dds)":35,
                                    "EPS (eps)":9, "GIF (gif)":0, "JPEG (jpg)":8, "Maya IFF (iff)":7, 
                                    "Maya16 IFF (iff)":10, "PSD (psd)":31, "PSD Layered (psd)":36, 
                                    "PNG (png)":32, "Quantel (yuv)":12, "RLA (rla)":2, "SGI (rgb)":5,
                                    "SGI16 (sgi)":13, "Softimage (pic)":1, "Targa (tga)":19, 
                                    "Tiff (tif)":3, "Tiff16 (tif)":4, "Windows Bitmap (bmp)":20, "HDR (hdr)":100, "OpenEXR (exr)":101}
        
        # For EXR and HDR extension we use this code:
        if value == "HDR (hdr)":
            cmds.setAttr("defaultRenderGlobals.imageFormat", 51)
            cmds.setAttr("defaultRenderGlobals.imfPluginKey","hdr", type="string")
        elif value == "OpenEXR (exr)":
            cmds.setAttr("defaultRenderGlobals.imageFormat", 51)
            cmds.setAttr("defaultRenderGlobals.imfPluginKey","exr", type="string")
        else:
            cmds.setAttr("defaultRenderGlobals.imageFormat", fileFormatDictionary[value])        
    
    
    #Frame padding 
    def framePaddingFunction(self,value, *args):
        
        cmds.setAttr("defaultRenderGlobals.extensionPadding", value)                         

    
    def framePaddingNum(self, currentFrame, framePadding):
        
        framePaddingNumber = []
        framePaddingDictinary = { 10:"000000000", 9:"00000000",8:"0000000",7:"000000",
                                 6:"00000", 5:"0000", 4:"000", 3:"00", 2:"0", 1:""}
        
        
        if framePadding == 1:
            framePaddingNumber = framePaddingDictinary[1]
        
        if framePadding == 2:
             if currentFrame >= 0 and currentFrame <10:
                 framePaddingNumber = framePaddingDictinary[2]
             else:
                 framePaddingNumber = framePaddingDictinary[1]
        
        if  framePadding == 3:     
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[2]
            else:
                framePaddingNumber = framePaddingDictinary[1]        
        
        if framePadding == 4:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[2]
            else:
                framePaddingNumber = framePaddingDictinary[1] 
                
        if framePadding == 5:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[5]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 1000 and currentFrame <10000:
                framePaddingNumber = framePaddingDictinary[2]    
            else:
                framePaddingNumber = framePaddingDictinary[1]
                
        if framePadding == 6:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[6]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[5]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 1000 and currentFrame <10000:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 10000 and currentFrame <100000:
                framePaddingNumber = framePaddingDictinary[2]        
            else:
                framePaddingNumber = framePaddingDictinary[1]
                
        if framePadding == 7:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[7]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[6]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[5]
            elif currentFrame >= 1000 and currentFrame <10000:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 10000 and currentFrame <100000:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 100000 and currentFrame <1000000:
                framePaddingNumber = framePaddingDictinary[2]            
            else:
                framePaddingNumber = framePaddingDictinary[1]
                
        if framePadding == 8:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[8]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[7]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[6]
            elif currentFrame >= 1000 and currentFrame <10000:
                framePaddingNumber = framePaddingDictinary[5]
            elif currentFrame >= 10000 and currentFrame <100000:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 100000 and currentFrame <1000000:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 1000000 and currentFrame <10000000:
                framePaddingNumber = framePaddingDictinary[2]                
            else:
                framePaddingNumber = framePaddingDictinary[1]
        
        if framePadding == 9:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[9]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[8]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[7]
            elif currentFrame >= 1000 and currentFrame <10000:
                framePaddingNumber = framePaddingDictinary[6]
            elif currentFrame >= 10000 and currentFrame <100000:
                framePaddingNumber = framePaddingDictinary[5]
            elif currentFrame >= 100000 and currentFrame <1000000:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 1000000 and currentFrame <10000000:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 10000000 and currentFrame <100000000:
                framePaddingNumber = framePaddingDictinary[2]                      
            else:
                framePaddingNumber = framePaddingDictinary[1]
        
        if framePadding == 10:
            if currentFrame >= 0 and currentFrame <10:
                framePaddingNumber = framePaddingDictinary[10]
            elif currentFrame >= 10 and currentFrame <100:
                framePaddingNumber = framePaddingDictinary[9]
            elif currentFrame >= 100 and currentFrame <1000:
                framePaddingNumber = framePaddingDictinary[8]
            elif currentFrame >= 1000 and currentFrame <10000:
                framePaddingNumber = framePaddingDictinary[7]
            elif currentFrame >= 10000 and currentFrame <100000:
                framePaddingNumber = framePaddingDictinary[6]
            elif currentFrame >= 100000 and currentFrame <1000000:
                framePaddingNumber = framePaddingDictinary[5]
            elif currentFrame >= 1000000 and currentFrame <10000000:
                framePaddingNumber = framePaddingDictinary[4]
            elif currentFrame >= 10000000 and currentFrame <100000000:
                framePaddingNumber = framePaddingDictinary[3]
            elif currentFrame >= 100000000 and currentFrame <1000000000:
                framePaddingNumber = framePaddingDictinary[2]                          
            else:
                framePaddingNumber = framePaddingDictinary[1]                                

        if framePaddingNumber != []:
            return framePaddingNumber
        

    def getRenderLayers(self, *args):
       
        #clear renderlayers list
        currentRenderLayer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        
        renderLayers = cmds.ls(exactType ="renderLayer")
        
        renderableLayers = []
        renderFlags = []
        
        for renderLayer in renderLayers:
            renderFlag = cmds.getAttr((renderLayer+".renderable"))
                
            if renderFlag:
                renderableLayers.append(renderLayer)
            else:
                renderFlags.append(renderFlag)
                        
        
        return [renderableLayers,currentRenderLayer, renderFlags]
    

    def  getCameras(self, *args):
        
        cameras = cmds.listCameras(perspective=True)
        currentCamera = cmds.lookThru(query=True)
        
        return [cameras, currentCamera]

    
    #Refresh Camera list
    def refreshCameras(self, *args):
        
        cameras = self.getCameras()
        
        cmds.textScrollList(self.cameraSettingsTextScroll,edit=True, removeAll=True, )
        cmds.textScrollList(self.cameraSettingsTextScroll,edit=True, append=cameras[0])            
        sys.stderr.write("<<RVBR: cameras clreared>>\n")       
    
    
    #Referesh render layers
    def refreshRenderLayers(self, *args):
        selectedCamera = cmds.textScrollList(self.cameraSettingsTextScroll, query=True, selectItem=True)
        renderablelayers =self.getRenderLayers()

        cmds.textScrollList(self.layersTextsScroll, edit=True, removeAll=True)
        cmds.textScrollList(self.layersTextsScroll, edit=True, append= renderablelayers[0])
        cmds.textScrollList(self.layersTextsScroll, edit=True, enable=True)
        
        masterLayer = "masterLayer"
        addedLayer = []
        
        if selectedCamera != None:
            for camera in selectedCamera:
                listAttr = cmds.listAttr(camera, locked=True)
                if listAttr != None:
                    if masterLayer in listAttr:
                         listAttr[listAttr.index('masterLayer')] = 'defaultRenderLayer' #Replase masterLayer by defaultRenderLayer
                    for layer in renderablelayers[0]:
                        if layer in listAttr:
                            cmds.button(self.apllySettingsBtn, edit=True, label="Edit")
                            addedLayer.append(layer)
                            cmds.textScrollList(self.layersTextsScroll, edit=True, allowMultiSelection=True)
                            cmds.textScrollList(self.layersTextsScroll, edit=True, selectItem=layer)
                else:
                    
                    cmds.button(self.apllySettingsBtn, edit=True, label="Save Settings")
        
        cmds.button(self.apllySettingsBtn, edit=True, enable=False)         
        self.infoPannel("cameras")

   
   
    def resetAll(self, *args):
        
        allCameras = self.getAllCamerasLayersPasses()[0]
        allRenderLayers = self.getAllCamerasLayersPasses()[1]
        
        masterLayer = "masterLayer"
        
        attr = 0
        
        for camera in allCameras:
            listAttributes = cmds.listAttr(camera, locked=True)
            if listAttributes != None:
                for renderLayer in allRenderLayers:
                    if renderLayer == 'defaultRenderLayer':
                        renderLayer = masterLayer
                    if renderLayer in listAttributes:  
                        attr = 1 
                if attr == 1:
                    for attribute in listAttributes:         
                        if attribute == 'masterLayer':          # Here attribute is called "masterLayer" and we need to rename it to "defaultRenderLayer" because
                            attribute = 'defaultRenderLayer'    # we need to find 'defaultRenderLayer' in all renderLayers for nex loop
                        if attribute in allRenderLayers:
                            if attribute == 'defaultRenderLayer':     # Here we need to rename defaultRenderLayer to masterLayer again because 
                                attribute = masterLayer               # we need to delete masterLayer attribute.             
                            cmds.setAttr((camera+"."+attribute), lock=False)
                            cmds.deleteAttr(camera, attribute=attribute)
            
        #Disconnec and deselect all renderPasses
        self.disConnectRenderPasses()
        self.disconnectSelectedRenderPass("deselect")
        
        if listAttributes == None:
           sys.stderr.write("<<RVBR: All Settings Are Reset>>\n")

        cmds.floatField(self.cameraSettingsStartFrameValue, edit=True, value= 1.000)
        cmds.floatField(self.cameraSettingsEndFrameValue, edit=True, value=10.000)
        cmds.button(  self.excludeLayerBtn, edit=True, enable=False, )
        cmds.button(self.resetAllBtn, edit=True, enable=False)
        cmds.button(self.apllySettingsBtn, edit=True, label="Save Settings")

        self.disconnectAll_renderPasses('resetAll')
      
    
    def resetLayer(self, *args):

        selectedCamera = self.getSelectedItemsFromList()[0]
        selectedRenderlayer = self.getSelectedItemsFromList()[1]
        renderPasses = self.getAllCamerasLayersPasses()[2]
        masterLayer = "masterLayer"
        
        for camera in selectedCamera:
            for renderLayer in selectedRenderlayer:
                listAttr = cmds.listAttr(camera, locked=True)
                if renderLayer in  listAttr:
                    if renderLayer == "defaultRenderLayer":
                        renderLayer = masterLayer
                    cmds.setAttr((camera+"."+renderLayer), lock=False)
                    cmds.deleteAttr(camera, attribute=renderLayer)

        self.disConnectRenderPassForSelectedLayers(selectedRenderlayer,renderPasses )
        
        cmds.button(self.excludeLayerBtn, edit=True,  enable=False)
        cmds.button(self.apllySettingsBtn, edit=True, label="Save Settings")
       
    
    def resetAllScriptJob(self, *args):
        
        self.cleanUpImagesDirectory()
        allCams = self.getAllCamerasLayersPasses()[0]
        allLayers = self.getAllCamerasLayersPasses()[1]
        renderPasses = self.getAllCamerasLayersPasses()[2]
        
        for camera in allCams:
            listAttributes = cmds.listAttr(camera, locked=True)
            if listAttributes != None:
                for attribute in listAttributes:
                    if attribute in allLayers or attribute == "masterLayer":
                        cmds.setAttr((camera+"."+attribute), lock=False)
                        cmds.deleteAttr(camera, attribute=attribute)
        
        
        self.disConnectRenderPassForSelectedLayers(allLayers,renderPasses )
        self.deleteRenderlayersMonitorScriptJob()
        
    # Activate/deactivate Custom resolution
    def activateCustomResolution(self, *args):
        
        customResolutionCheckbox = cmds.checkBox(self.activateCustomResolutionCheckBox, query=True, value=True)
        
        if customResolutionCheckbox == 1:
            cmds.intField(self.customHeight, edit=True, enable=True)
            cmds.intField(self.customWidth, edit=True, enable=True)
            cmds.optionMenuGrp(self.imageResolutionOptionMenu, edit=True, enable=False) #activate images size optionMenuGrp
        else:
            cmds.intField(self.customHeight, edit=True, enable=False)
            cmds.intField(self.customWidth, edit=True, enable=False) 
            cmds.optionMenuGrp(self.imageResolutionOptionMenu, edit=True, enable=True)  #deactivate images size optionMenuGrp  
   
            
    def layerSettingsScrollEnableDisable(self, commandId, *args):
        
        self.refreshRenderPasses()
        
        #To avoid dobble click for select item.Get currentry selected item. Set allowMultiSelection to False and then select queried item. 
        selectedItem = cmds.textScrollList(self.layersTextsScroll, query=True, selectItem=True)
        cmds.textScrollList(self.layersTextsScroll, edit=True, allowMultiSelection=False)
        cmds.textScrollList(self.layersTextsScroll, edit=True, selectItem=selectedItem[0])
        
        if commandId == "Enable":
            cmds.text(self.cameraSettingsStartFrameText, edit=True, enable=True)
            cmds.floatField( self.cameraSettingsStartFrameValue,  edit=True,enable=True)
            cmds.text( self.cameraSettingsEndFarmeText, edit=True, enable=True)
            cmds.floatField( self.cameraSettingsEndFrameValue, edit=True, enable=True)
            cmds.text( self.camerasSettingsAllPassesText, edit=True ,enable=True )
            cmds.button(self.createRemoveRenderPassesBtn, edit=True, enable=True)
            cmds.textScrollList(self.cameraSettingsPassesTextScroll,edit=True, enable=True)
            cmds.button(self.apllySettingsBtn, edit=True, enable=True)
            
            #Enable reset button
            selectedCamera = self.getSelectedItemsFromList()[0]
            selectedLayers = self.getSelectedItemsFromList()[1]
            allRenderPasses = self.getAllCamerasLayersPasses()[2]
            connectedRenderPasses = []
            
            if selectedLayers:
                for layer in selectedLayers:
                     connectedRenderPasses = cmds.listConnections((layer+".renderPass"), exactType=True) 

            cameraAttributes = cmds.listAttr(selectedCamera, locked=True)
            masterLayer = "masterLayer"
            
            if selectedLayers:
                for layer in selectedLayers:
                    if layer == "defaultRenderLayer":
                        layer = masterLayer
                    if cameraAttributes != None:
                        if layer in cameraAttributes or len(selectedLayers) > len(cameraAttributes):
                            cmds.button(self.excludeLayerBtn, edit=True, enable=True)
                            cmds.button(self.apllySettingsBtn, edit=True, label="Edit")
                            if connectedRenderPasses != None:
                                for renderPass in connectedRenderPasses:
                                     cmds.textScrollList(self.cameraSettingsPassesTextScroll, edit=True, selectItem=renderPass)
                        else:
                            cmds.button(self.excludeLayerBtn, edit=True, enable=False)
                            cmds.button(self.apllySettingsBtn, edit=True, label="Save Settings")
                    else:
                        if connectedRenderPasses != None:
                                for renderPass in connectedRenderPasses:
                                    cmds.textScrollList(self.cameraSettingsPassesTextScroll, edit=True, selectItem=renderPass)
                       
        if commandId == "Save":
            
            #Check if layer is selected and it's settings is active. To get this we will check if one of the element(in this case text) is enabled
            enabled = cmds.text(self.cameraSettingsStartFrameText, query=True, enable=True)
            if enabled:
                cmds.text(self.cameraSettingsStartFrameText, edit=True, enable=False)
                cmds.floatField( self.cameraSettingsStartFrameValue,  edit=True,value=1.00, enable=False)
                cmds.text( self.cameraSettingsEndFarmeText, edit=True, enable=False)
                cmds.floatField( self.cameraSettingsEndFrameValue, edit=True,value=2.00, enable=False)
                cmds.text( self.camerasSettingsAllPassesText, edit=True ,enable=False )
                cmds.button(self.createRemoveRenderPassesBtn, edit=True, enable=True)
                cmds.textScrollList(self.cameraSettingsPassesTextScroll,edit=True,deselectAll=True, enable=False)    
                cmds.button(self.apllySettingsBtn, edit=True, enable=False)
                cmds.button(self.createRemoveRenderPassesBtn, edit=True, enable=False)
                sys.stderr.write("<<RVBR: Settings Saved>>\n")
        
        self.editStartEndFrames()
        self.infoPannel("layers")
    
    
    def editStartEndFrames(self):
        
        currentLayers = self.getSelectedItemsFromList()[1]
        currentCamera = self.getSelectedItemsFromList()[0]
        attributeList = cmds.listAttr(currentCamera, locked=True)
        masterLayer = "masterLayer"
        
        if currentLayers:
            for layer in currentLayers:
                if layer == "defaultRenderLayer":
                        layer = masterLayer
                if attributeList != None:
                    if layer in attributeList:
                        cameraAttr = cmds.getAttr(currentCamera[0]+'.'+layer)
                        tempStartEndFrames_partitioned = str(cameraAttr).partition(';')[2]
                        tempStartEndFrames = tempStartEndFrames_partitioned.translate(None, ';')
                        startFrame =  tempStartEndFrames.split(',')[0]
                        endFrame =  tempStartEndFrames.split(',')[1]
                        cmds.floatField(self.cameraSettingsStartFrameValue,edit=True, value= float(startFrame))
                        cmds.floatField(self.cameraSettingsEndFrameValue,edit=True, value= float(endFrame))                
                    else:
                        cmds.floatField(self.cameraSettingsStartFrameValue,edit=True, value= 1.000)
                        cmds.floatField(self.cameraSettingsEndFrameValue,edit=True, value= 10.000)        
    
    
    def getAllCamerasLayersPasses(self):
        
        allCams = cmds.listCameras(perspective=True)
        allLayers = cmds.ls(exactType ="renderLayer")
        allPasses = cmds.ls(exactType = "renderPass")  
        
        return [allCams,allLayers, allPasses]
    
    
    def getSelectedItemsFromList(self, *args):
        
        selectedCamera = cmds.textScrollList(self.cameraSettingsTextScroll, query=True, selectItem=True)
        selectedLayers = cmds.textScrollList(self.layersTextsScroll, query=True, selectItem=True)
        selectedRenderPasses = cmds.textScrollList(self.cameraSettingsPassesTextScroll, query=True, selectItem=True)
        
        return [selectedCamera,selectedLayers,selectedRenderPasses ]
    
    
    def detectPlatform(self):
        
        operatingSystem = []
        getPlatform = platform.system()
        
        if getPlatform == "Windows":
            operatingSystem = "Windows"
        elif getPlatform == "Darwin":
            operatingSystem = "OSX"
        else:
            operatingSystem = "Linux"
        
        return operatingSystem
    
    
    def detectRendererVersion(self):
        
        rendererVersion = cmds.getAttr( 'defaultRenderGlobals.currentRenderer')
        
        return rendererVersion
    
    def collapseAndExpandFrames(self, frame, state, *args):
        
        frameName = frame
        frameState = state
        collapseHeight = 20
        expandHeight = 0
        frameLayoutName = []
        
        if frameName == "firstBloque":
            frameLayoutName = self.firstGroupFrame
            expandHeight = 200
        
        elif frameName == "secondBloque":
            frameLayoutName = self.secondGroupFrame
            expandHeight = 100
            
        elif frameName == "thirdBloque":
            frameLayoutName = self.thirdGroupFrame
            expandHeight = 305
            
        elif frameName == "fourthBloque":
            frameLayoutName = self.fourthGroupFrame            
            expandHeight = 120
        
        if  frameState == "collapse":
            cmds.frameLayout(frameLayoutName, edit=True, height = collapseHeight)
        
        elif frameState == "expand":
            cmds.frameLayout(frameLayoutName, edit=True, height = expandHeight)
    
    
    def renderPassesButtonChange(self, *args):
        
        # Button callback
        cmds.popupMenu(self.renderPassesPopupMenu, edit=True,  button=3)
        selectedRenderPass = cmds.textScrollList(self.cameraSettingsPassesTextScroll, query=True, selectItem=True)
        cmds.button(self.createRemoveRenderPassesBtn, edit=True, label="Remove", command= partial(self.removeRenderPass,selectedRenderPass))
        
        #Enable deselect button
        cmds.button(self.deselectRPassesBtn, edit=True, enable=True)
    
    
    def infoPannel(self, layout):
        
        masterLayer = 'masterLayer'
        
        if layout == "cameras":
            addedLayers = []
            selectedCamera = cmds.textScrollList(self.cameraSettingsTextScroll, query=True, selectItem=True)
            allLayers = self.getAllCamerasLayersPasses()[1]
            
            for camera in selectedCamera:
                listCamAttr = cmds.listAttr(camera, locked=True)
                if listCamAttr != None:
                    for layer in allLayers:
                        if layer == 'defaultRenderLayer':
                            layer = masterLayer
                        if layer in listCamAttr:
                            addedLayers.append(layer)
            
            childrenNumber =cmds.scrollLayout(self.fourthGroupTableScrollLayout, query=True, numberOfChildren=True)
            childrenName = cmds.scrollLayout(self.fourthGroupTableScrollLayout, query=True, childArray=True)
            
            if childrenName != None:
                for child in childrenName:
                    cmds.deleteUI(child)
                
            for addedLayer in addedLayers:
                cmds.text(label=addedLayer, parent=self.fourthGroupTableScrollLayout, font="plainLabelFont" )
            
        ##############################
        if layout == "layers":
            addedPasses = []
            selectedRenderLayer = cmds.textScrollList(self.layersTextsScroll, query=True, selectItem=True)
            allPasses = self.getAllCamerasLayersPasses()[2]
            
            if selectedRenderLayer:
                for renderlayer in selectedRenderLayer:
                    listconnectedPasses = cmds.listConnections(renderlayer+".renderPass")
                    if listconnectedPasses != None:
                        for rpass in allPasses:
                            if rpass in listconnectedPasses:
                                addedPasses.append(rpass)
            
            childrenNumber =cmds.scrollLayout(self.fourthGroupTableScrollLayout, query=True, numberOfChildren=True)
            childrenName = cmds.scrollLayout(self.fourthGroupTableScrollLayout, query=True, childArray=True)
            if childrenName != None:
                for child in childrenName:
                    cmds.deleteUI(child)
            
            addedPasses = sorted(set(addedPasses))
            for addedPass in addedPasses:
                cmds.text(label=addedPass, parent=self.fourthGroupTableScrollLayout, font="plainLabelFont" )
                
            
    def renderPassMenuItemIteration(self, state):
        state=state
        renderPassesDictionary = {1:"Blank", 2:"2D Motion Vector", 3:"3D Motion Vector", 4:"Ambient Irradience", 5:"Ambient Material Color", 6:"Ambient Occlusion",
                                  7:"Ambient", 8:"Beauty Without Reflections and Refractions", 9:"Beauty", 10:"Camera Depth Remaped", 11:"Camera Depth", 12:"Coverage",
                                  13:"Custom Color", 14:"Custom Depth", 15:"Custom Label", 16:"Custom Vector", 17:"Diffuse Material Color", 18:"Diffuse Without Shadows",
                                  19:"Diffuse", 20:"Direct Irradiance Without Shadows", 21:"Direct Irradiance", 22:"Glow Source", 23:"Incandescence", 24:"Incidence (Light/Normal)",
                                  25:"Indirect", 26:"Light Volume", 27:"Material Incidence (Camera/Normal)", 28:"Material Normal (Camera spae)", 29:"Material Normal (Object space)",
                                  30:"Material Normal (World space)", 31:"Matte", 32:"Normalized 2D Motion Vector", 33:"Object Incidence (Camera/Norma)", 34:"Object Normal (Camera space)",
                                  35:"Object Normal (Object space)", 36:"Object Normal (World space)", 37:"Object Volume", 38:"Opacity",39:"Raw Shadow", 40:"Reflected Material Color",
                                  41:"Reflection", 42:"Refraction Material Color", 43:"Refraction", 44:"Scatter", 45:"Scene Volume", 46:"Shadow", 47:"Specular Without Shadows", 48:"Specular",
                                  49:"Translucence Without Shadows", 50:"Translucence", 51:"UVPass", 52:"World Position"}
        
        if state == "initial_call":       
            counter = 1
            for menuItem in renderPassesDictionary:
                cmds.menuItem(label=renderPassesDictionary[counter], command=partial(self.createRenderPasses, renderPassesDictionary[counter]))
                counter += 1
        else:
            return         

    
    def createScriptJobForRenderableAttributes(self):
        
        self.deleteRenderlayersMonitorScriptJob()
        
        renderLayers = cmds.ls(type="renderLayer")
        
        for layer in renderLayers:
            scr = cmds.scriptJob(ac =[layer+".renderable", self.refreshRenderLayers], parent = self.mainWindow)
            self.scrJobs.append(scr)
        
    
    def deleteRenderlayersMonitorScriptJob(self):
        
        scjobs = self.scrJobs
        
        if scjobs:
            for job in scjobs:
                allJobs = cmds.scriptJob(listJobs=True)
                for j in allJobs:
                    if str(job) in j:
                        cmds.scriptJob(kill=job)
    
    
    
    def changeMenuItems(self):
        currentRenderer = self.detectRendererVersion()
        
        if currentRenderer == 'mayaSoftware':
            cmds.menuItem(self.sgiMenuItem, edit=True, label="SGI (sgi)")
            cmds.menuItem(self.sgi16MenuItem, edit=True, enable=True)
        
        if currentRenderer == 'mentalRay':
           cmds.menuItem(self.sgiMenuItem, edit=True, label="SGI (rgb)")               
           cmds.menuItem(self.sgi16MenuItem, edit=True, enable=False)
    
    def deleteScriptJobs(self):
        
        cmds.scriptJob(kill=self.quitAppJob)
        cmds.scriptJob(kill=self.sceneOpenJob)
    
    
    def cleanUpImagesDirectory(self, *args):
        #Clean up tmp images directory
        # Get temporal directory of rendered image. 
        currentProject = cmds.workspace(fullName=True)
        imagesDirectory = cmds.workspace('images', query=True, fileRuleEntry=True)
        
        # If realtive path
        if imagesDirectory == "images":
            tempImageFolder = currentProject + "/"+ imagesDirectory + "/tmp/"
        
        # If absolute path
        else:
           tempImageFolder = cmds.workspace('images', query=True, fileRuleEntry=True)+"/tmp/"
        
        if os.path.exists(tempImageFolder):
            shutil.rmtree(tempImageFolder)
            

    # UI
    def ikRenderViewBatchRendererUI(self, *args):
        cmds.RenderViewWindow()
        cmds.showWindow("renderViewWindow")
        
        cmds.setAttr("defaultResolution.width", 1280)
        cmds.setAttr("defaultResolution.height", 720)
        cmds.setAttr("defaultResolution.deviceAspectRatio", 1.777)
        cmds.setAttr("defaultResolution.pixelAspect", 1.000)
        
        #get list of cameras
        cameras = self.getCameras()[0]
        currentCamera = self.getCameras()[1]
        renderableLayers = self.getRenderLayers()[0]
        currentRenderLayer = self.getRenderLayers()[1]
        renderPasses = self.getRenderPasses()[0]
        currentProject = cmds.workspace(query=True,rootDirectory=True)
        currentProject = currentProject+'images'
        
       
        if cmds.window("ikRVBR",exists=True,):
            cmds.deleteUI("ikRVBR") 
            
        self.mainWindow = cmds.window("ikRVBR", title="IK Render View Batch renderer v2.0.6", sizeable=False, width=100, height=500)
        mainColumn = cmds.columnLayout(adjustableColumn=True, columnAlign = "center") 
        
        #First Bloque
        self.firstGroupFrame = cmds.frameLayout(collapsable=True, labelVisible=True, label="Directory & Resolution", borderVisible=False, width=450, height=200,
                                                cc=partial(self.collapseAndExpandFrames, "firstBloque", "collapse"), ec=partial(self.collapseAndExpandFrames,"firstBloque", "expand"))
        firstGroupScroll = cmds.scrollLayout(hst=0)
        
        cmds.text(label="")#just for space
        self.getDestinationDirectoryField = cmds.textFieldButtonGrp(label="Directory:", buttonLabel="Browse", text=currentProject, buttonCommand=self.getPath, editable=False, annotation="Set destination path for output files")
        
        cmds.rowColumnLayout(nc=3, columnSpacing = ([1,53],[2,1]),rowSpacing=[1,3])  # This rowLayout is especially "for Output file name"
        cmds.text(label="Output File Name:")
        self.outputfileName = cmds.textField(width=240, text="Untitled")
        cmds.text(label="", height=5)
        cmds.text(label="", height=5)
        cmds.text(label="", height=5)
        
        cmds.rowColumnLayout(nc=3,columnSpacing = ([1,45],[2,3]), rowSpacing=[1,3], parent=firstGroupScroll, width =250) # This rowLayout is especially "Start and End Frame"
       
        
        
        
        cmds.text(label="           Custom Size:")
        self.activateCustomResolutionCheckBox = cmds.checkBox(label="", onCommand=self.activateCustomResolution, offCommand=self.activateCustomResolution)
        cmds.text(label="")
        
        cmds.text(label="", height=3)
        cmds.text(label="", height=3)
        cmds.text(label="", height=3)
 
        cmds.text(label="                    Width:")
        self.customWidth = cmds.intField(value=2.0, enable=False ,width =80 , minValue=2, changeCommand=self.imageResolution, enterCommand=self.imageResolution) # Res Min value is 2 by default
        cmds.text(label="")
        cmds.text(label="                   Height:")
        self.customHeight = cmds.intField(value=2.0, enable=False, width =80,minValue=2, changeCommand=self.imageResolution, enterCommand=self.imageResolution)# Res Min value is 2 by default
        
        
        cmds.text(label="", height=3)
        cmds.text(label="", height=3)
        
        self.imageResolutionOptionMenu = cmds.optionMenuGrp(label="Size Presets:", parent=firstGroupScroll, changeCommand=self.imageResolution)
        cmds.menuItem(label="320x240")
        cmds.menuItem(label="640x480")
        cmds.menuItem(label="1k Square")
        cmds.menuItem(label="2k Square")
        cmds.menuItem(label="3k Square")
        cmds.menuItem(label="4k Square")
        cmds.menuItem(label="CCIR PAL/Quantel PAL")
        cmds.menuItem(label="CCIR 601/Quantel NTSC")
        cmds.menuItem(label="Full 1024")
        cmds.menuItem(label="Full 1280/Screen")
        cmds.menuItem(label="HD 540")
        cmds.menuItem(label="HD 720")
        cmds.menuItem(label="HD 1080")
        cmds.menuItem(label="NTCS 4D")
        cmds.menuItem(label="PAL 768")
        cmds.menuItem(label="PAL 780")
        cmds.optionMenuGrp(self.imageResolutionOptionMenu, edit=True, select=12)
        
        #Second Bloque
        self.secondGroupFrame = cmds.frameLayout(collapsable=True, labelVisible=True, label="Format & Frame Padding",borderVisible=False, width=400, height=100, parent= mainColumn,
                                                 cc=partial(self.collapseAndExpandFrames, "secondBloque", "collapse"), ec=partial(self.collapseAndExpandFrames,"secondBloque", "expand"))
        secondGroupScroll = cmds.scrollLayout(hst=0)

        cmds.text(label="")#just for space
        
        # Get Maya version
        rendererVersion = self.detectRendererVersion()
        
        self.imageFormats = cmds.optionMenuGrp(label="Image Format:", changeCommand=self.renderImageFormats)
        cmds.menuItem(label="Maya IFF (iff)")
        cmds.menuItem(label="OpenEXR (exr)")
        cmds.menuItem(label="HDR (hdr)")
        cmds.menuItem(label="Cineon (cin)")
        cmds.menuItem(label="DDS (dds)")
        cmds.menuItem(label="EPS (eps)")
        cmds.menuItem(label="GIF (gif)")
        cmds.menuItem(label="JPEG (jpg)")
        cmds.menuItem(label="Alias PIX (als)")
        cmds.menuItem(label="Maya16 IFF (iff)")
        cmds.menuItem(label="PSD (psd)")
        cmds.menuItem(label="PSD Layered (psd)") 
        cmds.menuItem(label="PNG (png)")
        cmds.menuItem(label="Quantel (yuv)")
        cmds.menuItem(label="RLA (rla)")
        if rendererVersion == "mayaSoftware":
            self.sgiMenuItem = cmds.menuItem(label="SGI (sgi)")
            self.sgi16MenuItem = cmds.menuItem(label="SGI16 (sgi)", enable=True)
        if rendererVersion =="mentalRay":
             self.sgiMenuItem = cmds.menuItem(label="SGI (rgb)")    
             self.sgi16MenuItem = cmds.menuItem(label="SGI16 (sgi)", enable=False)
        
        cmds.menuItem(label="Softimage (pic)")
        cmds.menuItem(label="Targa (tga)")
        cmds.menuItem(label="Tiff (tif)")
        cmds.menuItem(label="Tiff16 (tif)")
        cmds.menuItem(label="Windows Bitmap (bmp)")
        
        cmds.text(label="",height=3)#just for space
        self.faramePadding = cmds.intSliderGrp(label="Frame Padding:",field=True, minValue=1, maxValue=10, value=1, changeCommand=self.framePaddingFunction)
        
        #Third Bloque
        
        self.thirdGroupFrame = cmds.frameLayout(label="Cameras, Layers & Render Passes", borderVisible=False,labelVisible=True, collapsable=True,width=400, height=305, parent= mainColumn,
                                                cc=partial(self.collapseAndExpandFrames, "thirdBloque", "collapse"), ec=partial(self.collapseAndExpandFrames,"thirdBloque", "expand"))
        thirdGroupScroll =  cmds.scrollLayout(hst=0)
        thirdGroupRowColumnLayout = cmds.rowColumnLayout(nc=2, columnSpacing = ([1,1],[2,1]),rowSpacing=[1,5])
        self.aditionalFormLayout = cmds.formLayout()
        
        self.layersListText = cmds.text(label="Render Layers:")
        self.cameraListText = cmds.text(label="Cameras:", visible=True)
        self.cameraSettingsText = cmds.text(label="Settings:", visible=True)
        
        self.cameraSettingsTextScroll = cmds.textScrollList(numberOfRows = 8, allowMultiSelection=False, width=140, height=250, parent=self.aditionalFormLayout, append=cameras, selectItem=currentCamera, selectCommand=self.refreshRenderLayers )
        self.layersTextsScroll = cmds.textScrollList(numberOfRows = 8, allowMultiSelection=False, width=140, height=197, append = renderableLayers, selectCommand = partial(self.layerSettingsScrollEnableDisable, "Enable"))
        
        self.cameraSettingsScrollLayout = cmds.scrollLayout(visible=True,  width=140, height=197, parent=self.aditionalFormLayout)
        self.cameraSettingRowClumnLayout = cmds.rowColumnLayout( nc=2, parent=self.cameraSettingsScrollLayout, columnSpacing=[2,5], rowSpacing=[2,5], columnAlign=[1, "left"])
       
        self.cameraSettingsStartFrameText = cmds.text(label="Start Frame:", parent=self.cameraSettingRowClumnLayout, enable=False)
        self.cameraSettingsStartFrameValue = cmds.floatField(value=1.000, parent=self.cameraSettingRowClumnLayout,enable=False)
        self.cameraSettingsEndFarmeText = cmds.text(label="End Frame:", parent=self.cameraSettingRowClumnLayout,enable=False)
        self.cameraSettingsEndFrameValue = cmds.floatField( value=10.000,parent=self.cameraSettingRowClumnLayout,enable=False)
        self.camerasSettingsAllPassesText = cmds.text(label="Passes:", parent=self.cameraSettingRowClumnLayout,enable=False )
        self.createRemoveRenderPassesBtn = cmds.button(label="Create", width=42, height= 20, command=self.createRenderPasses,enable=False, annotation="Create or Remove Render pass")
        self.renderPassesPopupMenu = cmds.popupMenu(button=1)
        self.renderPassMenuItemIteration("initial_call")
        
        self.cameraSettingsPassesTextScroll = cmds.textScrollList(width = 130, height=117, parent=self.cameraSettingsScrollLayout, allowMultiSelection=True,append=renderPasses, enable=False, selectCommand=self.renderPassesButtonChange)
        
        self.resetAllBtn=cmds.button(label="Reset All Settings", parent=self.aditionalFormLayout,  enable=False, width=142, height= 25, command=self.resetAll, annotation="Reset All Settings Of All Cameras And Render Layers")
        self.excludeLayerBtn=cmds.button( label="Exclude Layer", parent=self.aditionalFormLayout, width=142, height= 25, command=self.resetLayer, enable=False, annotation="Remove Render Layer From Render List ")
        self.apllySettingsBtn=cmds.button( label="Save Settings", parent=self.aditionalFormLayout, width=138, height= 25, command=self.saveRenderSettings, enable=False, 
                                          annotation="Save User Settings For Selected Layer And-\nEdit Render Passes List Of Each Render Layer ")
        self.deselectRPassesBtn=cmds.button( label="Deselect Render Pass", parent=self.aditionalFormLayout, width=138, height= 25, command=partial(self.disconnectSelectedRenderPass, "deselect"), enable=False, annotation="Deselect Render Pass")
        
        cmds.formLayout(self.aditionalFormLayout, edit=True,attachForm=[(self.cameraSettingsTextScroll, "top", 18), (self.cameraSettingsTextScroll, "left", 1),
                                                                        (self.layersTextsScroll, "top", 18),(self.layersTextsScroll, "left", 149),
                                                                        (self.cameraSettingsScrollLayout, "top", 18), (self.cameraSettingsScrollLayout, "left", 295),
                                                                        (self.cameraListText, "top", 1),(self.cameraListText, "left", 40),
                                                                        (self.layersListText,  "top", 1), (self.layersListText,  "left", 185),
                                                                        (self.cameraSettingsText, "top", 1), (self.cameraSettingsText, "left", 340),
                                                                        (self.resetAllBtn, "top", 244 ), (self.resetAllBtn, "left", 148),
                                                                        (self.excludeLayerBtn, "top", 217), (self.excludeLayerBtn, "left", 148),
                                                                        (self.apllySettingsBtn, "top", 244), (self.apllySettingsBtn, "left", 297),
                                                                        (self.deselectRPassesBtn, "top",217 ), (self.deselectRPassesBtn, "left", 297),])  
       
       
       
        #fourth bloque info
        
        self.fourthGroupFrame = cmds.frameLayout(label="Connections Info", borderVisible=False,labelVisible=True, collapsable=True, width=400, height=120, parent= mainColumn, 
                                                 cc=partial(self.collapseAndExpandFrames, "fourthBloque", "collapse"), ec=partial(self.collapseAndExpandFrames,"fourthBloque", "expand"), annotation="Information about connected cameras, renderlayers and renderPasses")
       
        
        self.fourthGroupRowColumnLayout = cmds.rowColumnLayout(nc=1, columnSpacing = ([1,0]),rowSpacing=[1,5])
        self.fourthGroupConnectedItems = cmds.text(label="Connected Items:")
        self.fourthGroupTableScrollLayout = cmds.scrollLayout( hst=0, vst=0, width=449, height= 82, childResizable=True)
        
    
        #Buttons bloque
        mainWindow =  "ikRVBR"
        
        renderButtonGroupFrame = cmds.frameLayout(collapsable=False, borderVisible=False,labelVisible=False,  width=400, height=45, parent= mainColumn)
        renderButtonGroupScroll =  cmds.scrollLayout(hst=0)
        renderButtonRowColumnLayout = cmds.rowColumnLayout(nc=2,columnSpacing = ([1,1],[2,1]), columnWidth = ([1,219], [2,219]))
        
        self.renderButton = cmds.button(label="Render",height=35, command=self.doRender, annotation="Go! Render It!" , enable=False)
        closButton = cmds.button(label="Close", height=35, command = partial(self.closeMainWindow,mainWindow))
       
        #Execute this functions to start render without changig attributes
        self.renderImageFormats("Maya IFF (iff)")
        self.framePaddingFunction(1)
        
          
        cmds.scriptJob(uiDeleted=["ikRVBR", self.resetAllScriptJob]) #runOnce no need if uiDeleted used
        self.quitAppJob = cmds.scriptJob(runOnce=True, event=["quitApplication", self.resetAllScriptJob])
        self.refreshRenderPassesLayout = cmds.scriptJob(event=["renderPassChange", self.refreshRenderPasses], parent = self.mainWindow)
        self.refreshRenderLayersLayout = cmds.scriptJob(event=["renderLayerChange", self.refreshRenderLayers], parent = self.mainWindow)     
        self.refreshCamerasLayout = cmds.scriptJob(event=["cameraChange", self.refreshCameras], parent = self.mainWindow)
        self.currentRenderScriptJob = cmds.scriptJob(attributeChange = ['defaultRenderGlobals.currentRenderer', self.changeMenuItems], parent = self.mainWindow)
        
        self.scrJobs = [] # This variable is for createScriptJobForRenderableAttributes function
        self.monitorRenderLayers = cmds.scriptJob(event=["renderLayerChange", self.createScriptJobForRenderableAttributes], parent = self.mainWindow)
        # Run this for monitor already existing layers
        self.createScriptJobForRenderableAttributes()
        
       
        self.sceneOpenJob = cmds.scriptJob(event=['SceneOpened', self.disconnectAll_renderPasses])
        
        cmds.scriptJob(uiDeleted=["ikRVBR", self.deleteScriptJobs])
        
        self.cleanUpImagesDirectory()
        
        cmds.showWindow("ikRVBR")    

obj=IkRenderViewBatchRenderer()
obj.ikRenderViewBatchRendererUI()           