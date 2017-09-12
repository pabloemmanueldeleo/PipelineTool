import maya.cmds as mc

def selSh():
    sel = mc.ls(type = 'aiStandard') + mc.ls(type = 'lambert')
    if sel:
        #Si el nodo existe, lo borro de la lista.
        if 'lambert1' in sel:
            #Lo busco en la lista
            indexNodo = sel.index('lambert1')
            del sel[indexNodo]
        mc.select(sel)
        mc.warning('Se seleccionaron : ' + str(sel))
    else:
        mc.warning('No pude seleccionar perdon')
    return sel