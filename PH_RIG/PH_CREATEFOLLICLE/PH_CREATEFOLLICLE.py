import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def createFollicle (pos=[0, 0, 0], nurbs_surface=None, poly_surface=None, name=''):

    if (nurbs_surface==None and poly_surface==None):
        OpenMaya.displayError("Function createFollicle() needs a nurbs surface or poly surface")
        return

    transform_node = cmds.createNode("transform", n=name+"__TRF")
    cmds.setAttr((transform_node +".tx"), pos[0])
    cmds.setAttr((transform_node +".ty"), pos[1])
    cmds.setAttr((transform_node +".tz"), pos[2])

    #make vector product nodes to get correct rotation of the transform node
    vector_product = cmds.createNode("vectorProduct", n=name+'__NVP')
    cmds.setAttr((vector_product+".operation"), 4)
    cmds.connectAttr( (transform_node+".worldMatrix"), (vector_product+".matrix"), f=1)
    cmds.connectAttr( (transform_node+".rotatePivot"), (vector_product+".input1"), f=1)

    #connect the correct position to a closest point on surface node created
    if nurbs_surface:
        closest_position = cmds.createNode("closestPointOnSurface", n=name+"__CPOS")
        cmds.connectAttr( (nurbs_surface+".ws"), (closest_position+".is"), f=1)
        cmds.connectAttr( (vector_product+".output"), (closest_position+".inPosition"), f=1)

    if poly_surface:
        closest_position = cmds.createNode("closestPointOnMesh", n=name+"__CPOS")
        cmds.connectAttr( (poly_surface+".outMesh"), (closest_position+".im"), f=1)
        cmds.connectAttr( (vector_product+".output"), (closest_position+".inPosition"), f=1)

    #create a follicle node and connect it
    follicle_transform = cmds.createNode("transform", n=name+"__FOL")
    follicle = cmds.createNode("follicle", n=name+"__FOLSP", p=follicle_transform)
    cmds.connectAttr((follicle+".outTranslate"), (follicle_transform+".translate"), f=1)
    cmds.connectAttr((follicle+".outRotate"), (follicle_transform+".rotate"), f=1)
    if nurbs_surface:
        cmds.connectAttr((nurbs_surface+".local"), (follicle+".is"), f=1)
        cmds.connectAttr((nurbs_surface+".worldMatrix[0]"), (follicle+".inputWorldMatrix"), f=1)
    if poly_surface:
        cmds.connectAttr((poly_surface+".outMesh"), (follicle+".inm"), f=1)
        cmds.connectAttr((poly_surface+".worldMatrix[0]"), (follicle+".inputWorldMatrix"), f=1)

    cmds.setAttr((follicle+".parameterU"), cmds.getAttr (closest_position+".parameterU"))
    cmds.setAttr((follicle+".parameterV"), cmds.getAttr (closest_position+".parameterV"))

    #return strings
    cmds.delete(transform_node)
    return [follicle_transform, follicle, closest_position]

def createFollicles  (follicle_positions=[[0,0,0]], nurbs_surface=None, poly_surface=None):

    out_follicles=list()

    if (nurbs_surface==None and poly_surface==None):
        OpenMaya.displayError("Function createFollicles() needs a nurbs surface or poly surface")
        return

    for pos in follicle_positions:
        lst = createFollicle(pos, nurbs_surface, poly_surface)
        out_follicles.append(lst)
    return out_follicles
def starFollicle():
    sel=[]
    sel = cmds.ls(sl=1, fl=1)
    for obj in sel:
        pos = cmds.pointPosition(obj, w=1)
        follicle = createFollicle(pos, poly_surface = obj.split('.')[0],name=str(obj.split('.')[0].split('__')[0]))
        print follicle
