@ECHO OFF

@for /F "tokens=2 delims=:" %%i in ('"ipconfig | findstr IPv4"') do set LOCAL_IP=%%i
@echo Detected: Local IP = [%LOCAL_IP%]

::Agregar una variable global en window
set PYTHONPATH= ”c:\Program Files\Autodesk\Maya2015\bin\python.exe”;M:\PH_SCRIPTS\_MODULES;M:\PH_SCRIPTS\_PLUGINS;M:\PH_SCRIPTS\_SCRIPTS
set Path=C:\Python27\Lib\site-packages\PyQt4;C:\Python27\;C:\Python27\Scripts;C:\ProgramData\Oracle\Java\javapath;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files (x86)\Intel\iCLS Client\;C:\Program Files\Intel\iCLS Client\;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;C:\Program Files\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files\Intel\Intel(R) Management Engine Components\IPT;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\IPT;C:\Program Files\Common Files\Autodesk Shared\;C:\Program Files (x86)\Autodesk\Backburner\;C:\Program Files (x86)\QuickTime\QTSystem\;C:\Program Files (x86)\Windows Kits\8.1\Windows Performance Toolkit\;C:\Program Files\Microsoft SQL Server\110\Tools\Binn\;C:\Program Files (x86)\Microsoft SDKs\TypeScript\1.0\;M:\PH_SCRIPTS\_MODULES;M:\PH_SCRIPTS\_PLUGINS;
set solidangle_LICENSE=5053@server;
set golaem_LICENSE=5053@127.0.0.1;