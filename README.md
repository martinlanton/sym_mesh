# Features to implement

* build `symmetry table` (local space vertices position)
* build `symmetry table` (topology)
* Change geometry operations from a push button to a slider + spinbox and use the mouseReleased message to store the current command into the undo history
* Geometry operations from target or from selection
* testing and push reject on github
* Pip integration

# Maya sym mesh
This is a Maya project for mesh modification, including unittest setup

## Installation
To install this package for your local maya, you can use the following command in a `TERMINAL` in **_ADMINISTRATOR MODE_**: 
```commandline
mayapy -m pip install {package location} -r {package location}/requirements.txt
```
Where `{package location}` represents the location you downloaded the package, for example :
```commandline
mayapy -m pip install D:/python/sym-mesh -r D:/python/sym-mesh/requirements.txt
```
If you have more than one maya version installed, you will need to replace `mayapy` with the full path to your `mayapy` executable file, like so : 
```commandline
"C:\Program Files\Autodesk\Maya2022\bin\mayapy.exe" -m pip install D:/python/sym-mesh -r D:/python/sym-mesh/requirements.txt
```
Note that you will have to put the path in quotation marks if there are any blank spaces in it as Windows can't handle those.

## Launch
You can currently launch the tool with the current command : 
```python
from gui import startup
startup.startup()
```


# Development

## How to install coverage on Maya?

### In short, on Windows, from an ***administrator*** command line :
```commandline
mayapy -m pip install --ignore-installed coverage
```
The `ignore-install` flag is a nice thing to know when you want to ensure you get the latest version or when the package in question is already installed somewhere else.

### On both macOS and Linux, the following command can be used :
```commandline
sudo ./mayapy -m pip install <flags> <package>
```

### For more information, the coverage documentation can be found here :
https://coverage.readthedocs.io/en/6.4.3/cmd.html#

## How to run coverage on Maya?
Coverage can be run on maya by calling the coverage executable with the maya interpreter, this would look something like this : 
```commandline
C:\Program Files\Autodesk\Maya2022\bin\mayapy "C:\Program Files\Autodesk\Maya2022\Python37\Scripts\coverage.exe" run --source=src -m unittest
```
It is important that the coverage executable be in quotes (") so that the interpreter can read it as a path.

Then the html report can be generated with the following command (that you can add to the tox `commands` section of the environments to run):
```commandline
coverage html -d coverage_html
```
