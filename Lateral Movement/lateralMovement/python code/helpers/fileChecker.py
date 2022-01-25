from pathlib import Path
import os

def fileExists(path):
    my_file = Path(path)
    if my_file.is_file():
        # file exists
        return True
    else:
        return False

def createPath(path):
    try:
        os.makedirs(path);
    except OSError:
        print("Failed to create path: " + path);
    else:
        print: ("Successful create path: " + path);

def existsDirectory(path):
    return os.path.isdir(path);


