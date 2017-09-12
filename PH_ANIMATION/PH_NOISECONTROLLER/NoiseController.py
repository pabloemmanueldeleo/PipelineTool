# -*- encoding: utf-8 -*-
#*************************************************************************
 #
 #   file			: NoiseController.py
 #   copyright		: (C) DarkThoughts software
 #   email			: Focus_GFX@hotmail.com
 #   last changed	: LastChangedDate: 30-10-2012 7:12:24
 #
 #   This program is free software; you can redistribute it and/or modify
 #   it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation; either version 2 of the License, or
 #   (at your option) any later version.
 #
 #*************************************************************************/


import maya.OpenMayaUI as mui
import sys
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import sip

uiFile='../NoiseController.ui'
formClass, baseClass = uic.loadUiType(uiFile)

def getSelectedObject():
    selectedObjs = cmds.ls(sl=True)
    if(len(selectedObjs) != 1):
        cmds.warning("Invalid selection.")
        return None

    return selectedObjs

def GenerateMel(obj, value, attr, freq, oct, lac, gin, strn, atrabz):
    expr = ""
    expr += "float $orgvalue = %f;\n" %value
    expr += "float $strength = %f;\n" %strn
    expr += "\n"
    expr += "float $freq = %f;\n" %freq
    expr += "float $oct = %f;\n" %oct
    expr += "float $lac = %f;\n" %lac
    expr += "float $gin = %f;\n" %gin
    abvz = 1 if atrabz else 0
    expr += "float $strAbvZ = %r;\n" %abvz
    expr += "\n"

    expr += "//using our fractional brownian motion generator to have more detailed noise\n"

    expr += "proc float fbm(float $frequency, float $octaves, float $lacunarity, float $gain, float $factor)\n"
    expr += "{\n"
    expr += "    float $val, $amplitude = 1;\n"
    expr += "\n"
    expr += "    for($i = 0; $i < $octaves; $i++)\n"
    expr += "    {\n"
    expr += "        $val += $amplitude * (noise($factor * $frequency) + $strAbvZ);\n"
    expr += "        $factor *= $lacunarity;\n"
    expr += "        $amplitude *= $gain;\n"
    expr += "    }\n"
    expr += "\n"
    expr += "    return $val;\n"
    expr += "\n"
    expr += "}\n"
    expr += "\n"
    expr += "float $result = 0;\n"
    expr += "\n"
    expr += "$result = fbm($freq, $oct, $lac, $gin, time);\n"
    expr += "$result *= $strength;\n"
    expr += "$result += $orgvalue;\n"
    expr += "\n"
    expr += "%s.%s=$result;\n" % (obj[0],attr)

    return expr

def RemoveExpr(obj, attr):
    connections = cmds.listConnections("%s.%s" %(obj[0], attr), s=True, d=False, scn=True)
    if(connections):
        for expr in connections:
            cmds.delete(expr)

def getMayaWindow():
    #Get the maya main window as a QMainWindow instance
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class MainWindow(baseClass, formClass):

    def __init__(self, parent=getMayaWindow()):
        super(baseClass, self).__init__(parent)
        self.setupUi(self)
        self.SetupSignalsSlots()

    def SetupSignalsSlots(self):
        self.connect(self.CmbAttr, QtCore.SIGNAL("currentIndexChanged ( const QString)"), self.CmbAttrCurrentIndexChanged)
        self.connect(self.BtnAssign, QtCore.SIGNAL("clicked()"), self.BtnAssignClicked)
        self.connect(self.BtnRemove, QtCore.SIGNAL("clicked()"), self.BtnRemoveClicked)
        self.connect(self.BtnRefreshAttr, QtCore.SIGNAL("clicked()"), self.BtnRefreshAttrClicked)

    def updateTitle(self, obj, attr):
        self.setWindowTitle("Noise Controller-[%s.%s]" % (obj[0], attr))

    def loadObjAttribs(self, obj):
        attribs = cmds.listAttr(obj, k=True)
        self.CmbAttr.clear()
        for att in attribs:
            self.CmbAttr.addItem(att)

        self.updateTitle(obj, str(self.CmbAttr.currentText()))

    def BtnRemoveClicked(self):
        obj = getSelectedObject()
        if(obj):
            attribute = self.CmbAttr.currentText()
            RemoveExpr(obj, attribute)

    def BtnAssignClicked(self):
        obj = getSelectedObject()
        if(obj):
            attribute = self.CmbAttr.currentText()
            orgVal = cmds.getAttr(obj[0] + ".%s" % attribute)
            frequency = self.SpnFrequency.value()
            octaves = self.SpnOctaves.value()
            lacunarity = self.SpnLacunarity.value()
            gain = self.SpnGain.value()
            strength = self.SpnStrength.value()
            strAbvZ = self.ChkStrAbvZero.checkState()

            expr = GenerateMel(obj, orgVal, attribute, frequency, octaves, lacunarity, gain, strength, strAbvZ)
            #delete the expression first if exist
            RemoveExpr(obj, attribute)
            #create the expression
            exprName = "%s.%s_noise" %(obj[0], attribute)
            cmds.expression(s = expr, n=exprName, ae=1, uc = "all")

    def BtnRefreshAttrClicked(self):
        obj = getSelectedObject()
        if(obj):
            self.loadObjAttribs(obj)

    def CmbAttrCurrentIndexChanged(self, value):
        obj = getSelectedObject()
        if(obj):
            self.updateTitle(obj, value)

def main():
    obj = getSelectedObject()
    if(obj):
        global NoiseControllerMainWindow

        try:
            NoiseControllerMainWindow.close()
        except:
            pass

        NoiseControllerMainWindow = MainWindow()

        NoiseControllerMainWindow.loadObjAttribs(obj)

        NoiseControllerMainWindow.show()

#script start
main()
