import os

def AppendTextToFile(filePath,text):
    with open(filePath,'a') as f:
        f.write(text)

def WriteTextToFile(filePath, text):
    with open(filePath,'w') as f:
        f.write(text)

def ReadTextFromFile(filePath):
    if not os.path.exists(filePath):
        return None
    with open(filePath,'r') as f:
        return f.read()