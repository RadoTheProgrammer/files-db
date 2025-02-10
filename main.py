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

if system=="Windows":

    def _get_ctime(st,path):
        return st.st_ctime
elif system=="Darwin":
    def _get_ctime(st,path):
        return st.st_birthtime
elif system=="Linux":
    def _get_ctime(st,path):
        try:
            return subprocess.check_output(['stat', '-c', '%W', st,path]).decode().strip()
        except Exception:
            return None
    

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
class FilesDatabase(pd.DataFrame):
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    
    _pbar = _data = None
    
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
                for item in os.listdir(path):
                    size_add,n_add = _process(os.path.join(relpath,item),os.path.join(path,item),levelitem)
                    size+=size_add
                    n+=n_add
                    pbar.update(1)
            
            #ctime=_get_ctime(st,path)
            #dnprint(pd.to_datetime(int(_get_ctime(st,path)), unit="s"))
            data["name"].append(relpath)
            data["size"].append(size)
            data["n"].append(n)
            data["ctime"].append(_get_ctime(st,path))
            data["mtime"].append(st.st_mtime)
            data["atime"].append(st.st_atime)
            data["level"].append(level)
            # a={
            #     "size":size,
            #     "n":n,
            #     "ctime": _to_datetime(_get_ctime(st,path)),
            #     "mtime": _to_datetime(st.st_mtime),
            #     "atime": _to_datetime(st.st_atime),
            #     "level": level
            # }
            # self.loc[relpath]=a # taking 4/5 !!
            return size,n
        
        # end of the core function
        
        
        if show_progression:
            #print("Calculating total for progression...")
            total = sum(map(lambda d:len(d[1])+len(d[2]),os.walk(src)))

        else:
            total=0
        
        data={"name":[],"size":[],"n":[],"ctime":[],"mtime":[],"atime":[],"level":[]}
        with tqdm(total=total,disable=not show_progression) as pbar:
            _process("",src,0)
        
        self=cls(cls(data)[::-1].astype({
            "ctime":"datetime64[s]",
            "mtime":"datetime64[s]",
            "atime":"datetime64[s]",
            "name":"string"
            }).set_index("name"))
        self._remove_blank_index()
        return self
            
    @classmethod
    def read_csv(cls,file):
        self = cls(pd.read_csv(file).astype({
            "ctime":"datetime64[ns]",
            "mtime":"datetime64[ns]",
            "atime":"datetime64[ns]",
            "name":"string",
            }
        ).set_index("name"))
        self._remove_blank_index()
        return self
    
    def ls(self):
        return type(self)(self[self["level"]==1])
    
    ASCENDING_AUTO = {
        "name":True,
        "size":False,
        "n":False,
        "ctime":True,
        "mtime":True,
        "atime":True,
        "level":True,
    }
    def sort(self,by="name",ascending="auto"):
        if ascending=="auto":
            ascending = self.ASCENDING_AUTO[by]
        return type(self)(self.sort_values(by=by, ascending=ascending))
    
    def _remove_blank_index(self):
        self.index=self.index.map(lambda name:name if name else ".")

    def __call__(self,item:str): # at start used __getitem__ but it would cause conflict
        item = item.strip("/")
        if item not in self.index:
            raise FileNotFoundError(item)
        
        db = type(self)(self[self.index.str.startswith(item)])    
        db.level-=1
        db.index = db.index.str[len(item)+1:] #remove the head
        db._remove_blank_index()
        return type(self)(db)
    
#db = FilesDatabase.read_csv("db.csv")
if __name__ == "__main__":
    #FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/ecole2" # 9s, 2263
    FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/venv-windows" # 6s, 1654 # PERFECT
    #FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/MetalColor" #8s, 2046
    #FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/github-explore/requests"
    
    #FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"
    db = FilesDatabase.create(FILE)


            #df.loc[]
                    
            
        
        
            
        
