PoseMan 1.3.5

Install:
Copy poseMan.mel into "/user/documents/maya/version/scripts", "/user/documents/maya/scripts" or whatever path that include MAYA_SCRIPT_PATH environment

Use:
type poseMan in maya command line and press enter or create a shelfbutton with poseMan command.

Notes:
When Poseman launched, create own projects directories from your current maya project, if your current maya project is for example "MyProject", poseman will create two directories: "maya/projects/MyProject/poseman" and "maya/projects/MyProject/poseman_trash"

If you want to put an image in poseman window, you have to edit poseMan.mel and put an url of bmp/xpm file in this line: 
	// ***********************************
	// POSEMAN LOGO
	// ***********************************
	$POSEMAN_LOGO = "/PATH/TO/BMP_XPM/LOGO.bmp";
	

Contact
hisconer@gmail.com

Blog
http://inartx.com/poseman/