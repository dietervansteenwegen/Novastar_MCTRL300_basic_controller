############
Cleanup repo
############
- ``rm -r .git``
- ``rm -r .mypy_cache``
- ``rm -r .github``
- ``rm -r venv``

############
GIT init
############
- Create **EMPTY** repo on Github
- ``git init``
- ``git remote add origin git_prive:dietervansteenwegen/xxxxx``

############
SPHINX docs
############

- ``cd docs``
- ``sphinx-quickstart``
- copy/update conf.py parts
- add modules and usage to index.rst
- in source subdir, run ``sphinx-apidoc.exe --force --output-dir . ../.. ../../setup.py``

############
Prep VENV
############
----------
Linux
----------
- ``python3 -m virtualenv --python python3 venv``
- ``source .\venv\Scripts\activate``

----------
Windows
----------
- ``python -m venv venv``
- ``.\venv\Scripts\activate.bat``

----------
Afterwards
----------
- ``pip install yapf flake8 pre-commit rope flake8-bugbear tryceratops``
- ``pre-commit run --all-files``
- ``pre-commit install``

########
Others
########
- Rename module folder and script
- Write **README.md**
- Update **setup.py**
- update **conf.py** (Sphinx)
- Recreate **requirements.txt**
- write **usage.rxt**
- Update **requirements.txt**
- Remove this file


################
COMMIT/PUSH
################
- ``git add *``
- ``git status``
- ``git commit -m "initial commit"``
- ``git push -u origin master``
