import maya.mel as mel
import os.path

_version = "5.1"


def seithWeightsLoad(directory=None, method=None, spaceChoice=None):
    mel.eval('global string $gMainWindow')

    if directory is None:
        directory = mel.eval('textFieldButtonGrp -q -label swtTextFieldTFBG')
    if method is None:
        if mel.eval('radioButton -q -sl pointNumberLoadRB'):
            method = "Number"
        else:
            method = "Position"
    if spaceChoice is None:
        if mel.eval('radioButton -q -sl swtGlobalRB'):
            spaceChoice = "worldSpace"
        else:
            spaceChoice = "objectSpace"

    # Get the current selection.
    sel = mel.eval('ls -l -sl')

    if sel is None:
        print "Nothing is selected!"
        return

    for i in range( 0, len(sel) ):
        sel[i] = sel[i].encode("ascii","ignore")

    # geometriesInfo = [longTransformName, shortTransformName, longShapeName, skinCluster]
    geometriesInfo = []
    notSkins = []
    for s in sel:
        skinCluster = mel.eval('findRelatedSkinCluster("' + s + '")')
        shape = mel.eval('listRelatives -f -s ' + s)[0]
        geometriesInfo.append((s, s.split('|')[-1], shape, skinCluster))

    if geometriesInfo is not None:
        # Close the editors windows to make things faster.
        scriptEditorWasOpen = mel.eval('window -exists scriptEditorPanel1Window')
        textureEditorWasOpen = mel.eval('window -exists polyTexturePlacementPanel1Window')
        if scriptEditorWasOpen:
            mel.eval('catch(`deleteUI scriptEditorPanel1Window`)')
        if textureEditorWasOpen:
            mel.eval('catch(`deleteUI polyTexturePlacementPanel1Window`)')

        for c in xrange(0, len(geometriesInfo)):
            if os.path.exists(directory + '/' + geometriesInfo[c][1] + "_by" + method + ".mel"):
                # doLoadWeights(fileName, skinCluster, shapeName, method, number, totalNumber, threshold)
                doLoadWeights(directory + '/' + geometriesInfo[c][1] + "_by" + method + ".mel", geometriesInfo[c][3], geometriesInfo[c][2], method, c+1, len(geometriesInfo), None)
            else:
                #mel.eval('error "seithWeightTools: Cannot open file ' + directory + '/' + geometriesInfo[c][1] + "_by" + method + ".mel\"")
                print "seithWeightTools: Can not find file \"" + directory + '/' + geometriesInfo[c][1] + "_by" + method + ".mel"

        # Re-open the editors if they were open in the first place.
        if scriptEditorWasOpen:
             mel.eval('ScriptEditor')
        if textureEditorWasOpen:
             mel.eval('TextureViewWindow')

    # Output a summary.
    if len(notSkins):
        print "\n---------------------------\n seithLoadWeights Summary:\n---------------------------"
        for ns in notSkins:
            print 'Could not load weights for "' + ns + '" --> Not a skin!'
        mel.eval('confirmDialog -title "seithLoadWeights" -message "The operation ended with some errors. Please see the Script Editor for details... " -parent $gMainWindow  -button "Close"')
    else:
        mel.eval('print "seithWeightsLoad ended successfully!"')

    mel.eval('select -r ' + (' '.join(sel)))


