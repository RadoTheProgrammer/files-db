Create a database of all the items of a directory

# Installation
Clone the repo: `git clone https://github.com/RadoTheProgrammer/tetris`
Install the dependencies: `pip install -r requirements.txt`

# Usage
Create the database:
```python
import main
db = main.FilesDatabase.create(<your src>)
```
It is a table, a subclass of pandas dataframe, the columns are the following:
* name: name of the item, relative path
* size: size in bytes
* n: number of items and sub-items
* ctime: creation time
* mtime: modification time
* atime: last access time
* level: how deep the item is from the root
* nls: number of items (-1 if file)

You can use pandas native function `sort_values`

```python
db_size = db.sort_values("size",ascending=False) # Get which items takes the most place
db_timeline = db.sort_values("ctime") # Get a timeline of items by their creation date
```

Other features:
```python
db_ls = db.ls() # extract all root items
db_sub = db("foo/bar") # navigate in the database by getting into 1 specific item
db.only_dirs() # select only the dirs
db.only_files() # select only the files
db.pin_columns("nls") # pin a column(s) when you're more interested into a particular one

db.to_csv(<file>) # Export into a file
db = main.read_csv(<file>) # Import a database of file
```

And then you can save it into a file by `db.to_csv(<file>)` simply like pandas, and use a tool like Data Wrangler or Excel to view and analyse this data freely.