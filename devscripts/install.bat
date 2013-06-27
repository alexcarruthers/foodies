ECHO ------------------------------------------------------------
ECHO Installing foodies Development Environment
ECHO ------------------------------------------------------------

ECHO ------------------------------------------------------------
ECHO Install Dependencies
ECHO ------------------------------------------------------------

CALL setuptools-0.6c11.win32-py2.7.exe
CALL easy_install virtualenv
CALL easy_install pip

ECHO ------------------------------------------------------------
ECHO Installing Python Packages 
ECHO ------------------------------------------------------------
ECHO CALL virtualenv ../ --no-site-packages
CALL virtualenv ../
CALL PIL-1.1.7.win32-py2.7.exe
CALL pip install --use-mirrors -E ../ -r ../requirements.txt

ECHO ------------------------------------------------------------
ECHO Completed foodies Development Environment
ECHO ------------------------------------------------------------
