import main,main2
import timeit 
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding" # 6s, 1654 # PERFECT
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/MetalColor" #8s, 2046
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/github-explore/requests"
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud/zzzarchives/coding/Rpy-mc" 27380
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"
FILE=r"c:\Users\rrrad\OneDrive - Education Vaud\archives\coding\Rpy-mc"
FILE="."
#FILE="/Users/alain/Library/CloudStorage/OneDrive-EducationVaud"

# print(timeit.timeit(lambda:main2.create(FILE),number=1))
# print(timeit.timeit(lambda:main.FilesDatabase.create(FILE),number=1))

db = main.FilesDatabase.create(FILE)
db_data = db("data")
print(db.only_files())
print(db_data)
db.sort_values("size", ascending=False)
new_db=db.pin_columns("nls")
print(new_db)
#db.to_csv("db-Rpy-mc.csv")
#print(new_db)
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

    