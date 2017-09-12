#!/usr/bin/env python
#Para compilar se necesita el mayapy.exe
#C:\Program Files\Autodesk\Maya2015\bin
#mayapy pyside-uic D:\PH_SCRIPTS\PH_FIX\PH_EXOCORTEX\uiExocortex.ui -o uiExocortex.py

#Convertir archivos .ui a extencion .py para leer en pyside.
import sys, pprint
from pysideuic import compileUi
#creo un archivo vacio
pyfile = open("D:\PH_SCRIPTS\PH_FIX\PH_EXOCORTEX\uiExocortex.py", 'w')
#compilo en el mismo directorio convirtiendo el archivo
compileUi("D:\PH_SCRIPTS\PH_FIX\PH_EXOCORTEX\uiExocortex.ui", pyfile, False, 4,False)
#lo cierro para que no se editemas
pyfile.close()

#!/usr/bin/env python
import sys,os
from PySide import QtCore, QtGui, QtUiTools
import maya.cmds as cmds
path=r'D:\PH_SCRIPTS\PH_FIX\PH_EXOCORTEX'
if not path in sys.path:
    sys.path.append(path)
import uiExocortex
reload(uiExocortex)

#Clase necesaria para pyside
class ExoWindow(QtGui.QMainWindow, uiExocortex.Ui_PH_EXOCORTEX):

	def __init__(self, parent=None):
		super(ExoWindow, self).__init__(parent=parent)
#-------------------------------------------------------
		self.setupUi(self)
		listExocortex=[]
		listExocortex=cmds.ls(type='ExocortexAlembicFile')
		if listExocortex == None:
			listExocortex.append('No hay nodos alembic en la escena.')

		#BOTON
		self.BTN_CHANGE.clicked.connect(self.funcion)
	def funcion(self):
		print 'hola'
	#cmds.setAttr(listExocortex[0]+'.fileName',filename, type='string')
    #Exo._import.IJobInfo('D:/PH_SCRIPTS/SCENES_RIG/EXOCORTE/ARTURO_EXO2.abc')
if __name__ == "__main__":

    # Development workaround for winEvent error when running
    # the script multiple times
    try:
        ui.close()
    except:
        pass
    ui = ExoWindow()
    ui.show()

'''
    from PySide import QtCore, QtGui, QtUiTools

    path=r'D:\PH_SCRIPTS\PH_FIX\PH_EXOCORTEX\uiExocortex.ui'
    def loadUiWidget(uifilename, parent=None):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        ui = loader.load(uifile, parent)
        uifile.close()
        return ui


    if __name__ == "__main__":
        import sys
        app = QtGui.QApplication(sys.argv)
        MainWindow = loadUiWidget(path)
        MainWindow.show()
        sys.exit(app.exec_())
'''
