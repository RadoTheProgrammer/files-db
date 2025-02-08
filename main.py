import os
import datetime
import subprocess
import json
import platform
import pandas as pd


file_path = "/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/coding/projects-data-analysis.csv"
file_path = "test.py"

# st = os.stat(file_path)
# print("st_atime",datetime.datetime.fromtimestamp(st.st_atime))
# print("st_mtime",datetime.datetime.fromtimestamp(st.st_mtime))
# print("st_ctime",datetime.datetime.fromtimestamp(st.st_ctime))

"""
Results:
st_atime 2025-02-07 22:02:17.452634
st_mtime 2025-02-07 22:01:39.648626
st_ctime 2025-02-07 22:01:40.297824
"""
system = platform.system()
print(system)


def get_stats(file):
    st = os.stat(file)
    st_dict = {}
    
    for name in dir(st):
        if name.startswith("st"):
            st_dict[name] = getattr(st,name)
            
    return st_dict
def print_stats(file):
    print(json.dumps(get_stats(file), indent=4))
        
def timeline(src:str,dst:str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    if src.endswith("/"):
        src=src[:-1]
        
    lsrc=len(src)+1

    if system=="Windows":
        def get_creation_time(st,path):
            return st.st_ctime
    elif system=="Darwin":
        def get_creation_time(st,path):
            return st.st_birthtime
    elif system=="Linux":
        def get_creation_time(st,path):
            try:
                return subprocess.check_output(['stat', '-c', '%W', path]).decode().strip()
            except Exception:
                return None
            
    def process(pathbase):

        pathname = os.path.join(rootname,pathbase)
        path = os.path.join(root,pathbase)
        
        st=os.stat(path)
        creation_time = datetime.datetime.fromtimestamp(get_creation_time(st, path))
        modification_time = datetime.datetime.fromtimestamp(st.st_mtime)
        dstpath = os.path.join(dst,str(creation_time.date())+".csv")
        
        if not os.path.exists(dstpath):
            with open(dstpath,"w") as f:
                f.write("path,creation_time,modification_time\n")
                
        with open(dstpath,"a") as f:
            f.write(f"{pathname},{creation_time},{modification_time}\n")
            
            
    for root,filenames,directories in os.walk(src):
        #print("QUOICOUBEH")
        rootname = root[lsrc:] # to remove the head
        filetype="F"
        for pathname in filenames:
            process(pathname)
            
        filetype="D"
        for pathname in directories:
            process(pathname)


class FilesDatabase(pd.DataFrame):
    def create(self,src):
        
        
        #print(rootname,filenames,directories)
        
#timeline("test.py","")
# try:
#     birth_time = subprocess.check_output(['stat', '-f', '%B', file_path]).decode().strip()
#     print("Creation Date:", datetime.datetime.fromtimestamp(int(birth_time)))
# except Exception as e:
#     print("Error:", e)
