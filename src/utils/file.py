import os

def safe_write(path: str, contents: str):
    tmp = f"{path}.tmp"
    
    with open(tmp, 'w') as f:
        f.write(contents)
        
    os.replace(tmp, path)