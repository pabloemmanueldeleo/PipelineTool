import maya.cmds as cmds
import mtoa.utils
import maya.mel as mel
import time
import os
import math

widgets = {}

def UI():

	if cmds.dockControl('toolDock',exists=1):
		cmds.deleteUI('toolDock')

	# window and mainLayout
	widgets['window'] = cmds.window()


	# TABS FILTER
	widgets['menuLyt']  = cmds.menuBarLayout()
	widgets['tabsMenu'] = cmds.menu('tabsMenusRBs', label='Filter Tabs',to=0)
	widgets['tabsRadioC'] = cmds.radioMenuItemCollection()

	cmds.menuItem('Modeling',rb=1,command=tabsFunc)
	cmds.menuItem('Lighting and Shading',rb=1,command=tabsFunc)
	cmds.menuItem('Rendering',rb=1,command=tabsFunc)
	cmds.menuItem('Misc Tools',rb=1,command=tabsFunc)
	cmds.menuItem('All',rb=1,command=tabsFunc)


	# MAIN LAYOUT
	cmds.scrollLayout(cr=1)
	widgets['mainLayout'] = cmds.columnLayout(adj=1)



	# Create first frameLayout for Modeling
	widgets['frameLayout_01'] = cmds.frameLayout(label='Modeling', collapsable=1, w=300, bs='etchedIn',mh=0,parent=widgets['mainLayout'])
	widgets['formLayout_01'] = cmds.formLayout()

	"""
	+---------------------------------------------------------+
	|-------------------Arnold Subdivisions-------------------|
	+---------------------------------------------------------+
	"""


	widgets['descriptionSubdivs'] = cmds.text( label='Arnold Subdivisions',w=315,h=20,fn='boldLabelFont',bgc=(0.15,0.15,0.15))

	# Controls for aiSubdivs
	widgets['subOptionMenu'] = cmds.optionMenuGrp( 'subOptionMenu',label='Sub Type',cal=(1,'left'),cw=(1,47) )
	cmds.menuItem( label='none' )
	cmds.menuItem( label='catclark' )
	cmds.menuItem( label='linear' )
	#Set catclark as default
	cmds.optionMenuGrp(widgets['subOptionMenu'],e=1,sl=2)

	widgets['subNumbText'] = cmds.text( label='Subdivs',fn='plainLabelFont')
	widgets['subNumb'] = cmds.intField( 'subNumb',minValue=0, maxValue=100, value=2, w=30)

	# Button with function call
	widgets['subBtn'] = cmds.button(l='Set',w=60,h=21,command=aiSubdivs)

	widgets['sepBottom'] = cmds.separator( w=315,height=2, style='out' )

	widgets['rvTdesc'] = cmds.text( label='rview toggle',fn='smallPlainLabelFont')

	widgets['bP'] = cmds.button(l='Bot Pvt',h=18,ann='off',command=bottomPivot)
	widgets['bBox'] = cmds.button(l='Iso bBox',h=18,ann='off',ebg=0, bgc=(0.3,0.3,0.3),command=isoBbox)

	widgets['textTog'] = cmds.textField( 'textTog',ed=0,w=60, bgc=(0.18,0.18,0.18) )

	widgets['onOffText'] = cmds.text( label='ON     OFF',fn='smallBoldLabelFont')

	widgets['rviewClean'] = cmds.button(l='',w=30,h=18,ann='0',command=toggle)

	widgets['sepBottom2'] = cmds.separator( w=315,height=2, style='out' )

	# Attach controls
	#cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['titleAI'],'top',0), (widgets['titleAI'],'left',0) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['subOptionMenu'],'top',30), (widgets['subOptionMenu'],'left',10) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['subNumbText'],'top',34), (widgets['subNumbText'],'right',120) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['subNumb'],'top',31), (widgets['subNumb'],'right',85) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['subBtn'],'top',30), (widgets['subBtn'],'right',10) ])
	#cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['descriptionSubdivs'],'top',0), (widgets['descriptionSubdivs'],'left',0) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['sepBottom'],'top',60), (widgets['sepBottom'],'left',0) ])

	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['rvTdesc'],'top',73), (widgets['rvTdesc'],'left',166) ])
	
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['bP'],'top',71), (widgets['bP'],'left',10) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['bBox'],'top',71), (widgets['bBox'],'left',60) ])

	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['textTog'],'top',70), (widgets['textTog'],'left',50+178) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['onOffText'],'top',74), (widgets['onOffText'],'left',55+178) ])
	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['rviewClean'],'top',71), (widgets['rviewClean'],'left',51+178) ])

	cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['sepBottom2'],'top',100), (widgets['sepBottom2'],'left',0) ])

	"""
	+---------------------------------------------------------+
	|-------------Quad Light and Isolate Textured-------------|
	+---------------------------------------------------------+
	"""

	padding = 80

	widgets['frameLayout_02'] = cmds.frameLayout(label='Lighting and Shading', collapsable=1, w=300, bs='etchedIn',mh=5,parent=widgets['mainLayout'])
	widgets['formLayout_02'] = cmds.formLayout()


	widgets['LightBtn'] = cmds.symbolButton(w=50,h=50,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/aiLight.png',command=lightFromView)
	widgets['QuadDescription'] = cmds.text( label='Light from view',h=20,fn='obliqueLabelFont')

	widgets['IsoBtn'] = cmds.symbolButton(w=50,h=50,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/iso.png',command=isoTextured)
	widgets['IsoTextDes'] = cmds.text( label='Isolate Textured',h=20,fn='obliqueLabelFont')

	widgets['OverrideBtn'] = cmds.symbolButton(w=50,h=50,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/override.png',command=MatOver)
	widgets['OverrDes'] = cmds.text( label='Material Override',h=20,fn='obliqueLabelFont')

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['LightBtn'],'top',20), (widgets['LightBtn'],'left',20) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['QuadDescription'],'top',0), (widgets['QuadDescription'],'left',10) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['IsoBtn'],'top',20), (widgets['IsoBtn'],'left',116) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['IsoTextDes'],'top',0), (widgets['IsoTextDes'],'left',100) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['OverrideBtn'],'top',20), (widgets['OverrideBtn'],'left',213) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['OverrDes'],'top',0), (widgets['OverrDes'],'left',197) ])




	"""
	+---------------------------------------------------------+
	|----------Skydome Light, Test Scene, AutoMap-------------|
	+---------------------------------------------------------+
	"""

	widgets['SkyDomeBtn'] = cmds.symbolButton(w=50,h=50,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/aiSkyDomeLight.png',command=aiSkyDome)
	widgets['SkyDomeDescription'] = cmds.text( label='Skydome Light',h=20,fn='obliqueLabelFont')

	widgets['sceneBtn'] = cmds.symbolButton(w=50,h=50,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/aiscene.png',command=aiScene)
	widgets['sceneDescription'] = cmds.text( label='Test aiScene',h=20,fn='obliqueLabelFont')

	widgets['autoMapBtn'] = cmds.symbolButton(w=50,h=50,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/remaptext.png',command=autoMap)
	widgets['autoMapDescription'] = cmds.text( label='Auto Map',h=20,fn='obliqueLabelFont')

	### attach layout
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['SkyDomeBtn'],'top',101), (widgets['SkyDomeBtn'],'left',20) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['SkyDomeDescription'],'top',80), (widgets['SkyDomeDescription'],'left',10) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['sceneBtn'],'top',101), (widgets['sceneBtn'],'left',116) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['sceneDescription'],'top',80), (widgets['sceneDescription'],'left',112) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['autoMapBtn'],'top',101), (widgets['autoMapBtn'],'left',213) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['autoMapDescription'],'top',80), (widgets['autoMapDescription'],'left',214) ])



	"""
	+-----------------------------------------------------------+
	|------------------------IOR FRESNEL------------------------|
	+-----------------------------------------------------------+
	"""

	reduceMargin = 190

	widgets['sepFres'] = cmds.separator( w=315,height=2, style='out' )


	widgets['FresnelImg'] = cmds.image( image='D:\PH_SCRIPTS\PH_RENDER\CUSTOMTOOLS_THERENDERBLOG\icons\fresnel.png',w=300,h=43 )

	widgets['nText'] = cmds.text( label='N',fn='plainLabelFont')
	widgets['nVal'] = cmds.floatField( 'nVal',minValue=0, maxValue=200000, value=0, w=50, precision=5) #cc=?

	widgets['kText'] = cmds.text( label='K',fn='plainLabelFont')
	widgets['kVal'] = cmds.floatField( 'kVal',minValue=0, maxValue=200000, value=0, w=50, precision=5)

	widgets['iorBtn'] = cmds.button('create',w=50,h=20,ebg=0,bgc= (0.1,0.27,0.47), command=drawCurve)

	widgets['sepIor'] = cmds.separator( w=315,height=2, style='out' )


	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['sepFres'],'top',357-reduceMargin), (widgets['sepFres'],'left',0) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['FresnelImg'],'top',360-reduceMargin), (widgets['FresnelImg'],'left',0) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nText'],'top',413-reduceMargin), (widgets['nText'],'left',10) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nVal'],'top',410-reduceMargin), (widgets['nVal'],'left',20) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kText'],'top',413-reduceMargin), (widgets['kText'],'left',80) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kVal'],'top',410-reduceMargin), (widgets['kVal'],'left',90) ])

	
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['iorBtn'],'top',410-reduceMargin), (widgets['iorBtn'],'left',155) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['sepIor'],'top',435-reduceMargin), (widgets['sepIor'],'left',0) ])

	"""
	+-----------------------------------------------------------+
	|--------------------IOR FRESNEL TRIPLE---------------------|
	+-----------------------------------------------------------+
	"""
	widgets['iorRed'] = cmds.separator( w=2,height=18, style='none',bgc=(0.8,0,0) )
	widgets['nTextRED'] = cmds.text( label='N',fn='plainLabelFont')
	widgets['nValRED'] = cmds.floatField( 'nValRED',minValue=0, maxValue=200000, value=0, w=50, precision=5)
	widgets['kTextRED'] = cmds.text( label='K',fn='plainLabelFont')
	widgets['kValRED'] = cmds.floatField( 'kValRED',minValue=0, maxValue=200000, value=0, w=50, precision=5)

	widgets['iorGreen'] = cmds.separator( w=2,height=18, style='none',bgc=(0,0.8,0) )
	widgets['nTextGREEN'] = cmds.text( label='N',fn='plainLabelFont')
	widgets['nValGREEN'] = cmds.floatField( 'nValGREEN',minValue=0, maxValue=200000, value=0, w=50, precision=5)
	widgets['kTextGREEN'] = cmds.text( label='K',fn='plainLabelFont')
	widgets['kValGREEN'] = cmds.floatField( 'kValGREEN',minValue=0, maxValue=200000, value=0, w=50, precision=5)

	widgets['iorBlue'] = cmds.separator( w=2,height=18, style='none',bgc=(0,0,0.8) )
	widgets['nTextBLUE'] = cmds.text( label='N',fn='plainLabelFont')
	widgets['nValBLUE'] = cmds.floatField( 'nValBLUE',minValue=0, maxValue=200000, value=0, w=50, precision=5)
	widgets['kTextBLUE'] = cmds.text( label='K',fn='plainLabelFont')
	widgets['kValBLUE'] = cmds.floatField( 'kValBLUE',minValue=0, maxValue=200000, value=0, w=50, precision=5)

	presets = [ 'Default','Aluminium','Gold','Copper','Silver','Chromium','Platinum','Nickel' ]

	widgets['opmenuIor'] = cmds.optionMenu( 'opmenuIor',w=75,cc=presetFresnel )
	for preset in presets:
		itemsMenuIor = cmds.menuItem(label=preset )

	widgets['iorTripleBtn'] = cmds.button('Create Network',w=100,h=24,ebg=0,bgc= (0.1,0.27,0.47), command=drawCurve2)


	widgets['checkDiff'] = cmds.checkBox('checkDiff', label='Affect Diffuse',v=1)

	

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nTextRED'],'top',448-reduceMargin), (widgets['nTextRED'],'left',10) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nValRED'],'top',445-reduceMargin), (widgets['nValRED'],'left',20) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kTextRED'],'top',448-reduceMargin), (widgets['kTextRED'],'left',80) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kValRED'],'top',445-reduceMargin), (widgets['kValRED'],'left',90) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['iorRed'],'top',446-reduceMargin), (widgets['iorRed'],'left',1) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nTextGREEN'],'top',472-reduceMargin), (widgets['nTextGREEN'],'left',10) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nValGREEN'],'top',469-reduceMargin), (widgets['nValGREEN'],'left',20) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kTextGREEN'],'top',472-reduceMargin), (widgets['kTextGREEN'],'left',80) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kValGREEN'],'top',469-reduceMargin), (widgets['kValGREEN'],'left',90) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['iorGreen'],'top',470-reduceMargin), (widgets['iorGreen'],'left',1) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nTextBLUE'],'top',495-reduceMargin), (widgets['nTextBLUE'],'left',10) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['nValBLUE'],'top',493-reduceMargin), (widgets['nValBLUE'],'left',20) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kTextBLUE'],'top',495-reduceMargin), (widgets['kTextBLUE'],'left',80) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['kValBLUE'],'top',493-reduceMargin), (widgets['kValBLUE'],'left',90) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['iorBlue'],'top',494-reduceMargin), (widgets['iorBlue'],'left',1) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['opmenuIor'],'top',440-reduceMargin), (widgets['opmenuIor'],'left',186) ])
	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['checkDiff'],'top',465-reduceMargin), (widgets['checkDiff'],'left',182) ])

	cmds.formLayout(widgets['formLayout_02'],e=1,af=[ (widgets['iorTripleBtn'],'top',488-reduceMargin), (widgets['iorTripleBtn'],'right',23) ])







	"""
	+---------------------------------------------------------+
	|-------------------QUICK RENDER SETTINGS-----------------|
	+---------------------------------------------------------+
	"""

	widgets['frameLayout_03'] = cmds.frameLayout(label='Rendering', collapsable=1, w=300, bs='etchedIn',mh=0,parent=widgets['mainLayout'])
	widgets['formLayout_03'] = cmds.formLayout()

	widgets['qrDesc'] = cmds.text( label='Arnold Quick Settings',w=315,h=20,fn='boldLabelFont',bgc=(0.15,0.15,0.15))

	widgets['renderBtn'] = cmds.symbolButton(w=30,h=30,image='D:/PH_SCRIPTS/PH_RENDER/CUSTOMTOOLS_THERENDERBLOG/icons/ai_logo.png',command=setRender)

	# query image size
	widX = cmds.getAttr('defaultResolution.width')
	heiY = cmds.getAttr('defaultResolution.height')

	widgets['rezXtext'] = cmds.text( label='Width:',fn='plainLabelFont')
	widgets['rezX'] = cmds.intField( 'rezX',minValue=2, maxValue=200000, value=widX, w=40, cc=SetResolution)

	widgets['rezYtext'] = cmds.text( label='Height:',fn='plainLabelFont')
	widgets['rezY'] = cmds.intField( 'rezY',minValue=2, maxValue=200000, value=heiY, w=40, cc=SetResolution)

	#widgets['setRezBtn'] = cmds.button(l='Set',w=50,h=20,command=SetResolution)

	widgets['rezMenu'] = cmds.optionMenu( 'rezMenu',w=75, cc=SetRezMenu )

	cmds.menuItem(label='320x240')
	cmds.menuItem(label='640x480')
	cmds.menuItem(label='1280x720')
	cmds.menuItem(label='1920x1080')
	cmds.menuItem(label='1360x768')
	cmds.menuItem(label='2048x858')

	widgets['sepQRS'] = cmds.separator( w=315,height=2, style='in' )


	"""******************************************************"""
	"""******************** ARNOLD ONLY *********************"""
	"""******************************************************"""

	if cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold':

		# FILTER
		widgets['FilterOptionMenu'] = cmds.optionMenuGrp( 'FilterOptionMenu',label='Filter',cal=(1,'left'),cw=(1,25),cc=setFiltering )
		cmds.menuItem( label='gaussian' )
		cmds.menuItem( label='catrom' )

		#query state
		mipQ = cmds.getAttr('defaultArnoldRenderOptions.textureAutomip')

		widgets['checkTextures'] = cmds.checkBox( label='Auto mipmap')
		cmds.connectControl( widgets['checkTextures'], 'defaultArnoldRenderOptions.textureAutomip' )

		# BUCKET SIE

		#query default
		bsize = cmds.getAttr('defaultArnoldRenderOptions.bucketSize')

		widgets['Buckettext'] = cmds.text( label='Bucket:',fn='plainLabelFont')
		widgets['BucketNumb'] = cmds.intField( 'BucketNumb',minValue=16, value=bsize, maxValue=256, w=59)
		cmds.connectControl( widgets['BucketNumb'], 'defaultArnoldRenderOptions.bucketSize' )
		#widgets['bukBtn'] = cmds.button(l='Set',w=30,h=18,command=changeBucket)


		## SAMPLING
		aiSettings = ['defaultArnoldRenderOptions.AASamples','defaultArnoldRenderOptions.GIDiffuseSamples',
					  'defaultArnoldRenderOptions.GIGlossySamples','defaultArnoldRenderOptions.GIRefractionSamples']


		widgets['sampSlid1'] = cmds.attrFieldSliderGrp( at=aiSettings[0],cw3=[18,50,80],label='AA' )
		widgets['sampSlid2'] = cmds.attrFieldSliderGrp( at=aiSettings[1],cw3=[18,50,80],label='GI' )
		widgets['sampSlid3'] = cmds.attrFieldSliderGrp( at=aiSettings[2],cw3=[18,50,80],label='GS' )
		widgets['sampSlid4'] = cmds.attrFieldSliderGrp( at=aiSettings[3],cw3=[18,50,80],label='RS' )


		## REFRESH SWATCHES

		#query state
		swQ = cmds.renderThumbnailUpdate(q=1)
		widgets['checkSw'] = cmds.checkBox( label='Swatch Render',v=swQ, cc=swRender )


		widgets['sepQRS2'] = cmds.separator( w=315,height=2, style='in' )


		## RAY DEPTH
		widgets['raySlid1'] = cmds.attrFieldSliderGrp( at='defaultArnoldRenderOptions.GIDiffuseDepth',cw3=[18,50,80],label='DIF' )
		widgets['raySlid2'] = cmds.attrFieldSliderGrp( at='defaultArnoldRenderOptions.GIGlossyDepth',cw3=[18,50,80],label='GLS' )
		widgets['raySlid3'] = cmds.attrFieldSliderGrp( at='defaultArnoldRenderOptions.GIReflectionDepth',cw3=[18,50,80],label='RF' )
		widgets['raySlid4'] = cmds.attrFieldSliderGrp( at='defaultArnoldRenderOptions.GIRefractionDepth',cw3=[18,50,80],label='RE' )


		# OVERRIDES

		widgets['checkOverride1'] = cmds.checkBox( label='Ignore Texts' )
		cmds.connectControl( widgets['checkOverride1'], 'defaultArnoldRenderOptions.ignoreTextures' )

		widgets['checkOverride2'] = cmds.checkBox( label='Ignore Subdivs' )
		cmds.connectControl( widgets['checkOverride2'], 'defaultArnoldRenderOptions.ignoreSubdivision' )

		widgets['checkOverride3'] = cmds.checkBox( label='Ignore Disp' )
		cmds.connectControl( widgets['checkOverride3'], 'defaultArnoldRenderOptions.ignoreDisplacement' )


		# Gamma

		widgets['gammaBtn'] = cmds.button( label='set gamma', w=60,h=18,bgc=(0.21,0.21,0.21),ebg=0, command=setGamma )



		# LOAD AOVS


		widgets['sepaov'] = cmds.separator( w=315,height=2, style='out' )

		widgets['descAov'] = cmds.text( label="Load AOV's",w=315,h=22,fn='boldLabelFont',bgc=(0.15,0.15,0.15))

		widgets['aovsList'] = cmds.optionMenu( 'aovsListMenu',w=95,label='AOV',cc=loadAOV )

		activeAOVS = cmds.ls(et='aiAOV')
		aovsNames = [i.split('_', 1)[1] for i in activeAOVS]

		cmds.menuItem(label='beauty')

		for item in aovsNames:
			cmds.menuItem(label=item )


		widgets['exposureSlider'] = cmds.attrFieldSliderGrp( at='defaultViewColorManager.exposure',cw3=[50,50,80],label='EXP' )

		widgets['resetBtnExp'] = cmds.button( label='', w=10,h=10,bgc=(0.21,0.21,0.21),ebg=0, command=resetExp )

		widgets['sepaov2'] = cmds.separator( w=315,height=2, style='out' )


		# ANIMATION REGION RENDER PREVIEW

		widgets['descReg'] = cmds.text( label="Animate region render preview",w=315,h=22,fn='boldLabelFont',bgc=(0.15,0.15,0.15))
		widgets['SetGlobBtn'] = cmds.button( label='set globals', h=20,bgc=(0.31,0.31,0.31),ebg=0,command= raiseRenderSettings )
		widgets['cleanAnimBtn'] = cmds.button( label='clean', h=20,bgc=(0.21,0.21,0.21),ebg=0,command=clearRview )

		widgets['RenderAnimBtn'] = cmds.button( label='render', w=75, h=20,bgc=(0.21,0.31,0.19),ebg=0,command=regionRenderAnim )
		widgets['playAnimBtn'] = cmds.button( label='play', w=75, h=20,bgc=(0.21,0.21,0.4),ebg=0,command=playRegion )

		widgets['sepAnimReg'] = cmds.separator( w=315,height=2, style='out' )

		widgets['regAnimDesc'] = cmds.text( label='Set the range of the animation',w=288,fn='obliqueLabelFont')
		widgets['beginAnimInt'] = cmds.floatField( 'beginAnimInt',minValue=0, value=( cmds.playbackOptions(q=1,ast=1) ), w=50,precision=2,cc=SetFrames)
		widgets['endAnimInt'] = cmds.floatField( 'endAnimInt',minValue=1, value=( cmds.playbackOptions(q=1,aet=1) ), w=50,precision=2,cc=SetFrames)

		widgets['sepAnimReg2'] = cmds.separator( w=315,height=2, style='out' )



		widgets['frameLayoutRange'] = cmds.frameLayout(w=160,h=22,bs='in',parent=widgets['formLayout_03'],lv=0,mw=0,mh=0)

		widgets['rangeControl'] = cmds.rangeControl( 'rangeControl2', parent=widgets['frameLayoutRange'],nbg=1)

		widgets['hideSep'] = cmds.separator( w=160,height=2, style='out', parent=widgets['formLayout_03'])

		widgets['hideBorders1'] = cmds.text( label="",w=160,h=2,fn='boldLabelFont',bgc=(0.27,0.27,0.27), parent=widgets['formLayout_03'])
		widgets['hideBorders2'] = cmds.text( label="",w=1,h=20,fn='boldLabelFont',bgc=(0.38,0.38,0.38), parent=widgets['formLayout_03'])






	"""******************************************************"""
	"""******************** ARNOLD ONLY END******************"""
	"""******************************************************"""

	## Atach widgets
	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['qrDesc'],'top',0), (widgets['qrDesc'],'left',0) ])
	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['renderBtn'],'top',30), (widgets['renderBtn'],'left',10) ])

	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['rezXtext'],'top',38), (widgets['rezXtext'],'left',49) ])
	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['rezX'],'top',35), (widgets['rezX'],'left',83) ])
	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['rezYtext'],'top',38), (widgets['rezYtext'],'left',128) ])
	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['rezY'],'top',35), (widgets['rezY'],'left',165) ])

	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['rezMenu'],'top',35), (widgets['rezMenu'],'left',212) ])

	cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sepQRS'],'top',70), (widgets['sepQRS'],'left',0) ])







	if cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold':

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['FilterOptionMenu'],'top',88), (widgets['FilterOptionMenu'],'left',180) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['checkTextures'],'top',111), (widgets['checkTextures'],'left',180) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['checkSw'],'top',130), (widgets['checkSw'],'left',180) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['Buckettext'],'top',152), (widgets['Buckettext'],'left',180) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['BucketNumb'],'top',149), (widgets['BucketNumb'],'left',220) ])
		#cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['bukBtn'],'top',150), (widgets['bukBtn'],'left',248) ])


		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sampSlid1'],'top',90), (widgets['sampSlid1'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sampSlid2'],'top',110), (widgets['sampSlid2'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sampSlid3'],'top',130), (widgets['sampSlid3'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sampSlid4'],'top',150), (widgets['sampSlid4'],'left',10) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sepQRS2'],'top',188), (widgets['sepQRS2'],'left',0) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['raySlid1'],'top',200), (widgets['raySlid1'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['raySlid2'],'top',220), (widgets['raySlid2'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['raySlid3'],'top',240), (widgets['raySlid3'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['raySlid4'],'top',260), (widgets['raySlid4'],'left',10) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['checkOverride1'],'top',201), (widgets['checkOverride1'],'left',180) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['checkOverride2'],'top',221), (widgets['checkOverride2'],'left',180) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['checkOverride3'],'top',241), (widgets['checkOverride3'],'left',180) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['gammaBtn'],'top',261), (widgets['gammaBtn'],'left',180) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sepaov'],'top',291), (widgets['sepaov'],'left',0) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['descAov'],'top',293), (widgets['descAov'],'left',0) ])


		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['aovsList'],'top',325), (widgets['aovsList'],'left',10) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['exposureSlider'],'top',324), (widgets['exposureSlider'],'left',82) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['resetBtnExp'],'top',329), (widgets['resetBtnExp'],'left',270) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sepaov2'],'top',355), (widgets['sepaov2'],'left',0) ])



		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['descReg'],'top',357), (widgets['descReg'],'left',0) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['SetGlobBtn'],'top',388), (widgets['SetGlobBtn'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['cleanAnimBtn'],'top',388), (widgets['cleanAnimBtn'],'left',75) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['RenderAnimBtn'],'top',388), (widgets['RenderAnimBtn'],'left',123) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['playAnimBtn'],'top',388), (widgets['playAnimBtn'],'left',205) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sepAnimReg'],'top',416), (widgets['sepAnimReg'],'left',0) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['regAnimDesc'],'top',422), (widgets['regAnimDesc'],'left',0) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['beginAnimInt'],'top',442), (widgets['beginAnimInt'],'left',10) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['endAnimInt'],'top',442), (widgets['endAnimInt'],'left',230) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['sepAnimReg2'],'top',470), (widgets['sepAnimReg2'],'left',0) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['hideSep'],'top',442), (widgets['hideSep'],'left',65) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['hideBorders1'],'top',440), (widgets['hideBorders1'],'left',65) ])
		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['hideBorders2'],'top',442), (widgets['hideBorders2'],'left',65) ])

		cmds.formLayout(widgets['formLayout_03'],e=1,af=[ (widgets['frameLayoutRange'],'top',440), (widgets['frameLayoutRange'],'left',65) ])





	############################################################

	widgets['frameLayout_04'] = cmds.frameLayout(label='Misc Tools', collapsable=1, w=300, bs='etchedIn',mh=0,parent=widgets['mainLayout'])
	widgets['formLayout_04'] = cmds.formLayout()
	widgets['btnFiles'] = cmds.button('File Info',command=fileinfo,w=100,ebg=0,bgc= (0.27,0.47,0.27) )
	widgets['btnREF'] = cmds.button('Open Reference',command=openRef,w=120,ebg=0,bgc= (0.27,0.27,0.47) )
	widgets['btnTEMP'] = cmds.button('Open tmp img',command=openImgTemp,w=100,ebg=0,bgc= (0.27,0.67,0.47) )
	widgets['btnREN'] = cmds.button('Rename Objs Shapes',command=renameDup,w=120,ebg=0,bgc= (0.67,0.67,0.47) )
	widgets['btnDupSh'] = cmds.button('Select Dup shapes',command=dupShapes,w=100,ebg=0,bgc= (0.67,0.27,0.27) )
	widgets['sepMisc1'] = cmds.separator( w=315,height=2, style='out' )


	cmds.formLayout(widgets['formLayout_04'],e=1,af=[ (widgets['btnFiles'],'top',10), (widgets['btnFiles'],'left',10) ])
	cmds.formLayout(widgets['formLayout_04'],e=1,af=[ (widgets['btnREF'],'top',10), (widgets['btnREF'],'left',150) ])
	cmds.formLayout(widgets['formLayout_04'],e=1,af=[ (widgets['btnTEMP'],'top',40), (widgets['btnTEMP'],'left',10) ])
	cmds.formLayout(widgets['formLayout_04'],e=1,af=[ (widgets['btnREN'],'top',40), (widgets['btnREN'],'left',150) ])
	cmds.formLayout(widgets['formLayout_04'],e=1,af=[ (widgets['btnDupSh'],'top',70), (widgets['btnDupSh'],'left',10) ])
	cmds.formLayout(widgets['formLayout_04'],e=1,af=[ (widgets['sepMisc1'],'top',100), (widgets['sepMisc1'],'left',0) ])

	"""
	+---------------------------------------------------------+
	|-------------------------SHOW UI-------------------------|
	+---------------------------------------------------------+
	"""


	# Refresh bug?
	cmds.dockControl('dockControl1', e=1, r=1)
	

	# Show Dock Window
	widgets['dockPanel'] = cmds.dockControl('toolDock',label='Custom Tools',area='right',w=326,content=widgets['window'],aa='right',sizeable=0)
	cmds.dockControl('toolDock',e=1,r=1)








