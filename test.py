from main import FilesDatabase
import timeit 
FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/venv-windows" # 6s, 1654 # PERFECT
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/MetalColor" #8s, 2046
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/github-explore/requests"

#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"

#timeit.timeit(lambda:FilesDatabase.create(".."),number=3)
print(timeit.timeit(lambda:FilesDatabase.create(FILE),number=1))
# BIG OPTIMIZATION: 1.25 -> 0.25, wow 5x faster
#print(FilesDatabase.create(".."))
##db = FilesDatabase.create("..")##
while True:pass

    