#!/bin/bash
# Created: 2023.12.08
# Vladimir Vons, VladVons@gmail.com

py=python3.12
DirPy=~/virt/python3


VSCode()
{
    code --list-extensions

    code --force --install-extension ms-python.python
    code --force --install-extension ms-python.pylint 
    code --force --install-extension tabnine.tabnine-vscode
    code --force --install-extension shardulm94.trailing-spaces
    #code --force --install-extension fallenmax.mithril-emmet
    code --force --install-extension anteprimorac.html-end-tag-labels
    code --force --install-extension naumovs.color-highlight
}

Python()
{
    sudo apt update
    sudo apt dist-upgrade

    sudo apt install --no-install-recommends software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install --no-install-recommends $py $py-dev $py-distutils $py-venv virtualenv

    sudo apt install postgresql-plpython3-16
    su postgres -c "python3 -m pip install geoip2"
    service postgresql restart
}

PythonPkg()
{
    $py -m venv $DirPy
    source $DirPy/bin/activate

    pip3 install --upgrade pip
    pip3 install --requirement requires.lst
}

Clear()
{
  find $DirPy -type d -name "__pycache__" -exec rm -r {} +
  find ~/.vscode/extensions -type d -name "__pycache__" -exec rm -r {} +
  find -L ./src -type d -name "__pycache__" -exec rm -r {} +

  rm -rf ~/.config/Code/Cache
  rm -rf ~/.config/Code/CachedData
  rm -rf ~/.config/Code/User/workspaceStorage
}

#VSCode

#Python
PythonPkg
#Clear

