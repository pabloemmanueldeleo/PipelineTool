global  proc string createWaterMark(){
	string $curPane;
	$curPane = `getPanel -withFocus`;
	if ($curPane == "scriptEditorPanel1"){$curPane = "modelPanel4";}
	string $cam;
	$cam = `modelPanel -q -cam $curPane`;
	$trfC = `listRelatives -ap $cam`;
	string $nodoImp="";string $trfIP[];string $trfIP_Ren="";


	if (`objExists "WATERMARK__IMPSH"`==0){
		$nodoImp = `createNode imagePlane -n "WATERMARK__IMPSH"`;
		$trfIP = `listRelatives -ap $nodoImp`;
		$trfIP_Ren = `rename $trfIP[0] "WATERMARK__IMP"`;
		parent $trfIP_Ren $trfC;
		string $imagePlaneFile;
		$imagePlaneFile = "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/MARKWATER.png";
		setAttr ( $nodoImp + ".imageName" ) -type "string" $imagePlaneFile;
		connectAttr -f ( $nodoImp + ".message" ) ( $cam+".imagePlane[0]" );
		AEinvokeFitFilmGate ( $cam + ".sizeX") ( $nodoImp + ".sizeY" );
		setAttr ( $nodoImp + ".fit" ) 1;
		setAttr ( $nodoImp + ".coverageX" ) 1920;
		setAttr ( $nodoImp + ".coverageY" ) 1080;
		setAttr ( $nodoImp + ".imageCenterZ" ) -19.800;
		setAttr ( $nodoImp + ".width" ) 19.2;
		setAttr ( $nodoImp + ".height" ) 10.8;
		setAttr ( $nodoImp + ".displayMode" ) 3;
		setAttr ( $nodoImp + ".colorOffset" ) -type double3 0 0 0 ;
		setAttr ( $nodoImp + ".alphaGain" ) 0.15;
		setAttr ( $nodoImp + ".depth" ) 1;
	}else{warning ( "YA EXISTE UN IMAGEPLANE" ); delete "WATERMARK__IMP";}
	return $nodoImp;
}
createWaterMark()