"""
+---------------------------------------------------------+
|                  <<< FUNCTIONS TOOLS >>>                |
+---------------------------------------------------------+
"""



"""
+-----------+----------+
|      Ai Subdivs      |
+-----------+----------+
"""

def aiSubdivs(*args):

	# get selection
	selection = cmds.ls(sl = True)


	# avoid empty selection
	if len(selection) > 0:

		subType = cmds.optionMenuGrp('subOptionMenu',q=1,sl=True)
		subType = int(subType) - 1
		
		subCount = cmds.intField('subNumb',q=1,v=True)

		# set subdivs type and number
		for object in selection:
			if cmds.listRelatives(object,pa=1)[0] in cmds.ls(et='mesh'):
			#if cmds.listRelatives(object,pa=1) in cmds.ls(et='mesh'):
			#if object in cmds.listRelatives(cmds.ls(et='mesh'),p=1)
				cmds.setAttr(object + ".aiSubdivType" , subType)
				cmds.setAttr(object + ".aiSubdivIterations" , subCount)

	else:
		cmds.warning("Empty selection")


"""
+-----------+----------+
|    Light from View   |
+-----------+----------+
"""

def lightFromView(*args):
	#select the perspective camera
	selection = cmds.ls("persp")

	#Get the transform values
	translation = cmds.xform(selection, query=True, worldSpace=True, rotatePivot=True)
	rotation = cmds.xform(selection, query=True, worldSpace=True, ro=True)

	#Create aiAreaLight
	myLight = mtoa.utils.createLocator('aiAreaLight', asLight=True)

	#Apply transforms to the light
	cmds.xform( myLight[1], r=True, ro=rotation, t=translation, s=(30,30,30))

	#Set attributtes to the light
	cmds.setAttr(myLight[0] + ".aiTranslator" , 'quad', type="string")
	cmds.setAttr(myLight[0] + ".intensity" , 300)
	cmds.setAttr(myLight[0] + ".aiSamples" , 2)



