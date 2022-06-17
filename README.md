# MapTarget
Helps you find the nearest object 

## Description
This application gets object data through [overpy](https://github.com/DinoTools/python-overpy) 
(Wrapper to access the [Overpass API](https://python-overpy.readthedocs.io/en/latest/)),
[KD](https://en.wikipedia.org/wiki/K-d_tree) tree is used to find the nearest object to the point,
the result of the program is displayed using PyQt5

## Build
Enter the following commands to create an exe file:
```shell
pyinstaller --onefile  --noconsole --ico map-ico.ico .\main.py
```
```shell
xcopy .\resources .\dist\resources /E 
```