def doLoadWeights(fileName=None, skinCluster=None, shapeName=None, method=None, number=None, totalNumber=None, threshold=None):
    # Open weight file.
    f = open(fileName, "r")
    allLines = []
    if os.path.exists(fileName):
        allLines = f.readlines()
    else:
        #mel.eval('progressWindow -endProgress')
        mel.eval('deleteUI swtProgressWindow')
        mel.eval('error "seithWeightTools: Cannot open file ' + fileName)

    # Setting up the progress window.
    #mel.eval('progressWindow -title "' + shapeName + ' - ' + str(number) + ' of ' + str(totalNumber) + '" -progress 0 -min 0 -max 100 -status "0 %" -isInterruptable true')
    progressWindow = 'window -wh 300 50 -title "' + shapeName.split("|")[-1] + ' - ' + str(number) + ' of ' + str(totalNumber) + '" swtProgressWindow; \
        columnLayout -adj true -p swtProgressWindow swtProgressWindowColumn; \
        separator -h 4 -style "none" -p swtProgressWindowColumn; \
        text -l "Loading Weights" -p swtProgressWindowColumn swtProgressWindowText; \
        separator -h 4 -style "none" -p swtProgressWindowColumn; \
        progressBar -progress 1 -min 0 -max 100 -width 200 -isInterruptable true -p swtProgressWindowColumn swtProgressBar; \
        showWindow swtProgressWindow'
    mel.eval(progressWindow)
    amount = 0

    # If the mesh is not a skin, then bind it using the joints in the weights file.
    if skinCluster == '':
        listOfJoints = allLines[0][allLines[0].find(':')+1:]
        mel.eval('select -r ' + shapeName + ' ' + listOfJoints)
        skinCluster = mel.eval('skinCluster -toSelectedBones -ignoreHierarchy -mi 4 -dr 5')[0]

    # Get rid of the first line (the one mentionning the joints).
    allLines.pop(0)

    if method == "Number":
        amountStep = 100.0 / (len(allLines))

        # Apply the weights.
        for line in allLines:
            if mel.eval('progressBar -query -isCancelled swtProgressBar'):
                break

            # Simply Replace "$skincl" with the real skinCluster and execute the line.
            command = line.replace("$skincl", skinCluster)
            mel.eval('catchQuiet(`eval ("' + command[:-2] + '")`)')

            # Update the Maya progress window.
            amount += amountStep
            #mel.eval('progressWindow -edit -progress ' + str(int(amount)) + ' -status "Load weights by ' + method + ' - ' + str(int(amount)) + ' %"')
            mel.eval('text -edit -label "Load weights by ' + method + ' - ' + str(int(amount)) + ' %" swtProgressWindowText')
            mel.eval('progressBar -edit -progress ' + str(int(amount)) + ' swtProgressBar')

    elif method == "Position":
        amountStep = 100.0 / (len(allLines)/3)

        geometryType = mel.eval('ls -st ' + shapeName)

        # Select all the points.
        if geometryType[1] == "nurbsSurface":
            numberOfSpansTmp = mel.eval('getAttr ' + shapeName + '.spansUV')
            mel.eval('select -r ' + shapeName + '.cv[0:' + str(numberOfSpansTmp[1]+2) + '][0:' + str(numberOfSpansTmp[0]) + ']')
        elif geometryType[1] == "mesh":
            numberOfVtxs = mel.eval('polyEvaluate -v ' + shapeName)
            mel.eval('select -r ' + shapeName + '.vtx[0:' + str(numberOfVtxs[0]) + ']')

        # Get the list of points as an expanded selection (each point is individually selected, instead of toto.vtx[0:500]).
        pointsSelection = mel.eval('ls -fl -sl')

        points = []
        weights = []
        xpos = []
        ypos = []
        zpos = []

        for line in allLines:
            if mel.eval('progressBar -query -isCancelled swtProgressBar'):
                break

            if line.find("[") != -1:
                # Get the next point name.
                points.append(line.strip())

            elif line.find("-tv") != -1:
                # Get the weights string.
                weights.append(line.strip()) #print ("\n$weights[$totalv] = " + $weights[`size $verts`]);

            else:
                # Get the point position.
                posTmp = line.strip().split()
                xpos.append(float(posTmp[0]))
                ypos.append(float(posTmp[1]))
                zpos.append(float(posTmp[2]))

        # At this point we have a list of the original points, weighting and pos and the current set of selected vertices.
        for c in xrange(0, len(pointsSelection)):
            if mel.eval('progressBar -query -isCancelled swtProgressBar'):
                break

            # Update the Maya progress window.
            amount += amountStep
            #mel.eval('progressWindow -edit -progress ' + str(int(amount)) + ' -status "Load weights by ' + method + ' - ' + str(int(amount)) + ' %"')
            mel.eval('text -edit -label "Load weights by ' + method + ' - ' + str(int(amount)) + ' %" swtProgressWindowText')
            mel.eval('progressBar -edit -progress ' + str(int(amount)) + ' swtProgressBar')

            # Get current point position.
            pointPosition = []

            if mel.eval('radioButton -q -sl swtGlobalRB'):
                pointPosition = mel.eval('pointPosition -w ' + pointsSelection[c])
            else:
                pointPosition = mel.eval('pointPosition -l ' + pointsSelection[c])

            # Now store distance from each saved vert.
            delta = []

            for d in xrange(0, len(pointsSelection)):
                delta.append((
                abs(pointPosition[0]-xpos[d]) +
                abs(pointPosition[1]-ypos[d]) +
                abs(pointPosition[2]-zpos[d]) ) / 3)

            # Now figure which one is closest. By default matches first one.
            isMatch = 0
            mindelta = delta[0]

            for d in xrange(0, len(pointsSelection)):
                if delta[d] < mindelta:
                    # Found a closer match?
                    isMatch = d;
                    mindelta = delta[d]

            # Finally if it is within threshold, load new weights!
            if threshold is None:
                if mel.eval('floatField -q -ex swtThreshFieldFF'):
                    threshold = mel.eval('floatField -q -v swtThreshFieldFF')
                else:
                    threshold = 0.001

            # Found a close enough match!
            if pointPosition[0] < (xpos[isMatch]+threshold) and \
                pointPosition[0] > (xpos[isMatch]-threshold) and \
                pointPosition[1] < (ypos[isMatch]+threshold) and \
                pointPosition[1] > (ypos[isMatch]-threshold) and \
                pointPosition[2] < (zpos[isMatch]+threshold) and \
                pointPosition[2] > (zpos[isMatch]-threshold):
                command = "skinPercent " + weights[isMatch] + " " + skinCluster + " " + pointsSelection[c]
                mel.eval('catchQuiet(`eval (\"' + command + '\")`)')
                print "Point " + pointsSelection[c] + " matches old vertex " + points[isMatch]
            else:
                print "Point " + pointsSelection[c] + " is not within threshold enough to match " + points[isMatch] + " so no action taken."

    #mel.eval('progressWindow -endProgress')
    mel.eval('deleteUI swtProgressWindow')
    f.close()

    # Re-enable weights normalization.
    mel.eval('if (("' + skinCluster + '.normalizeWeights") != ".normalizeWeights") setAttr ("' + skinCluster + '.normalizeWeights") true')


