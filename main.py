import os
import subprocess
import json
import platform
import pandas as pd
import stat
from tqdm import tqdm

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



def _get_ctime_windows(st,path):
    return st.st_ctime
def _get_ctime_darwin(st,path):
        return st.st_birthtime
def _get_ctime_linux(st,path):
    try:
        return subprocess.check_output(['stat', '-c', '%W', st,path]).decode().strip()
    except Exception:
        return None
    
if system=="Windows":
    _get_ctime = _get_ctime_windows
elif system=="Darwin":
    _get_ctime = _get_ctime_darwin
elif system=="Linux":
    _get_ctime = _get_ctime_linux
    

# def get_stats(file):
#     st = os.stat(file)
#     st_dict = {}
    
#     for name in dir(st):
#         if name.startswith("st"):
#             st_dict[name] = getattr(st,name)
            
#     return st_dict
# def print_stats(file):
#     print(json.dumps(get_stats(file), indent=4))

def _to_datetime(timestamp):
    return pd.to_datetime(int(timestamp), unit="s")
NAME="name"
SIZE="size"
ASTYPE = {
        "name":"string",
        "size":"int64",
        "n":"int64",
        "ctime":"datetime64[s]",
        "mtime":"datetime64[s]",
        "atime":"datetime64[s]",
        "level":"int64",
        "nls":"int64"
        }
class FilesDatabase(pd.DataFrame):
    @property
    def _constructor(self):
        return FilesDatabase

    @classmethod
    def create(cls,src,show_progression=True):
        #print(cls)


        #self = self[::-1]
        #print(type(self))

        def _process(relpath,path,level):
            """
            This is the core function of the whole program, the time the program takes depend on it
            so I optimize it as possible
            """
            if os.path.islink(path): # on va éviter de se casser la tête avec ces links
                return (0,0)

            st=os.stat(path)

            size=st.st_size
            n=1
            
            if stat.S_ISDIR(st.st_mode): # equivalent to isdir
                levelitem = level+1
                ls = os.listdir(path)
                for item in ls:
                    size_add,n_add = _process(os.path.join(relpath,item),os.path.join(path,item),levelitem)
                    size+=size_add
                    n+=n_add
                    pbar.update(1)
                nls = len(ls)
            else:
                nls = -1

            data["name"].append(relpath)
            data["size"].append(size)
            data["n"].append(n)
            data["ctime"].append(_get_ctime(st,path))
            data["mtime"].append(st.st_mtime)
            data["atime"].append(st.st_atime)
            data["level"].append(level)
            data["nls"].append(nls)

            return size,n
        
        # end of the core function
        
        
        if show_progression:
            #print("Calculating total for progression...")
            total = sum(map(lambda d:len(d[1])+len(d[2]),os.walk(src)))

        else:
            total=0
        
        data={"name":[],"size":[],"n":[],"ctime":[],"mtime":[],"atime":[],"level":[], "nls":[]}
        with tqdm(total=total,disable=not show_progression) as pbar:
            _process("",src,0)
        
        self=cls(cls(data)[::-1].reset_index(drop=True).astype(ASTYPE))
        self._remove_blank_name()
        return self
    @classmethod
    def read_csv(cls,file):
        self = cls(pd.read_csv(file).astype(ASTYPE))
        self._remove_blank_name()
        return self

    def ls(self):
        return self[self["level"]==1]

    def _remove_blank_name(self):
        self.loc[:,"name"]=self["name"].map(lambda name:name if name else ".")

    def __call__(self,item:str): # at start used __getitem__ but it would cause conflict
        item = item.strip(os.sep)

        if item not in self.name.values:
            print(".git" in self.name)
            print("__pycache__" in self.name)
            raise FileNotFoundError(item)
        
        self = self[(self.name == item) | (self.name.str.startswith(f"{item}{os.sep}"))]
        self.loc[:,"level"]-=item.count(os.sep)+1
        self.loc[:,"name"] = self.name.str[len(item)+1:] #remove the head
        self._remove_blank_name()
        return self

    def pin_columns(self,*cols_to_pin):
        cols = list(self.columns)
        for n,col in enumerate(cols_to_pin):
            #n+=1 # if name is a normal column
            cols.remove(col)
            cols.insert(n,col)
            
        print(cols)
        return self[cols]

    def only_dirs(self):
        return self[self["nls"]!=-1]
    
    def only_files(self):
        return self[self["nls"]==-1]

create = FilesDatabase.create
read_csv = FilesDatabase.read_csv
            
        
        
            
        