"""
+-----------+----------+
|   Isolate Textured   |
+-----------+----------+
"""

def isoTextured(*args):

    if cmds.window('exitWindow', ex=True):

        cmds.warning("Already in isolate mode")

    else:

        noSelection = cmds.ls(sl=True)

        if noSelection == []:
            cmds.warning( "No Objects Selected" )

        else:



            allGeo = set( cmds.ls(geometry=True) )
            singleObj = set( cmds.listRelatives(shapes=True) )
            
            finalSelection = allGeo-singleObj

            if len(finalSelection) <= 0:
                cmds.warning( "All objects Selected" )

            else:

                if len(finalSelection) > 0:

                    if cmds.getPanel(withFocus=1) != 'modelPanel4':
                        cmds.setFocus('modelPanel4')

                    viewportPan = cmds.getPanel( withFocus=True )

                    cmds.modelEditor( viewportPan, edit=True, displayAppearance='smoothShaded', dtx=True)


                    for obj in finalSelection:
                        cmds.setAttr(obj + ".overrideEnabled" , 1)
                        cmds.setAttr(obj + ".overrideTexturing" , 0)



                    
                    window = cmds.window( "exitWindow", bgc=[0.5,0.1,0.08], tb=0,s=False )
                    cmds.columnLayout( adjustableColumn=True )
                    cmds.button( label='Exit Isolate Mode', w=200,h=35, command=UndoIsoTextured )

                    vpX = cmds.formLayout(viewportPan,q=True,w=True)
                    vpX = vpX/2
                    
                    cmds.showWindow( window )
                    cmds.window( "exitWindow", edit=True, tlc=(100,vpX-60) )



