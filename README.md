# perp

## Environment Setup

The following instructions should help you setup your Python development
environment. 
 
### Install Python
Using homebrew on mac, 
```bash
> brew update
> brew install python 
```
Ensure that you have version `3.7.2` with,
```bash
> python --version
```

### Install PyCharm

It is strongly recommended that you use the PyCharm IDE as no 
instructions will be provided for any other editor. You can download 
PyCharm [here](https://www.jetbrains.com/pycharm/download/#section=mac).
You can use either the Community or Professional editions (professional 
is available free with a 
[student license](https://www.jetbrains.com/student/)). The proceeding
instructions will refer to the Community edition. 

Once you have PyCharm downloaded and installed, open the application 
and select `Open` from the home screen, then navigate the location of 
your clone of this repository. 

### Create Virtual Environment

This project uses `tox` to manage virtual environments. Install tox with,
```bash
> pip install tox
```
To create a `Python 3.7` virtual environment for the project run,
```bash
> tox -e py37
```
To configure Pycharm to point to your new virtual environment, 
* Navigate to your PyCharm preferences
* Select `Project: perp`
* Select `Project Interpreter`
* Click the gear icon and select `Add...`
* Select `Existing Interpreter`
* Click the `...` icon, and navigate to `/path/to/perp/.tox/py37/bin/python`
* Click `Ok`
