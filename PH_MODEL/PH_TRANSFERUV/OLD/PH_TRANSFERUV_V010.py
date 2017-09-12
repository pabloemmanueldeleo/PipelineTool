def uvTranfer(mesh_source,mesh_target):

    import maya.mel as mel

    # Usually the original mesh before skinning has been renamed as *Orig
    # and hidden
    cmds.select(mesh_target, replace=True)
    mesh_orig = cmds.listRelatives(mesh_target)[1]
    #mesh_orig = cmds.listHistory('*Orig')[0]
    
    print 'Mesh Source (with UV) :', mesh_source
    print 'Mesh Target (skinned mesh):', mesh_target
    print 'Mesh Original:', mesh_orig
    
    # Toggle OFF the Intermediate Object option box
    cmds.select(mesh_orig, replace=True)
    cmds.setAttr("{mesh_orig}.intermediateObject".format(mesh_orig=mesh_orig), False);
    cmds.select(clear=True)
    
    # Transfer UV using Transfer Attribute Command
    cmds.select(mesh_source, replace=True)
    cmds.select(mesh_orig, toggle=True)
    
    print('selecting...', mesh_source, mesh_orig)
    
    cmds.transferAttributes(
            transferPositions=False,
            transferNormals=False,
            transferUVs=2,
            transferColors=2,
            sampleSpace=4,
            sourceUvSpace="map1",
            targetUvSpace="map1",
            searchMethod=3,
            flipUVs=False,
            colorBorders=True
        )
    
    
    # Delete Construction History of mesh_orig after we transfer the UV information
    cmds.select(mesh_orig, replace=True)
    cmds.delete(constructionHistory=True)
    cmds.select(clear=True)
    
    # Toggle ON the Intermediate Object option box
    cmds.select(mesh_orig, replace=True)
    cmds.setAttr("{mesh_orig}.intermediateObject".format(mesh_orig=mesh_orig), True);
    cmds.select(clear=True)
    
    # Return the selections as it was selected by user
    cmds.select(mesh_source, replace=True)
    cmds.select(mesh_target, toggle=True)
    
    # Process complete
    mel.eval('print ("RESULT: UV successfully transferred to skinned mesh, you are welcome.")')