def UndoIsoTextured(*args):

    AllGeo = cmds.ls(geometry=True)

    if cmds.getPanel(withFocus=1) != 'modelPanel4':
        cmds.setFocus('modelPanel4')

    viewportPan = cmds.getPanel( withFocus=True )
    cmds.modelEditor( viewportPan, edit=True, displayAppearance='smoothShaded', dtx=False)
    
    for objs in AllGeo:
        cmds.setAttr(objs + ".overrideEnabled" , 0)
        cmds.setAttr(objs + ".overrideTexturing" , 1)

    cmds.deleteUI("exitWindow")



"""
+-----------+----------+
|  Material Override   |
+-----------+----------+
"""

def MatOver(*args):

	condition = cmds.editRenderLayerGlobals( q=1, currentRenderLayer=1 ) == 'defaultRenderLayer' and cmds.ls(geometry=True) != []

	if condition:

	    #create a copy of master layer with a specific name "OverrideMaterial_rlyr"
	    cmds.createRenderLayer(name='OverrideMaterial_rlyr', g=True)
	    
	    #select the new layer as active
	    cmds.editRenderLayerGlobals( currentRenderLayer = 'OverrideMaterial_rlyr' )
	    
	    #assign material override to that layer
	    cmds.sets( name='material_overrideSG', renderable=True, empty=True )
	    cmds.shadingNode('lambert', asShader=True, n='material_override_M')
	    cmds.surfaceShaderList( 'material_override_M', add='material_overrideSG' )
	    cmds.connectAttr( 'material_overrideSG.message', 'OverrideMaterial_rlyr.shadingGroupOverride', force=True )

	else:
		
		if cmds.editRenderLayerGlobals( q=1, currentRenderLayer=1 ) == 'defaultRenderLayer':
			return False
			#cmds.warning('Scene empty')
		else:
		    #set to default renderLayer, delete OverrideRenderLayer and material nodes
		    cmds.editRenderLayerGlobals( currentRenderLayer = 'defaultRenderLayer' )
		    cmds.delete( 'OverrideMaterial_rlyr', 'material_overrideSG', 'material_override_M' )


