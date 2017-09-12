import maya.cmds as mc
sel = mc.ls(sl=True)
for o in sel:# Mirror the piece
    if mc.nodeType(mc.listRelatives(o)[0])=='mesh':
        if mc.objExists(o+'_mirror')==False:
            mirroredGeo = ''
            mirroredGeo = mc.duplicate(o,n=o+'_mirror')[0]

            piv=mc.xform(mirroredGeo,q=1,piv=1)

            mc.xform(mirroredGeo, ws=True, piv=(0,0,0))
            mc.makeIdentity (mirroredGeo,translate=1,rotate=1,scale=True, apply=True)
            mc.setAttr (mirroredGeo +'.scaleX',-1)
            mc.makeIdentity (mirroredGeo,translate=1,rotate=1,scale=True, apply=True)
            mc.polyNormal (mirroredGeo, normalMode=0, userNormalMode=0)

            mc.xform(mirroredGeo, ws=True,centerPivots=1)
            if 'L_' in mirroredGeo:
                mc.rename(mirroredGeo, o.replace('L_','R_'))
            elif 'R_' in mirroredGeo:
                mc.rename(mirroredGeo, o.replace('R_','L_'))
            elif 'Left' in mirroredGeo:
                mc.rename(mirroredGeo, o.replace('Left','Right'))
            elif 'Right' in mirroredGeo:
                mc.rename(mirroredGeo, o.replace('Right','Left'))
            elif 'Mid' or 'C_' or 'mid' in mirroredGeo or None == mirroredGeo:
                mc.polyUnite(o, mirroredGeo, name=str(o), constructionHistory=1, mergeUVSets=1,caching=True)
                mc.delete(mirroredGeo,ch = True)
                mc.rename(mirroredGeo,str(o))
