import maya.cmds as cmds
from os import listdir

class TextureImport():
    def __init__(self):
        if cmds.window(TextureImport, q=True, exists=True):
            cmds.deleteUI(TextureImport)
        GUI=cmds.window(title="Texture Import Tool", widthHeight=(250,160), s=True, tlb=True)
        cmds.rowColumnLayout(numberOfColumns=1, columnAlign=(1, 'center'), columnAttach=(1, 'both', 0), cw=(1,250))
        cmds.button(label="Select Directory", command=self.select_dir)
        cmds.separator(style='in', h=20)
        cmds.optionMenu('optionMenu', label="File List")
        cmds.button(label="Clear List", command=self.clear_list)
        cmds.separator(style='in', h=20)
        cmds.text('Select your object, then:', h=25)
        cmds.button(label="Apply Texture", command='')
        cmds.setParent('..')
        cmds.showWindow()

    def select_dir(self, *args):
        basicFilter = "Image Files (*.jpg *.jpeg *.tga *.png *.tiff *.bmp *.psd)"
        self.myDir = cmds.fileDialog2 (fileFilter=basicFilter, dialogStyle=2, fm=3)
        myFiles = listdir(self.myDir[0])

        for items in myFiles:
            fileEndings = ('.psd','.PSD','.jpg','JPG','.jpeg','.JPEG','.tga','.TGA','.png','.PNG','.tiff','.TIFF','.bmp','.BMP')
            if items.endswith(fileEndings):
                cmds.menuItem(items)
            else:
                cmds.warning(items + 'This is not a valid image type, you fool.')
        print myFiles

    def clear_list(self, *args):
        fileList = cmds.optionMenu('optionMenu', q=True, itemListLong=True)
        if fileList:
            cmds.deleteUI(fileList)

coco=TextureImport()
coco=__ini__()