"""
+-----------+----------+
|     SkyDomeLight     |
+-----------+----------+
"""

def aiSkyDome(*args):

	aiSkyNode = mtoa.utils.createLocator('aiSkyDomeLight', asLight=True)

	cmds.setAttr(aiSkyNode[0]+'.skyRadius',1)
	cmds.setAttr(aiSkyNode[0]+'.aiSamples',2)

	physicalSky = cmds.shadingNode("aiPhysicalSky", asTexture=True)
	cmds.connectAttr(physicalSky+'.outColor', aiSkyNode[0]+'.color',f=1)

"""
+-----------+----------+
|      Test Scene      |
+-----------+----------+
"""


def aiScene(*args):
	
	aiSkyDome()

	cmds.polyPlane(w=26,h=26,sx=1,sy=1)
	mySphere = cmds.polySphere(r=3)
	cmds.setAttr(mySphere[0]+'.translateY',3)
	cmds.select(clear=1)


"""
+-----------+----------+
|       Auto Map       |
+-----------+----------+
"""

def autoMap(*args):

    txts = cmds.ls(tex=1)
    #rmps = cmds.ls(exactType='remapHsv')
    #final = txts + rmps
    
    textSelected = cmds.ls(sl=1)
    
    if textSelected == [] or len(textSelected) > 1 or textSelected[0] not in txts:
        cmds.warning('Select a texture node')
    else:
        # Create remaps hsv
        rmp1 = cmds.shadingNode('remapHsv', asUtility=1, name='spec_remap')
        rmp2 = cmds.shadingNode('remapHsv', asUtility=1, name='bump_remap')
        
        
        # Connect remaps and remove saturation
        cmds.connectAttr(textSelected[0]+'.outColor', rmp1+'.color')
        cmds.connectAttr(textSelected[0]+'.outColor', rmp2+'.color')
        
        cmds.setAttr(rmp1+'.saturation[1].saturation_FloatValue', 0)
        cmds.setAttr(rmp2+'.saturation[1].saturation_FloatValue', 0)
        
        # Create shader and connect nodes
        aiShader = cmds.shadingNode('aiStandard', asShader=1, name='aiStandard_remap')
        
        cmds.connectAttr(textSelected[0]+'.outColor', aiShader+'.color')
        cmds.connectAttr(rmp1+'.outColor', aiShader+'.KsColor')
        
        cmds.setAttr(aiShader+'.Ks',1)
        cmds.setAttr(aiShader+'.specularFresnel',1)
        cmds.setAttr(aiShader+'.Ksn',0.15)
        cmds.setAttr(aiShader+'.specularRoughness',0.2)
        cmds.setAttr(aiShader+'.Kd',1)
        
        
        bumpNode = cmds.shadingNode('bump2d', asUtility=1)
        cmds.setAttr(bumpNode+'.bumpDepth',0.15)
        
        cmds.connectAttr(rmp2+'.outColorR', bumpNode+'.bumpValue',f=1)
        cmds.connectAttr(bumpNode+'.outNormal', aiShader+'.normalCamera',f=1)

        cmds.select(aiShader)


"""
+-----------+----------+
|    Render Texture    |
+-----------+----------+
"""

# used in 2 functions
def queryRV():
	for i in cmds.getPanel(vis=1):
		if i == 'renderView':
			return 1

def renderTexture(*args):

	materials = cmds.ls(mat=1)

	if 'textures_MAT' in materials:

		for i in cmds.lsUI(windows=1):
			if i == "renderViewWindow":
				cmds.showWindow(i)
	    
	    
		rview = cmds.getPanel( sty = 'renderWindowPanel' )

		if queryRV() != 1:
			cmds.scriptedPanel(rview, e=1, tearOff=1)

		ntype = cmds.nodeType('textures_MAT')

		if ntype == 'blinn':
			cmds.setAttr('textures_MAT.incandescence',0,0,0)

		cmds.render('persp',x=500,y=500)
		cmds.renderWindowEditor( rview, e=True, cap=0 )
		cmds.renderWindowEditor( rview, e=True, rs=True )

		if ntype == 'blinn':
			cmds.setAttr('textures_MAT.incandescence',1,1,1)

	else:
		cmds.warning('No texture to render')


"""
+-----------+----------+
|    QUICK SETTINGS    |
+-----------+----------+
"""

def setRender(*args):

	if cmds.getAttr('defaultRenderGlobals.currentRenderer') != 'arnold':

		cmds.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')
		import mtoa.core as core
		core.createOptions()


		import customTools_therenderblog
		reload(customTools_therenderblog)
		customTools_therenderblog.UI()

	else:
		if cmds.arnoldIpr(q=1, mode='start'):
			cmds.arnoldIpr(mode='stop')
		else:
			#cmds.warning('Arnold Render already active')
			for i in cmds.lsUI(windows=1):
				if i == "renderViewWindow":
					cmds.showWindow(i)

			rview = cmds.getPanel( sty = 'renderWindowPanel' )

			if queryRV() != 1:
				cmds.scriptedPanel(rview, e=1, tearOff=1)


			resolX = cmds.getAttr('defaultResolution.width')
			resolY = cmds.getAttr('defaultResolution.height')
			#cmds.arnoldRender(cam='persp', w=resolX, h=resolY)
			cmds.arnoldIpr(cam='persp', w=resolX, h=resolY, mode='start')
			cmds.arnoldIpr(mode='refresh')
			#cmds.arnoldIpr(mode='stop')


def SetResolution(*args):

	resolutX = cmds.intField( widgets['rezX'] ,q=1,v=True)
	resolutY = cmds.intField( widgets['rezY'] ,q=1,v=True)

	cmds.setAttr('defaultResolution.width', resolutX)
	cmds.setAttr('defaultResolution.height', resolutY)

	#mel.eval('updateMayaSoftwarePixelAspectRatio')

	aspRatio = float(cmds.getAttr('defaultResolution.width'))/float(cmds.getAttr('defaultResolution.height'))
	cmds.setAttr('defaultResolution.deviceAspectRatio', aspRatio)


def setFiltering(*args):
	aiFilter = cmds.optionMenuGrp('FilterOptionMenu',q=1,sl=True)

	if aiFilter == 1:
		cmds.setAttr('defaultArnoldFilter.aiTranslator', 'gaussian' ,type='string')
	else:
		cmds.setAttr('defaultArnoldFilter.aiTranslator', 'catrom' ,type='string')



def swRender(*args):
	qsw = cmds.renderThumbnailUpdate(q=1)

	if qsw == 1:
		cmds.renderThumbnailUpdate(0)
	else:
		cmds.renderThumbnailUpdate(1)


def rvClean(*args):
	rv = cmds.getPanel(sty='renderWindowPanel')

	mel.eval('renderWindowMenuCommand toolbar renderView;')
	cmds.scriptedPanel(rv , e=True, mbv=0 )


	mel.eval('renderWindowMenuCommand toolbar renderView;')
	cmds.scriptedPanel(rv , e=True, mbv=1 )

def getRVstate():
	for i in cmds.lsUI(windows=1):
		if i == "renderViewWindow":
			return 1

def toggle(*args):

	query = cmds.button(widgets['rviewClean'],q=1,ann=1)
	rv = cmds.getPanel(sty='renderWindowPanel')

	if getRVstate() != 1:

		cmds.warning('RenderView is not visible')

	else:

		if query == '0':
			cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['rviewClean'],'top',71), (widgets['rviewClean'],'left',79+178) ])
			cmds.button(widgets['rviewClean'],e=1,ann='1')

			#HIDE RENDERVIEW MENU AND TOOLBAR
			mel.eval('renderWindowMenuCommand toolbar renderView;')
			cmds.scriptedPanel(rv , e=True, mbv=0 )
			cmds.renderWindowEditor(rv,e=1,cap=0)
			cmds.renderWindowEditor(rv,e=1,rs=1)
		else:
			cmds.formLayout(widgets['formLayout_01'],e=1,af=[ (widgets['rviewClean'],'top',71), (widgets['rviewClean'],'left',51+178) ])
			cmds.button(widgets['rviewClean'],e=1,ann='0')

			#SHOW RENDERVIEW MENU AND TOOLBAR
			mel.eval('renderWindowMenuCommand toolbar renderView;')
			cmds.scriptedPanel(rv , e=True, mbv=1 )

