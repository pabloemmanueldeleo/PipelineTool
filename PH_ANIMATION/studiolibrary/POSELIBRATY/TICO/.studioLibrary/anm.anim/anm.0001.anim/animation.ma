//Maya ASCII 2015ff05 scene
//Name: animation.ma
//Last modified: Fri, Jun 26, 2015 04:47:04 PM
//Codeset: 1252
requires maya "2015ff05";
requires -dataType "HIKCharacter" -dataType "HIKCharacterState" -dataType "HIKEffectorState"
		 -dataType "HIKPropertySetState" "mayaHIK" "1.0_HIK_2014.2";
requires -dataType "byteArray" "Mayatomr" "2015.0 - 3.12.1.18 ";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201410051530-933320-1";
fileInfo "osv" "Microsoft Windows 7 Ultimate Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode animCurveTL -n "CURVE1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 21 77.135963439941406;
createNode animCurveTL -n "CURVE2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 56.998172760009766 21 70.249069213867188;
createNode animCurveTL -n "CURVE3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 -0.68315881490707397 21 32.809822082519531;
createNode animCurveTA -n "CURVE4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 6.3611093629270335e-015 21 6.3611093629270335e-015;
createNode animCurveTA -n "CURVE5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 -6.3611093629270335e-015 21 -6.3611093629270335e-015;
createNode animCurveTA -n "CURVE6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 6.3611093629270335e-015 21 6.3611093629270335e-015;
// End