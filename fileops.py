import os

# which files to look for in lib
def filter(name):
  return name.endswith(".py")

def listfiles(root):
  res = []
  
  for path, subdirs, files in os.walk(root):
    for name in files:
      fullpath = os.path.join(path, name)
      fullpath = fullpath.replace("\\", "/")
      if filter(fullpath):
        res.append(fullpath)
  
  return res

def read_lines(filepath):
    with open(filepath, 'r', encoding="utf8") as file: 
        data = file.read()
    return data.split('\n')