def bottomPivot(*args):

	selection = cmds.ls(sl=True)

	if selection == []:
		cmds.warning('Nothing selected')

	for selected in selection:

		# center the pivot
		cmds.xform(selected, cp=True)
		
		# determine the bounding box so we know where to put our pivot
		# bounding_box = xmin ymin zmin xmax ymax zmax.
		bounding_box = cmds.xform(selected, q=True, boundingBox=True, ws=True)
		xmin, ymin, zmin, xmax, ymax, zmax = bounding_box
		
		# move the pivot points in the Y direction to the bottom Y point
		cmds.move(ymin, [selected + ".scalePivot",selected + ".rotatePivot"], y=True, absolute=True)

def isoBbox(*args):

	queryStateBbox = cmds.button( widgets['bBox'], q=1, ann=1 )


	if queryStateBbox == 'off':

		selection = cmds.ls(sl=1,transforms=True)

		if selection == []:
			cmds.warning('Nothing selected')

		else:
			allGeo = set( cmds.ls(geometry=True) )
			singleObj = set( cmds.listRelatives(shapes=True) )
			finalSelection = allGeo-singleObj

			for obj in finalSelection:
				cmds.setAttr(obj + ".overrideEnabled" , 1)
				cmds.setAttr(obj + ".overrideLevelOfDetail" , 1)

			cmds.button( widgets['bBox'], e=1, ann='on', ebg=0, bgc=(0.4,0.04,0.03) )

	else:
		allGeo = set( cmds.ls(geometry=True) )

		for obj in allGeo:
			cmds.setAttr(obj + ".overrideLevelOfDetail" , 0)
			cmds.setAttr(obj + ".overrideEnabled" , 0)

		cmds.button( widgets['bBox'], e=1, ann='off',ebg=0, bgc=(0.3,0.3,0.3) )


"""
+-----------+----------+
|      LOAD AOV'S      |
+-----------+----------+
"""


def loadAOV(*args):

	activeAOVS = cmds.ls(et='aiAOV')
	aovsNames = [i.split('_', 1)[1] for i in activeAOVS]

	if activeAOVS == []:
		cmds.warning("No aov's setup")
	else:
		CurrentProject = cmds.workspace(q=1,fullName=1)
		rview = cmds.getPanel( sty = 'renderWindowPanel' )
		selectedAOV = cmds.optionMenu('aovsListMenu',q=1,v=1)
		
		ImgTempPath = CurrentProject + '/images/tmp/'
		latest_file = max(all_files_under(ImgTempPath), key=os.path.getmtime)
		splitPath = latest_file.replace('/','\\')
		
		splitPath = splitPath.split(os.sep)


		for n, i in enumerate(splitPath):
			if i in aovsNames or i == 'beauty':
				splitPath[n] = selectedAOV

		splitPath[0] = splitPath[0] + '\\'
		pathToImg = reduce(os.path.join,splitPath)

		cmds.renderWindowEditor( rview, e=True, li=pathToImg )

def all_files_under(path):
	for cur_path, dirnames, filenames in os.walk(path):
		for filename in filenames:
			yield os.path.join(cur_path, filename)

def resetExp(*args):
	cmds.setAttr('defaultViewColorManager.exposure',0)


def setGamma(*args):
	cmds.setAttr("defaultArnoldRenderOptions.display_gamma", 1)
	cmds.setAttr("defaultViewColorManager.imageColorProfile", 2)


"""
+-----------+----------+
|    Animate Region    |
+-----------+----------+
"""

def SetFrames(*args):
	startFrame = cmds.floatField( 'beginAnimInt' , q=1,v=True)
	endFrame   = cmds.floatField( 'endAnimInt' , q=1,v=True)

	cmds.playbackOptions(e=1,ast=startFrame)
	cmds.playbackOptions(e=1,aet=endFrame)

	cmds.playbackOptions( min=startFrame , max=endFrame )

	cmds.setAttr ("defaultRenderGlobals.startFrame", startFrame)
	cmds.setAttr ("defaultRenderGlobals.endFrame", endFrame)

	mel.eval('playButtonStart;')



def raiseRenderSettings(*args):
	mel.eval('RenderGlobalsWindow;')

	sFrame = cmds.floatField( 'beginAnimInt' , q=1,v=True)
	eFrame   = cmds.floatField( 'endAnimInt' , q=1,v=True)

	cmds.setAttr ("defaultRenderGlobals.startFrame", sFrame)
	cmds.setAttr ("defaultRenderGlobals.endFrame", eFrame)


def clearRview(*args):

	## FOR REFERENCE ONLY

	#rview = cmds.getPanel( sty = 'renderWindowPanel' )
	#cmds.renderWindowEditor(rview, e=1, ra=1)
	#attrbts = [ cmds.getAttr('defaultResolution.width') , cmds.getAttr('defaultResolution.height') ]
	#cmds.renderWindowEditor(rview, e=1, cl=( attrbts[0], attrbts[1], 0.1, 0.1, 0.1) )

	mel.eval('renderWindowMenuCommand removeAllImagesFromRenderView renderView;')
	mel.eval('renderWindowRenderCamera snapshot renderView "";')
	mel.eval('playButtonStart;')


def regionRenderAnim(*args):

	clearRview()

	rview = cmds.getPanel( sty = 'renderWindowPanel' )

	if cmds.renderWindowEditor(rview,q=1,mq=1):
		#rangeLimit = cmds.floatField( 'endAnimInt' , q=1,v=True)

		rangeLimit = int(cmds.playbackOptions(q=1,max=1))

		#postRenderMel = "playButtonStepForward;if (`currentTime -q` <="+str(rangeLimit)+" ) {renderWindowMenuCommand keepImageInRenderView renderView;renderWindowRenderRegion renderView;} else {setAttr -type \"string\" defaultRenderGlobals.postRenderMel \"\";playButtonStart;}"
		postRenderMel = "if (`currentTime -q` <"+str(rangeLimit)+" ) {playButtonStepForward;renderWindowMenuCommand keepImageInRenderView renderView;renderWindowRenderRegion renderView;} else if (`currentTime -q` =="+str(rangeLimit)+" ) {setAttr -type \"string\" defaultRenderGlobals.postRenderMel \"\";playButtonStart;} else {setAttr -type \"string\" defaultRenderGlobals.postRenderMel \"\";playButtonStart;};"
		cmds.setAttr('defaultRenderGlobals.postRenderMel',postRenderMel,type='string')
		mel.eval('renderWindowRenderRegion renderView')
	else:
		cmds.warning('Draw the region to render')
		mel.eval('renderWindowRenderCamera snapshot renderView "";')


def playRegion(*args):

	rview = cmds.getPanel( sty = 'renderWindowPanel' )

	totalFrames = int(cmds.playbackOptions(q=1,max=1)) - int(cmds.playbackOptions(q=1,min=1))
	displayImg = []

	for i in range(-1,totalFrames):
		displayImg.append(i)

	displayImg.reverse()

	for item in displayImg:
		#print "Displaying image..." + str(item)
		cmds.renderWindowEditor(rview,e=1,di=item)
		cmds.renderWindowEditor(rview,e=1,cap=0)
		#cmds.renderWindowEditor(rview,e=1,pca='')
		time.sleep(0.02)


def SetRezMenu(*args):

	querySelectedRez = cmds.optionMenu( 'rezMenu',q=1,v=1 )
	rez = querySelectedRez.split('x')

	cmds.intField( widgets['rezX'] ,e=1,v= int(rez[0]) )
	cmds.intField( widgets['rezY'] ,e=1,v= int(rez[1]) )

	cmds.setAttr('defaultResolution.width', int(rez[0]) )
	cmds.setAttr('defaultResolution.height', int(rez[1]) )

	aspRatio = float(cmds.getAttr('defaultResolution.width'))/float(cmds.getAttr('defaultResolution.height'))
	cmds.setAttr('defaultResolution.deviceAspectRatio', aspRatio)


"""
------------------
FILE INFO MISC TAB
------------------
"""


