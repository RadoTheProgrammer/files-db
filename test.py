from main import FilesDatabase
import timeit 
FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/venv-windows" # 6s, 1654 # PERFECT
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/MetalColor" #8s, 2046
FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/github-explore/requests"
FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/Rpy-mc"

#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"

#timeit.timeit(lambda:FilesDatabase.create(".."),number=3)
#print(timeit.timeit(lambda:FilesDatabase.create(FILE),number=5))
db=FilesDatabase.create("/Users/alain/Library/CloudStorage/OneDrive-EducationVaud")
db.to_csv("db-all.csv")
print("ended")
# BIG OPTIMIZATION: 1.25 -> 0.25, wow 5x faster

# another optimization: 0.25 -> 0.11

# another optimization (by adding string dtype for name/index)
#print(FilesDatabase.create(".."))
##db = FilesDatabase.create("..")##
while True:pass

    