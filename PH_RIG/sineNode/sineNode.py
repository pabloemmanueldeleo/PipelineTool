#SineNode v1.0


import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import math, random
import maya.cmds as cmds

kPluginNodeTypeName = "sineNode"
kPluginNodeId = OpenMaya.MTypeId(0x8723)

class sineNode(OpenMayaMPx.MPxNode):
	aInput = OpenMaya.MObject()
	aOutput = OpenMaya.MObject()
	
	aAmplitude = OpenMaya.MObject()
	aFrequency = OpenMaya.MObject()
	aOffset = OpenMaya.MObject()
	
	def __init__(self):
		#print "> sineNode.init"
		OpenMayaMPx.MPxNode.__init__(self)
	
	def compute(self, plug, block):
		#print "> compute"
		
		inputValue = block.inputValue(sineNode.aInput).asFloat()
		amplitudeValueX = block.inputValue(sineNode.aAmplitudeX).asFloat()
		frequencyValueX = block.inputValue(sineNode.aFrequencyX).asFloat()
		amplitudeValueY = block.inputValue(sineNode.aAmplitudeY).asFloat()
		frequencyValueY = block.inputValue(sineNode.aFrequencyY).asFloat()
		amplitudeValueZ = block.inputValue(sineNode.aAmplitudeZ).asFloat()
		frequencyValueZ = block.inputValue(sineNode.aFrequencyZ).asFloat()
		
		noiseFlag = block.inputValue(sineNode.aNoise).asInt()
		
		outputData = block.outputValue(sineNode.aOutput)
		
		if (noiseFlag == 0):
			resultX = math.sin(inputValue * frequencyValueX) * amplitudeValueX 
			resultY = math.sin(inputValue * frequencyValueY) * amplitudeValueY 
			resultZ = math.sin(inputValue * frequencyValueZ) * amplitudeValueZ
		if (noiseFlag == 1):
			#if frequency is 1, the noise doesn't work, hence the 101, so it's unlikely anyone will manage to make the frequency exactly 1 now.
			resultX = improvedGradNoise( inputValue*(frequencyValueX*0.101), inputValue*(frequencyValueX*0.101), inputValue*(frequencyValueX*0.101) ) * amplitudeValueX
			resultY = improvedGradNoise( inputValue*(frequencyValueY*0.101)+250, inputValue*(frequencyValueY*0.101)+250, inputValue*(frequencyValueY*0.101)+250 ) * amplitudeValueY 
			resultZ = improvedGradNoise( inputValue*(frequencyValueZ*0.101)+500, inputValue*(frequencyValueZ*0.101)+500, inputValue*(frequencyValueZ*0.101)+500 ) * amplitudeValueZ

		outputData.set3Float(resultX,resultY,resultZ)
		
		block.setClean(plug)
		
		return OpenMaya.MStatus.kSuccess


def nodeCreator():
	#print "> nodeCreator"
	#myNode = maya.cmds.createNode("sineNode")
	#cmds.connectAttr("time1.outTime", myNode + ".input")
	return OpenMayaMPx.asMPxPtr( sineNode() )
	