def fileinfo(*args):

	if cmds.window('FileInfo',ex=1):
		cmds.deleteUI('FileInfo')

	mywindow = cmds.window('FileInfo',mnb=0,mxb=0)
	cmds.scrollLayout(cr=1)
	mainFormL = cmds.columnLayout(adj=1)
	MyframeLayout = cmds.frameLayout(label='All Files', collapsable=0, w=200, bs='etchedIn',mh=3,mw=3,parent=mainFormL)


	### POPULATE INFO
	prj = cmds.workspace(q=1,fullName=1)
	brokenFiles = []
	outFiles = []
	allFiles = []
	duplicated = []
	mixPathNfile = []
	duplicatedFiles = []

	fileNodes = cmds.ls(typ='file')

	cmds.text( 'stats', label="0 files broken",fn='obliqueLabelFont',align='left' )
	cmds.text( 'stats2', label="0 files not in the project imgs",fn='obliqueLabelFont',align='left' )
	cmds.text( 'stats3', label="0 files duplicated",fn='obliqueLabelFont',align='left' )
	cmds.text( 'stats4', label="0 files without shader",fn='obliqueLabelFont',align='left' )

	mbtn = cmds.button("right click to select options",pma=1)

	cmds.popupMenu(p=mbtn)
	cmds.menuItem("select all",command=selectAll )
	cmds.menuItem("select broken",command=selectBroken  )
	cmds.menuItem("select duplicated",command=selectDup  )
	cmds.menuItem("select files outside project",command=selectOut  )
	cmds.menuItem("select files with no shader",command=selUnused  )
	cmds.menuItem("clear selection",command='cmds.select(None)'  )

	cmds.button("set file paths to current project",command=correctPaths, ebg=0, bgc=(0.185,0.185,0.185) )

	cmds.separator(style='in')

	for fnode in fileNodes:
		cmds.text( label=fnode,fn='boldLabelFont',align='left' )
		result = cmds.getAttr(fnode+'.fileTextureName')
		allFiles.append(result)
		mixPathNfile.append(result+'*'+fnode)
	    
		if len(result) > 35:    
			cmds.textField('tf_'+fnode,text=result[0:20]+'...'+result[-10:],fn='smallPlainLabelFont',ed=0,bgc=(0.150,0.150,0.150))
		else:
			cmds.textField('tf_'+fnode,text=result,fn='smallPlainLabelFont',ed=0,bgc=(0.150,0.150,0.150))
		
		if cmds.file(result, q=1, ex=1)== False or result == '':
			cmds.textField( 'tf_'+fnode, e=1, bgc=(0.20,0.10,0.10), ann='broken')
			brokenFiles.append(fnode)
		
		if result[ 0 : len(prj) ] != prj and result[ 0 : 12 ] != 'sourceimages':
			outFiles.append(fnode)

		if fnode != fileNodes[-1]:
			cmds.separator(style='in')

	for i in mixPathNfile:
		if allFiles.count( i.split('*')[0] ) > 1:
			duplicated.append( i.split('*')[0]  )
			duplicatedFiles.append( i.split('*')[1] )

			if duplicated.count( i.split('*')[0]  ) >= 2:
				duplicated.remove( i.split('*')[0]  )     

	cmds.text( 'stats', e=1, label= str(len(brokenFiles))+ " files broken")
	cmds.text( 'stats2', e=1, label= str(len(outFiles))+ " files not in the project imgs")
	cmds.text( 'stats3', e=1, label= str(len(duplicated))+" files duplicated")
	cmds.text( 'stats4', e=1, label= selUnusedNumb() +" files without shader")

	cmds.showWindow(mywindow)
	cmds.window('FileInfo',e=1,w=230,h=300)
	cmds.setFocus(mywindow)



def correctPaths(*args):

	textures = cmds.ls(type='file')

	for i in textures:
		result = cmds.getAttr(i+'.fileTextureName')
		path = 'sourceimages/' + result.split('/')[-1]
		cmds.setAttr( i + '.fileTextureName', path,type='string')



def selectAll(*args):
	fileNodes = cmds.ls(typ='file')
	cmds.select(fileNodes)

def selectBroken(*args):

	fileNodes = cmds.ls(typ='file')
	brokenFiles = []

	for fnode in fileNodes:
		result = cmds.getAttr(fnode+'.fileTextureName')

		if cmds.file(result, q=1, ex=1) == False or result == '':
			brokenFiles.append(fnode)

	cmds.select(brokenFiles)


def selectDup(*args):
	fileNodes = cmds.ls(typ='file')
	allFiles = []
	mixPathNfile = []
	duplicatedFiles = []

	for fnode in fileNodes:
		result = cmds.getAttr(fnode+'.fileTextureName')
		allFiles.append(result)
		mixPathNfile.append(result+'*'+fnode)

	for i in mixPathNfile:
		if allFiles.count( i.split('*')[0] ) > 1:
			duplicatedFiles.append( i.split('*')[1] )

	cmds.select(duplicatedFiles)





def selectOut(*args):

	prj = cmds.workspace(q=1,fullName=1)
	outFiles = []
	fileNodes = cmds.ls(typ='file')


	for fnode in fileNodes:
		result = cmds.getAttr(fnode+'.fileTextureName')	

		if result[ 0 : len(prj) ] != prj and result[ 0 : 12 ] != 'sourceimages':
			outFiles.append(fnode)

	cmds.select(outFiles)


def selUnused(*args):

	fileNodes = cmds.ls(typ='file')
	materials = cmds.ls(mat=1) + cmds.ls(typ='shadingEngine') + cmds.ls(typ='locator')
	conns = []

	selectNodes = []

	for node in fileNodes:
		conn = cmds.listHistory( node ,f=1)
		conns.append(conn)


	for i in conns:
		for x in i:
			if x in materials:
				if selectNodes.count(i[0]) < 1:
					selectNodes.append( i[0] )

	fileMix = fileNodes + selectNodes
	fileSelection = []

	for y in fileMix:
		if fileMix.count(y) == 1:
			fileSelection.append(y)

	cmds.select(fileSelection)


def selUnusedNumb():

	fileNodes = cmds.ls(typ='file')
	materials = cmds.ls(mat=1) + cmds.ls(typ='shadingEngine') + cmds.ls(typ='locator')
	conns = []

	selectNodes = []

	for node in fileNodes:
		conn = cmds.listHistory( node ,f=1)
		conns.append(conn)


	for i in conns:
		for x in i:
			if x in materials:
				if selectNodes.count(i[0]) < 1:
					selectNodes.append( i[0] )

	fileMix = fileNodes + selectNodes
	fileSelection = []

	for y in fileMix:
		if fileMix.count(y) == 1:
			fileSelection.append(y)

	return str( len(fileSelection) )




"""
----------------------
--- TABS  FUNCTION ---
----------------------
"""


def tabsFunc(*args):

	noItens = cmds.menu( widgets['tabsMenu'] , q=1,ia=1)
	allTabs = [ widgets['frameLayout_01'], widgets['frameLayout_02'], widgets['frameLayout_03'], widgets['frameLayout_04'] ]

	for item in noItens:
		if cmds.menuItem(item,q=1,rb=1):
			indxItem = noItens.index(item)

			for tab in allTabs:
				if allTabs.index(tab) != indxItem and indxItem < len(allTabs):
					cmds.frameLayout(tab, e=1, cl=1)
				else:
					cmds.frameLayout(tab, e=1, cl=0)


"""
OPEN REF
"""
def getFolder():
    return cmds.fileDialog2(fm=2,cap='Select the images folder',okc='Select')


def openRef(*args):


	# select folder
	folder = getFolder()



	# Raise renderView
	rview = cmds.getPanel( sty = 'renderWindowPanel' )

	queryRV()

	for i in cmds.lsUI(windows=1):
		if i == "renderViewWindow":
			cmds.showWindow(i)

	if queryRV() != 1:
		cmds.scriptedPanel(rview, e=1, tearOff=1)


	# clean rview

	if cmds.scriptedPanel(rview , q=True, mbv=1 ):
		toggle()

	for img in os.listdir(folder[0]):
		#print folder[0] + '/' +img
		cmds.renderWindowEditor( rview, e=True, li=folder[0] + '/' +img )
		mel.eval('renderWindowMenuCommand keepImageInRenderView renderView;')


def openImgTemp(*args):
	CurrentProject = cmds.workspace(q=1,fullName=1)
	path = CurrentProject + '/images/tmp/'
	os.startfile(path)

def renameDup(*args):

	selection = cmds.ls(sl=1)

	if selection != []:
		for z, obj in enumerate( selection ):

			if obj[-1] != cmds.listRelatives(obj,s=1)[0][-1]:
				cmds.rename(obj,'geo_'+str(z))

	else:
		cmds.warning('Empty selection')


def dupShapes(*args):
	dupShapes = []

	for y in cmds.ls(sl=1):
		if len(cmds.listRelatives(y,pa=1)) > 1:
			dupShapes.append(cmds.listRelatives(y,pa=1)[1])

	if dupShapes != []:
		cmds.select(dupShapes)
		cmds.warning('Confirm your selection and delete')
	else:
		cmds.warning('No dulicated shapes')




"""
---------------
Fresnel Formula
---------------
"""

def IOR(n,k):

	theta_deg = 0

	n = n
	k = k
	fresnel = []

	while theta_deg <= 90:
		theta = math.radians(theta_deg)
		a = math.sqrt((math.sqrt((n**2-k**2-(math.sin(theta))**2)**2 + ((4 * n**2) * k**2)) + (n**2 - k**2 - (math.sin(theta))**2))/2)
		b = math.sqrt((math.sqrt((n**2-k**2-(math.sin(theta))**2)**2 + ((4 * n**2) * k**2)) - (n**2 - k**2 - (math.sin(theta))**2))/2)

		Fs = (a**2+b**2-(2 * a * math.cos(theta))+(math.cos(theta))**2)/ \
		     (a**2+b**2+(2 * a * math.cos(theta))+(math.cos(theta))**2)
		Fp = Fs * ((a**2+b**2-(2 * a * math.sin(theta) * math.tan(theta))+(math.sin(theta))**2*(math.tan(theta))**2)/ \
			  (a**2+b**2+(2 * a * math.sin(theta) * math.tan(theta))+(math.sin(theta))**2*(math.tan(theta))**2))
		R = (Fs + Fp)/2

		fresnel.append(R)

		theta_deg += 1
	return fresnel



