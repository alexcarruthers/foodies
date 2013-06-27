foodies
=======
ECSE 428 Project - Foodies Social Network

Assumptions
-----------
You are on a mac with brew installed or you are on a Ubuntu 12.04 and greater.

How to set up your Development Environment
------------------------------------------
* Run the ```devscripts/install.sh``` or ```devscripts/install_mac.sh``` scripts to bootstrap your environment.
* You should add the ```virtualenvwrapper``` script referenced in devscripts/install.sh runs to your bashrc or zshrc.
The location of this file may change depending on your linux or mac distribution. Restart your terminal and you should
be able to run the command ```workon foodies``` with no error.This will activate the foodies virtual environment.
* Run ```pip install -r requirements.txt``` from the root project directory. This will download all the python
dependencies for the project.
* Run the postinstall script from the root project directory to handle django-related project setup.

Note: For windows, there is no equivalent to the postinstall script... you will have to manually run
the appropriate commands. Windows is not supported beyond a simple .bat install script.
