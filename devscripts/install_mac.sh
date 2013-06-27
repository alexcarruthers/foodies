#!/bin/bash
echo "------------------------------------------------------------"
echo "Installing foodies Development Environment On Mac"
echo "------------------------------------------------------------"

echo "------------------------------------------------------------"
echo "Installing Dependencies"
echo "------------------------------------------------------------"
brew install libyaml libmemcached

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
mkvirtualenv --no-site-packages foodies
workon foodies
pip install --use-mirrors -r ../requirements.txt

echo "------------------------------------------------------------"
echo "Completed foodies Development Environment"
echo "------------------------------------------------------------"