def nodeInitializer():
	#print "> nodeInitializer"
	
	nAttr = OpenMaya.MFnNumericAttribute()
	
	sineNode.aInput = nAttr.create("input", "in", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(-10)
	nAttr.setSoftMax(10)
	
	sineNode.aAmplitudeX = nAttr.create("amplitudeX", "ampX", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(-20)
	nAttr.setSoftMax(20)
	
	sineNode.aFrequencyX = nAttr.create("frequencyX", "freqX", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(2)
	
	sineNode.aAmplitudeY = nAttr.create("amplitudeY", "ampY", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(-20)
	nAttr.setSoftMax(20)
	
	sineNode.aFrequencyY = nAttr.create("frequencyY", "freqY", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(2)
	
	sineNode.aAmplitudeZ = nAttr.create("amplitudeZ", "ampZ", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(-20)
	nAttr.setSoftMax(20)
	
	sineNode.aFrequencyZ = nAttr.create("frequencyZ", "freqZ", OpenMaya.MFnNumericData.kFloat, 1)
	nAttr.setSoftMin(0)
	nAttr.setSoftMax(2)
	
	sineNode.aOutput = nAttr.create("output", "out", OpenMaya.MFnNumericData.k3Float)
	nAttr.setWritable(False)
	
	# boolean attr
	#booleanAttr = OpenMaya.MFnNumericAttribute()
	sineNode.aNoise = nAttr.create("noise", "ba", OpenMaya.MFnNumericData.kBoolean)
	nAttr.setHidden(False)
	nAttr.setKeyable(False)
	
	sineNode.addAttribute( sineNode.aNoise )
	sineNode.addAttribute( sineNode.aInput )
	sineNode.addAttribute( sineNode.aOutput )
	sineNode.addAttribute( sineNode.aAmplitudeX )
	sineNode.addAttribute( sineNode.aFrequencyX )
	sineNode.addAttribute( sineNode.aAmplitudeY )
	sineNode.addAttribute( sineNode.aFrequencyY )
	sineNode.addAttribute( sineNode.aAmplitudeZ )
	sineNode.addAttribute( sineNode.aFrequencyZ )

	
	sineNode.attributeAffects( sineNode.aNoise, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aInput, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aAmplitudeX, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aFrequencyX, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aAmplitudeY, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aFrequencyY, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aAmplitudeZ, sineNode.aOutput)
	sineNode.attributeAffects( sineNode.aFrequencyZ, sineNode.aOutput)


	#connect the node to time
	#OpenMaya.MGlobal.executeCommand( "connectAttr -f time1.outTime sineNode1.input;" );

	#myNode = getNode();
	

def createSinNode(transform=None):
	sineNode = cmds.createNode("sineNode")
	cmds.connectAttr("time1.outTime", "%s.input" % sineNode)
	
	return sineNode

def initializePlugin(mobject):
	#print "> initializePlugin"
	fnPlugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		fnPlugin.registerNode(kPluginNodeTypeName, kPluginNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kDependNode)
	except:
		sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )


def uninitializePlugin(mobject):
	#print "> uninitializePlugin"
	fnPlugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		fnPlugin.deregisterNode(kPluginNodeId)
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
		
#createSinNode()

# Ken's permutation array composed of 512 elements = 2 sets of (0,255)
p = [151,160,137, 91, 90, 15,131, 13,201, 95, 96, 53,194,233,  7,225,
	 140, 36,103, 30, 69,142,  8, 99, 37,240, 21, 10, 23,190,  6,148,
	 247,120,234, 75,  0, 26,197, 62, 94,252,219,203,117, 35, 11, 32,
	  57,177, 33, 88,237,149, 56, 87,174, 20,125,136,171,168, 68,175,
	  74,165, 71,134,139, 48, 27,166, 77,146,158,231, 83,111,229,122,
	  60,211,133,230,220,105, 92, 41, 55, 46,245, 40,244,102,143, 54,
	  65, 25, 63,161,  1,216, 80, 73,209, 76,132,187,208, 89, 18,169,
	 200,196,135,130,116,188,159, 86,164,100,109,198,173,186,  3, 64,
	  52,217,226,250,124,123,  5,202, 38,147,118,126,255, 82, 85,212,
	 207,206, 59,227, 47, 16, 58, 17,182,189, 28, 42,223,183,170,213,
	 119,248,152,  2, 44,154,163, 70,221,153,101,155,167, 43,172,  9,
	 129, 22, 39,253, 19, 98,108,110, 79,113,224,232,178,185,112,104,
	 218,246, 97,228,251, 34,242,193,238,210,144, 12,191,179,162,241,
	  81, 51,145,235,249, 14,239,107, 49,192,214, 31,181,199,106,157,
	 184, 84,204,176,115,121, 50, 45,127,  4,150,254,138,236,205, 93,
	 222,114, 67, 29, 24, 72,243,141,128,195, 78, 66,215, 61,156,180,
	 151,160,137, 91, 90, 15,131, 13,201, 95, 96, 53,194,233,  7,225,
	 140, 36,103, 30, 69,142,  8, 99, 37,240, 21, 10, 23,190,  6,148,
	 247,120,234, 75,  0, 26,197, 62, 94,252,219,203,117, 35, 11, 32,
	  57,177, 33, 88,237,149, 56, 87,174, 20,125,136,171,168, 68,175,
	  74,165, 71,134,139, 48, 27,166, 77,146,158,231, 83,111,229,122,
	  60,211,133,230,220,105, 92, 41, 55, 46,245, 40,244,102,143, 54,
	  65, 25, 63,161,  1,216, 80, 73,209, 76,132,187,208, 89, 18,169,
	 200,196,135,130,116,188,159, 86,164,100,109,198,173,186,  3, 64,
	  52,217,226,250,124,123,  5,202, 38,147,118,126,255, 82, 85,212,
	 207,206, 59,227, 47, 16, 58, 17,182,189, 28, 42,223,183,170,213,
	 119,248,152,  2, 44,154,163, 70,221,153,101,155,167, 43,172,  9,
	 129, 22, 39,253, 19, 98,108,110, 79,113,224,232,178,185,112,104,
	 218,246, 97,228,251, 34,242,193,238,210,144, 12,191,179,162,241,
	  81, 51,145,235,249, 14,239,107, 49,192,214, 31,181,199,106,157,
	 184, 84,204,176,115,121, 50, 45,127,  4,150,254,138,236,205, 93,
	 222,114, 67, 29, 24, 72,243,141,128,195, 78, 66,215, 61,156,180]

# Ken's Utility functions for noise
# linear interpolation
def lerp(parameter=0.5,value1=0.0,value2=1.0):
	return value1 + parameter * (value2 - value1)

# Ken's new spline interpolation
def fade(parameter=1.0):
	return parameter*parameter*parameter*(parameter*(parameter*6.0 - 15.0) + 10.0)

# Ken's new function to return gradient values
# based on bit operations on hashId
def grad(hashId=255,x=1.0,y=1.0,z=1.0):
	h = hashId & 15
	if (h < 8):
		u = x
	else:
		u = y
		
	if (h < 4):
		v = y
	elif (h==12 or h==14):
		v = x
	else:
		v = z
	if ((h&1)!=0):
		u = -u
	if ((h&2)!=0):
		v = -v
	return u + v

# Ken's improved gradient noise function
def improvedGradNoise(vx=1.0,vy=1.0,vz=1.0):
	# get integer lattice values for sample point position
	X = int(math.floor(vx)) & 255
	Y = int(math.floor(vy)) & 255
	Z = int(math.floor(vz)) & 255
	# fractional part of point position
	vx -= math.floor(vx)
	vy -= math.floor(vy)
	vz -= math.floor(vz)
	# interpolate fractional part of point position
	u = fade(vx)
	v = fade(vy)
	w = fade(vz)
	# new hash integer lattice cell coords onto perm array
	A = p[X]+Y
	B = p[X+1]+Y
	AA = p[A]+Z
	BA = p[B]+Z
	AB = p[A+1]+Z
	BB = p[B+1]+Z
	# new hash onto gradients
	gradAA  = grad(p[AA],   vx,     vy,     vz  )
	gradBA  = grad(p[BA],   vx-1.0, vy,     vz  )
	gradAB  = grad(p[AB],   vx,     vy-1.0, vz  )
	gradBB  = grad(p[BB],   vx-1.0, vy-1.0, vz  )
	gradAA1 = grad(p[AA+1], vx,     vy,     vz-1.0)
	gradBA1 = grad(p[BA+1], vx-1.0, vy,     vz-1.0)
	gradAB1 = grad(p[AB+1], vx,     vy-1.0, vz-1.0)
	gradBB1 = grad(p[BB+1], vx-1.0, vy-1.0, vz-1.0)
	# trilinear intropolation of resulting gradients to sample point position
	result = lerp(w, lerp(v, lerp(u, gradAA, gradBA), lerp(u, gradAB, gradBB)), lerp(v, lerp(u, gradAA1, gradBA1), lerp(u, gradAB1, gradBB1)))
	return result