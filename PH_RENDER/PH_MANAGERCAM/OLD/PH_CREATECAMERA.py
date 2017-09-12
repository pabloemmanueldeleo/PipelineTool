# -*- encoding: utf-8 -*-
# 28/07/2015
# crea rig stereo con nombre
import maya.cmds as cmds
import maya.mel as mel
import sys


def renombrado(escenaplano=''):
    cmds.rename('C_E999_P00__GRP', 'C_' + escenaplano + '__GRP')
    cmds.rename('C_E999_P00__CNTSH', "C_" + escenaplano + "__CNTSH")
    cmds.rename('C_E999_P00__TRF', "C_" + escenaplano + "__TRF")
    cmds.rename('L_E999_P00__CAM', "L_" + escenaplano + "__CAM")
    cmds.rename('L_E999_P00__HCNS', "L_" + escenaplano + "__HCNS")
    cmds.rename('R_E999_P00__CAM', "R_" + escenaplano + "__CAM")
    cmds.rename('R_E999_P00__HCNS', "R_" + escenaplano + "__HCNS")
    cmds.rename('C_E999_P00__CNT', "C_" + escenaplano + "__CNT")
    cmds.rename('C_E999_P00_SCAM', "C_" + escenaplano + "_SCAM")
    cmds.rename('L_E999_P00_SCAM', "L_" + escenaplano + "__SCAM")
    cmds.rename('R_E999_P00_SCAM', "R_" + escenaplano + "__SCAM")
    cmds.rename('C_E999_P00__HCNS', "C_" + escenaplano + "__HCNS")


# mover camara
def getSetCam(nCam=''):
    # nCam='E000_P00'
    nCam = 'C_' + nCam + '__CNT'
    sel = cmds.ls(sl=1, type='transform')
    if sel:
        transforms = {}
        transforms['trf'] = ('tx', 'ty', 'tz')
        transforms['rot'] = ('rx', 'ry', 'rz')
        trf = []
        rot = []
        for t in transforms['trf']:
            trf.append(cmds.getAttr(sel[0] + '.' + t))
            cmds.setAttr(sel[0] + '.' + t, lock=False)
        for r in transforms['rot']:
            rot.append(cmds.getAttr(sel[0] + '.' + r))
            cmds.setAttr(sel[0] + '.' + r, lock=False)
        # set attr del segundo objeto
        try:
            cmds.setAttr(nCam + '.tx', float(format(trf[0], '.3f')))
            cmds.setAttr(nCam + '.ty', float(format(trf[1], '.3f')))
            cmds.setAttr(nCam + '.tz', float(format(trf[2], '.3f')))
            cmds.setAttr(nCam + '.rx', float(format(rot[0], '.3f')))
            cmds.setAttr(nCam + '.ry', float(format(rot[1], '.3f')))
            cmds.setAttr(nCam + '.rz', float(format(rot[2], '.3f')))
        except:
            print cmds.warning(('Puede que no alla puesto bien la camara revisala.').upper())
    else:
        cmds.warning(('Se creo en el zero del mundo.').upper())


# LOCKEO
def lockeado(escenaplano=''):
    cmds.setAttr("C_" + escenaplano + "__CNT.INTERAXIAL", l=1)
    cmds.setAttr("C_" + escenaplano + "__CNT.ZEROP", l=1)
    cmds.setAttr("C_" + escenaplano + "__CNT.CONVERGENCE", l=1)
    cmds.setAttr("C_" + escenaplano + "__CNT.FocalLenght", l=1)
    cmds.setAttr("C_" + escenaplano + "__CNT.NearClip", l=1)
    cmds.setAttr("C_" + escenaplano + "__CNT.FarClip", l=1)


def importarRig(esc=000, pla=00):
    # esc=000
    # pla=00
    if (esc > 999) or (pla > 99):
        cmds.warning('REVISAR VALORES. UNO O AMBOS EXCEDEN EL LIMITE')
    else:
        esc = u'%03d' % esc
        pla = u'%02d' % pla
        EXXX_PXX = str('E' + esc + '_P' + pla)
        if cmds.objExists('C_' + EXXX_PXX + '__GRP'):
            cmds.warning('Ya existe el grupo en la escena. Borralo o crea otro.')
        else:
            sel = cmds.ls(sl=1, type='transform')
            cmds.file("M:/PH_SCRIPTS/SCENES_RIG/IMPORTRIGS/rig_esterocam_final.ma", i=1, type='mayaAscii',
                      namespace=':', options='v=0')
            if sel:
                cmds.select(sel[0])
            renombrado(EXXX_PXX)
            getSetCam(EXXX_PXX)
            lockeado(EXXX_PXX)
