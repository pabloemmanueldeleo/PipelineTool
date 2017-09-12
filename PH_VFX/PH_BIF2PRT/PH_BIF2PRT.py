import sys
path='M:\PH_SCRIPTS\_SCRIPTS\PyBat_0.1.2'
if not path in sys.path:
    sys.path.append(path)

import pybat
import subprocess
import os
#path=r'D:/Sims/E125/Prt_Bif/cache/bifrost/Bif2prt/'
path=r'D:/PH_SCRIPTS/SCENES_RIG/Bif2prt/'
#filepath=r'C:\Program Files\Autodesk\Maya2016\plug-ins\bifrost\devkit\bif2prt\bin'
filepath=r'C:/Program Files/Autodesk/Maya2015/plug-ins/bifrost/bin/bif2prt.bat'
outFolder='C:/coco/'

files = []

for name in os.listdir(path):
    if os.path.isfile(os.path.join(path, name)):
        files.append(name)

for file in files:
	archivo=str(path+file)
	outFolder=outFolder+file.split('.')[0]+'.prt'
	p = subprocess.Popen([filepath, '-f', archivo,outFolder])
