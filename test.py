import main
import timeit 
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding" # 6s, 1654 # PERFECT
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/MetalColor" #8s, 2046
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/github-explore/requests"
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/Rpy-mc"
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"
FILE="."
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"

print(timeit.timeit(lambda:main.create(".."),number=1))
# db = main.create(FILE)
# new_db=db.pin_columns("nls")
# new_db=db(".git")
# print(new_db)
#main.create(".")
# BIG OPTIMIZATION: 1.25 -> 0.25, wow 5x faster

# another optimization: 0.25 -> 0.11

# another optimization (by adding string dtype for name/index)
#print(FilesDatabase.create(".."))
##db = FilesDatabase.create("..")##
input()

    