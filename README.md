# Features list

* build `symmetry table` (local space vertices position)
* build `symmetry table` (topology)
* get selected vertices (to work only on selection)
* reset selection (to work on the whole object)
* flip selected mesh (or `mesh to modify` if nothing is selected)
* redo

# maya sym mesh
This is a Maya project for mesh modification, including unittest setup

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