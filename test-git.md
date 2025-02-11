C

`git checkout <commit-id> `create a sandbox branch, in it, erases commits in this branch

`git checkout <commit-id> -- .`  undo it, just the files, and stage changes, stay in the branch

`git restore <file_name>` just undo the changes to stage, = discard on vs code

`git revert <commit-id>` revert just ONE commit (xd)

`git reset --hard <commit>` undo everything, but warning, erase commits

`git reset --soft <commit>`erase commits, but it doesn't edit files, it stage changes: the files are still the same, it's the git who changed

`git restore --source <commit> <file_name>` change just the files, not the git, without staging changes (like git checkout -- . but it doesn't stage)
