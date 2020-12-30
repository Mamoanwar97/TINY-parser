# TINY-Scanner

## Setup
To run it you need to create conda enviroment first:

```
conda create -n <enviroment-name> python=3.7.5
```
Then be sure to download PySide2 and shiboken2 of the same version
```
pip install pyside2@5.15.1 
```
If shiboken2 didnt install directly use this command:
```
pip install shiboken2@5.15.1 
```
Now you need to download pygraphviz
```
conda install -c alubbock pygraphviz
```
or for linux:
```
sudo apt-get install graphviz graphviz-dev
pip install pygraphviz
```
if you faced an error for '.png', run this command inside your enviroment:
```
dot -c
```

## Run
Now after installing everything, be sure that you activated your enviroment
```
conda activate <enviroment-name>
```
and from inside of your enviroment and from inside of this folder run 
```
python TINY_Scanner.py
```
