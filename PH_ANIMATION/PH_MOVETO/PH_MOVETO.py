# -*- encoding: utf-8 -*-
import maya.cmds as mc
global sel
global winD
global win
winD='winDel'
win='PH_MOVETO'
sel=[]
def moveTo():
    global sel
    sel=mc.ls(sl=1,type='transform')
    transforms={}
    transforms['trf']=('tx','ty','tz')
    transforms['rot']=('rx','ry','rz')
    transforms['scl']=('sx','sy','sz')
    trf=[]
    rot=[]
    scl=[]
    if sel:
        if mc.nodeType(sel[0])=='transform':
            if len(sel)==2:
                #get attr del primer objeto
                for t in transforms['trf']:
                    trf.append(mc.getAttr(sel[0]+'.'+t))
                    mc.setAttr(sel[0]+'.'+t,lock=False)
                for r in transforms['rot']:
                    rot.append(mc.getAttr(sel[0]+'.'+r))
                    mc.setAttr(sel[0]+'.'+r,lock=False)
                for s in transforms['scl']:
                    scl.append(mc.getAttr(sel[0]+'.'+s))
                    mc.setAttr(sel[0]+'.'+s,lock=False)
                    #set attr del segundo objeto
                try:
                    mc.setAttr(sel[1]+'.tx',float(format(trf[0],'.3f')))
                    mc.setAttr(sel[1]+'.ty',float(format(trf[1],'.3f')))
                    mc.setAttr(sel[1]+'.tz',float(format(trf[2],'.3f')))
                    mc.setAttr(sel[1]+'.rx',float(format(rot[0],'.3f')))
                    mc.setAttr(sel[1]+'.ry',float(format(rot[1],'.3f')))
                    mc.setAttr(sel[1]+'.rz',float(format(rot[2],'.3f')))
                    mc.setAttr(sel[1]+'.sx',float(format(scl[0],'.3f')))
                    mc.setAttr(sel[1]+'.sy',float(format(scl[1],'.3f')))
                    mc.setAttr(sel[1]+'.sz',float(format(scl[2],'.3f')))
                    winDel()
                except:
                    print mc.warning(('No todo se pudo.').upper())
            else:
                print mc.warning(('Selecciona solo dos objetos.').upper())
        else:
            print mc.warning(('Eleji un transform.').upper())
    else:
        print mc.warning(('No hay nada seleccionado.').upper())
def delTRF():
    global sel
    mc.delete(sel[0])
    closewins()
def winDel():
    global winD
    if mc.window (winD,q=1, ex=1):
        mc.deleteUI (winD)
    mc.window(winD,title='¿DESEA BORRAR EL VIEJO TRF?',widthHeight=(200, 55),toolbox=1)
    mc.rowLayout( numberOfColumns=3,columnWidth3=(80, 75, 150),columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )
    mc.button(label='YES',command='PH_MOVETO.delTRF()',bgc=(0.6,0.0,0.0))
    mc.button(label='NO',command='PH_MOVETO.closewins()' )
    mc.showWindow(winD)
def closewins():
    mc.deleteUI(winD)
    mc.deleteUI(win)
def winMoveTo():
    global win
    version=' v0.1'
    if mc.window (win,q=1, ex=1):
        mc.deleteUI (win)
    mc.window(win,title=win+version,widthHeight=(260, 80),toolbox=1,s=0)
    mc.columnLayout( adjustableColumn=True )
    mc.text('1-SELECCIONA EL TRF VIEJO'+'\n\n'+'2-SELECCIONA EL TRF NUEVO'+'\n')
    mc.button(label='MOVE',command='PH_MOVETO.moveTo()',bgc=(0.5,0.6,0.3))
    mc.showWindow(win)