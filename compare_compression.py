import pandas as pd
import time
import os

DATA_DIR = "data"


def compare(df):
    """
    Compare the size and time of different file formats for a given DataFrame."""
    items = []
    sizes = []
    times = []
    tt = time.time()

    def export(item,function):
        print(f"Exporting {item}...")
        file = os.path.join(DATA_DIR,item)
        function(file)
        tt2 = time.time()
        times.append(round(tt2-tt,3))


        items.append(item)
        size = os.path.getsize(file)
        sizes.append(size)

        return tt2
    
    tt=export("data.feather", lambda file: df.to_feather(file))
    tt=export("data.csv", lambda file: df.to_csv(file, index=False))
    tt=export("data.pkl", lambda file: df.to_pickle(file))



    for engine in ("pyarrow", "fastparquet"):
        for compression in ("gzip", "brotli", "snappy", "lz4", "zstd"):
            tt=export(f"data-{engine}-{compression}.parquet", lambda file: df.to_parquet(file, engine=engine, compression=compression))
            
    items.append("memory-usage")
    sizes.append(df.memory_usage(deep=True).sum())
    times.append(0)

    return pd.DataFrame({"item": items, "size": sizes, "time": times})


import main
db = main.read_csv("db-all.csv")
df_comparison = compare(db)
df_comparison.to_csv("comparison.csv", index=False)