def seithWeightsSave(directory=None, methods=[], spaceChoice=None):
    mel.eval('global string $gMainWindow')
    mel.eval('waitCursor -state on')

    if directory is None:
        directory = mel.eval('textFieldButtonGrp -q -label swtTextFieldTFBG')
    if len(methods) == 0:
        if mel.eval('checkBox -q -v pointNumberSaveCB'):
            methods.append("Number")
        if mel.eval('checkBox -q -v pointPositionSaveCB'):
            methods.append("Position")
    if spaceChoice is None:
        if mel.eval('radioButton -q -sl swtGlobalRB'):
            spaceChoice = "worldSpace"
        else:
            spaceChoice = "objectSpace"

    # Get the current selection.
    sel = mel.eval('ls -l -sl')
    for i in range( 0, len(sel) ):
        sel[i] = sel[i].encode("ascii","ignore")

    # geometriesInfo = [longTransformName, shortTransformName, longShapeName, skinCluster]
    geometriesInfo = []
    rejects = []
    for s in sel:
        skinClusterTmp = mel.eval('findRelatedSkinCluster("' + s + '")')
        if skinClusterTmp != '':
            shapeTmp = mel.eval('listRelatives -f -s ' + s)[0]
            geometriesInfo.append((s, s.split('|')[-1], shapeTmp, skinClusterTmp))
        else:
            rejects.append(s.split('|')[-1])

    # Save the weights.
    if geometriesInfo is not None:
        yesToAll = False
        cancelAll = False

        #mel.eval('progressWindow -title "seithWeightsSave" -progress 0 -min 0 -max 100 -status "" -isInterruptable false')
        progressWindow = 'window -wh 300 50 -title "seithWeightsSave" swtProgressWindow; \
            columnLayout -adj true -p swtProgressWindow swtProgressWindowColumn; \
            separator -h 4 -style "none" -p swtProgressWindowColumn; \
            text -l "" -p swtProgressWindowColumn swtProgressWindowText; \
            separator -h 4 -style "none" -p swtProgressWindowColumn; \
            progressBar -progress 1 -min 0 -max 100 -width 200 -isInterruptable true -p swtProgressWindowColumn swtProgressBar; \
            showWindow swtProgressWindow'
        mel.eval(progressWindow)

        for c in xrange(0, len(geometriesInfo)):
            # Check if the file already exists.
            confirmedMethods = []
            for m in methods:
                if os.path.exists(directory + '/' + geometriesInfo[c][1] + "_by" + m + ".mel") and yesToAll == False:
                    result = mel.eval('confirmDialog -title "Confirm Save Weights by Point ' + m + '" -message "Overwrite the existing file: ' + directory + '/' + geometriesInfo[c][1] + '_by' + m + '.mel ?" -ma "center" -button "Yes" -button "No" -button "Yes to all" -button "Cancel" -defaultButton "Yes" -cancelButton "Cancel" -dismissString "No"')
                    if result == "Yes":
                        if len(confirmedMethods) < len(methods):
                            confirmedMethods.append(m)
                    elif result == "Yes to all":
                        if len(confirmedMethods) < len(methods):
                            confirmedMethods.append(m)
                        yesToAll = True
                        #break
                    elif result == "Cancel":
                        cancelAll = True
                        break
                else:
                    confirmedMethods.append(m)
            #print "confirmedMethods = " + str(confirmedMethods)

            if cancelAll:
                break
            elif len(confirmedMethods) >= 1:
                #mel.eval('progressWindow -edit -title "seithWeightsSave: ' + str(c+1) + ' of ' + str(len(geometriesInfo)) + '"')
                mel.eval('window -edit -title "seithWeightsSave: ' + str(c+1) + ' of ' + str(len(geometriesInfo)) + '" swtProgressWindow')
                #mel.eval('text -edit -label "Load weights by ' + method + ' - ' + str(int(amount)) + ' %" swtProgressWindowText')
                #mel.eval('progressBar -edit -progress ' + str(int(amount)) + ' swtProgressBar')
                doSaveWeights(directory, geometriesInfo[c], confirmedMethods, spaceChoice)

    # Finish up.
    mel.eval('select -cl')
    for s in sel:
        mel.eval('select -add ' + s)
    #mel.eval('progressWindow -endProgress')
    mel.eval('deleteUI swtProgressWindow')
    mel.eval('waitCursor -state off')

    # Output a summary.
    if len(rejects) and not cancelAll:
        print "\n---------------------------\n seithSaveWeights Summary:\n---------------------------"
        for r in rejects:
            print 'Could not save weights for "' + r + '" --> Not a skin!'
        mel.eval('confirmDialog -title "seithSaveWeights" -message "The operation ended with some errors. Please see the Script Editor for details... " -button "Close"')
    else:
        mel.eval('print "seithWeightsSave ended successfully!"')


