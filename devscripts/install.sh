#!/bin/bash
echo "------------------------------------------------------------"
echo "Installing foodies Development Environment"
echo "------------------------------------------------------------"

echo "------------------------------------------------------------"
echo "Installing Dependencies"
echo "------------------------------------------------------------"
sudo apt-get update
sudo apt-get install -y --force-yes gcc build-essential python-imaging curl libcurl4-openssl-dev unzip python-setuptools python-dev libboost-dev automake libtool flex bison pkg-config g++ lynx python-software-properties aptitude git
sudo apt-get install -y --force-yes python-yaml libxml2-dev libxslt-dev

echo "------------------------------------------------------------"
echo "Installing Python Environment"
echo "------------------------------------------------------------"
sudo easy_install virtualenv
sudo easy_install pip
sudo pip install virtualenvwrapper
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh

echo "------------------------------------------------------------"
echo "Installing Python Packages"
echo "------------------------------------------------------------"
mkvirtualenv foodies
pip install --use-mirrors -r ../requirements.txt

echo "------------------------------------------------------------"
echo "Completed foodies Development Environment"
echo "------------------------------------------------------------"

