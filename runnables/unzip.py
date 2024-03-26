import zipfile
import sys
import glob

## ---------- Define Root Path ---------- ## 
ROOTPATH = '/Users/zhenggong/Documents/Github/IBES_selected/' # for importing and reference management 
sys.path.append(ROOTPATH)

file_paths = glob.glob('IBES_raw/*')
print(file_paths)

for filepath in file_paths:
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall('IBES_extracted/')