def doSaveWeights(directory=None, geometriesInfo=None, methods=None, spaceChoice=None):
    # geometriesInfo = [longTransformName, shortTransformName, longShapeName, skinCluster]
    longName = geometriesInfo[0]
    shortName = geometriesInfo[1]
    longShapeName = geometriesInfo[2]
    skinCluster = geometriesInfo[3]

    # For every geometry, save the weights.
    mel.eval('select -r ' + longName)
    geoType = mel.eval('ls -sl -dag -s -showType ' + longName)[1]
    if geoType == "mesh":
        mel.eval('select -r "' + longName + '.vtx[*]"')
    elif geoType == "nurbsSurface":
        mel.eval('select -r "' + longName + '.cv[*][*]"')

    # Open the weights file.
    fileByNumber = None
    fileByPosition = None
    if "Number" in methods:
        fileByNumber = open(directory + '/' + shortName + "_byNumber.mel", "w")
    if "Position" in methods:
        fileByPosition = open(directory + '/' + shortName + "_byPosition.mel", "w")

    # Get the geometry's points.
    listOfPoints = mel.eval('ls -sl -fl')
    listOfJointsTmp = mel.eval('skinCluster -q -inf ' + skinCluster)
    listOfJoints = ''
    for j in listOfJointsTmp:
        listOfJoints += j.split("|")[-1].encode("ascii","ignore") + ' '

    if "Number" in methods:
        fileByNumber.write("// List of joints: " + listOfJoints + '\n')
    if "Position" in methods:
        fileByPosition.write("// List of joints: " + listOfJoints + '\n')

    # Set the Maya progress window.
    amountStep = 100.0 / len(listOfPoints)
    amount = 0
    #mel.eval('progressWindow -progress ' + str(int(amount)) + ' -status \"Starting...\"')
    mel.eval('text -edit -label "Starting..." swtProgressWindowText')
    mel.eval('progressBar -edit -progress ' + str(int(amount)) + ' swtProgressBar')

    # For every point, get the weighting info.
    for point in listOfPoints:
        # Get the influencing joints list.
        skinJoints = mel.eval('skinPercent -q -t ' + skinCluster + ' ' + point)
        skinJointTSM = []
        TSMON = False

        # This is added to work with Anzovin's the Setup Machine.
        #for jointTmp in skinJoints:
        #    if mel.eval('ls -type "joint" ' + jointTmp) is None:
        #        skinJointTSM.append(mel.eval('listConnections -s on -d off -type "joint" ' + jointTmp)[0])
        #        TSMON = True

        #if TSMON:
        #    skinJoints = skinJointTSM

        if skinJoints is not None:
            # And what are their skinPercent weights?
            weights = []
            for joint in skinJoints:
                weights.append(mel.eval('skinPercent -t ' + joint + ' -q ' + skinCluster + ' ' + point))

            # Write to the files.
            outputLine = []

            if "Number" in methods:
                outputLine.append("skinPercent")
                for c in xrange(0, len(skinJoints)):
                    outputLine.append("-tv " + skinJoints[c] + " " + "%f" % weights[c])

                # Note here we print the skinCluster as a variable ($skincl), that way we're not tied to a specific skinCluster name when we re-apply the weights.
                outputLine.append("$skincl " + point + ";\n")
                fileByNumber.write(' '.join(outputLine))

            if "Position" in methods:
                fileByPosition.write(point + "\n")
                pointPosTmp = []
                if spaceChoice == "worldSpace":
                    pointPosTmp = mel.eval('pointPosition -w ' + point)
                else:
                    pointPosTmp = mel.eval('pointPosition -l ' + point)
                pointPos = "%f" % pointPosTmp[0] + ' ' + "%f" % pointPosTmp[1] + ' ' + "%f" % pointPosTmp[2]
                fileByPosition.write(pointPos + "\n")
                jointsAsString = []
                for c in xrange(0, len(skinJoints)):
                    jointsAsString.append("-tv " + skinJoints[c] + ' ' + "%f" % weights[c])
                fileByPosition.write(' '.join(jointsAsString) + "\n")

        else:
            print "Could not find any joint influence for point " + point

        # Update the Maya progress window.
        amount += amountStep
        #mel.eval('progressWindow -edit -progress ' + str(int(amount)) + ' -status \"' + point + '\"')
        mel.eval('text -edit -label "' + point + '" swtProgressWindowText')
        mel.eval('progressBar -edit -progress ' + str(int(amount)) + ' swtProgressBar')

    print skinJoints

    # Close the weights file.
    if "Number" in methods:
        fileByNumber.close()
    if "Position" in methods:
        fileByPosition.close()