"""
-----------------------
Ramer Douglas Algorithm
-----------------------
"""



def _vec2d_dist(p1, p2):
	return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def _vec2d_sub(p1, p2):
	return (p1[0]-p2[0], p1[1]-p2[1])


def _vec2d_mult(p1, p2):
	return p1[0]*p2[0] + p1[1]*p2[1]


def ramerdouglas(line, dist):

	if len(line) < 3:
		return line

	(begin, end) = (line[0], line[-1]) if line[0] != line[-1] else (line[0], line[-2])

	distSq = []
	for curr in line[1:-1]:
		tmp = (
			_vec2d_dist(begin, curr) - _vec2d_mult(_vec2d_sub(end, begin), _vec2d_sub(curr, begin)) ** 2 / _vec2d_dist(begin, end))
		distSq.append(tmp)

	maxdist = max(distSq)
	if maxdist < dist ** 2:
		return [begin, end]

	pos = distSq.index(maxdist)
	return (ramerdouglas(line[:pos + 2], dist) + 
			ramerdouglas(line[pos + 1:], dist)[1:])


"""
---------------------------
Draw Fresnel Curve | Single
---------------------------
"""


def drawCurve(*args):

	nValue = cmds.floatField( 'nVal' , q=1,v=True)
	kValue = cmds.floatField( 'kVal' , q=1,v=True)

	if nValue > 0:

		# create remapValue node
		remapNode = cmds.shadingNode('remapValue',asUtility=1)

		# Calculate Fresnel Curve
		fresnelList = IOR( nValue, kValue )


		# Compensate for non-linear facingRatio
		linearValues = [ float(i)/90 for i in range(91) ]
		rawValues = [ math.sin(linearValues[i]*90*math.pi/180) for i in range(91) ]
		rawValues.reverse()


		# Reduce curve points
		myline = zip(rawValues, fresnelList)
		precisionVals = [0.00005,0.0001,0.0002,0.0003]
		simplified = []

		for i in precisionVals:
			if len(simplified) == 0 or len(simplified) > 50:
				simplified = ramerdouglas(myline, dist = i)



		# Remove default values
		cmds.removeMultiInstance(remapNode+'.value[0]', b=1)
		cmds.removeMultiInstance(remapNode+'.value[1]', b=1)


		# Draw curve on remapValue Editor
		for i in simplified:
			currentSize = cmds.getAttr(remapNode +'.value',size=1)

			# First and last values with Linear interpolation
			if simplified.index(i) == 0 or simplified.index(i) == len(simplified)-1:
				cmds.setAttr( remapNode+'.value['+str( currentSize+1 )+']', i[0],i[1],1, type="double3")
			# Others with Spline interpolation
			else:
				cmds.setAttr( remapNode+'.value['+str( currentSize+1 )+']', i[0],i[1],3, type="double3")

	else:
		cmds.warning('N value must be greater than 0!')








def drawCurve2(*args):

	shaders = ['aiStandard','VRayMtl']

	if cmds.nodeType( cmds.ls(sl=1) ) not in shaders :
		cmds.warning('Select an aiStandard or a VRayMtl Material!')
		return False

	aiMetal = cmds.ls(sl=1)[0]

	redValues = [cmds.floatField( 'nValRED' , q=1,v=True),cmds.floatField( 'kValRED' , q=1,v=True)]
	greenValues = [cmds.floatField( 'nValGREEN' , q=1,v=True),cmds.floatField( 'kValGREEN' , q=1,v=True)]
	blueValues = [cmds.floatField( 'nValBLUE' , q=1,v=True),cmds.floatField( 'kValBLUE' , q=1,v=True)]

	allNnK = [redValues,greenValues,blueValues]

	if all(i > 0 for i in redValues) and all(i > 0 for i in greenValues) and all(i > 0 for i in blueValues):
	
		# create aditional nodes
		sInfo   = cmds.shadingNode('samplerInfo',asUtility=1)
		remapNodes = ['RED','GREEN','BLUE']


		# Compensate for non-linear facingRatio
		linearValues = [ float(i)/90 for i in range(91) ]
		rawValues = [ math.sin(linearValues[i]*90*math.pi/180) for i in range(91) ]
		rawValues.reverse()

		finalRemapList = []

		for remap in remapNodes:
			remapNode = cmds.shadingNode('remapValue', asUtility=1,n='remap_'+str(remap)+'')
			finalRemapList.append(remapNode)

			fresnelList = IOR( allNnK[remapNodes.index(remap)][0] , allNnK[remapNodes.index(remap)][1] )


			# Reduce curve points
			myline = zip(rawValues, fresnelList)
			precisionVals = [0.00005,0.0001,0.0002,0.0003]
			simplified = []

			for i in precisionVals:
				if len(simplified) == 0 or len(simplified) > 50:
					simplified = ramerdouglas(myline, dist = i)

			# remove default values
			cmds.removeMultiInstance(remapNode+'.value[0]', b=1)
			cmds.removeMultiInstance(remapNode+'.value[1]', b=1)

			# Draw curve on remapValue Editor
			for i in simplified:
				currentSize = cmds.getAttr(remapNode +'.value',size=1)

				# First and last values with Linear interpolation
				if simplified.index(i) == 0 or simplified.index(i) == len(simplified)-1:
					cmds.setAttr( remapNode+'.value['+str( currentSize+1 )+']', i[0],i[1],1, type="double3")
				# Others with Spline interpolation
				else:
					cmds.setAttr( remapNode+'.value['+str( currentSize+1 )+']', i[0],i[1],3, type="double3")

			
			# connect to network
			cmds.connectAttr(sInfo+'.facingRatio', remapNode+'.inputValue',f=1)


		# connect to Material
		if cmds.nodeType( aiMetal ) == 'aiStandard':
			cmds.connectAttr( finalRemapList[0]+'.outValue', aiMetal+'.KsColorR', f=1 )
			cmds.connectAttr( finalRemapList[1]+'.outValue', aiMetal+'.KsColorG', f=1 )
			cmds.connectAttr( finalRemapList[2]+'.outValue', aiMetal+'.KsColorB', f=1 )

		if cmds.nodeType( aiMetal ) == 'VRayMtl':
			cmds.connectAttr( finalRemapList[0]+'.outValue', aiMetal+'.reflectionColorR', f=1 )
			cmds.connectAttr( finalRemapList[1]+'.outValue', aiMetal+'.reflectionColorG', f=1 )
			cmds.connectAttr( finalRemapList[2]+'.outValue', aiMetal+'.reflectionColorB', f=1 )			

		# Affect Diffuse
		if cmds.nodeType( aiMetal ) == 'aiStandard' :

			if cmds.checkBox( 'checkDiff', q=1, v=1 ):
				cmds.setAttr(aiMetal+'.specularFresnel', 1)
				cmds.setAttr(aiMetal+'.Ksn', 1)
				cmds.setAttr(aiMetal+'.FresnelAffectDiff', 1)



	else:
		cmds.warning('N and K values must be greater than 0!')

	



def presetFresnel(*args):

	presets = [ ('Default',0,0,0,0,0,0),
				('Aluminium',1.55803,7.7124,0.84921,6.1648,0.72122,5.7556),
				('Gold',0.17009,3.1421,0.7062,2.0307,1.26175,1.8014),
				('Copper',0.21845,3.6370,1.12497,2.5834,1.15106,2.4926),
				('Silver',0.13928,4.1285,0.13,3.0094,0.13329,2.7028),
				('Chromium',3.1044,3.3274,2.85932,3.3221,2.54232,3.2521),
				('Platinum',2.37387,4.2454,2.00768,3.5017,1.90571,3.2893),
				('Nickel',2.01294,3.8059,1.69725,3.0186,1.65785,2.7993)
			  ]

	selected = cmds.optionMenu( 'opmenuIor',q=1, sl=1 )-1

	cmds.floatField( 'nValRED',e=1,v=presets[selected][1] )
	cmds.floatField( 'kValRED',e=1,v=presets[selected][2] )
	cmds.floatField( 'nValGREEN',e=1,v=presets[selected][3] )
	cmds.floatField( 'kValGREEN',e=1,v=presets[selected][4] )
	cmds.floatField( 'nValBLUE',e=1,v=presets[selected][5] )
	cmds.floatField( 'kValBLUE',e=1,v=presets[selected][6] )