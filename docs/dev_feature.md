# Creating a feature

### At any point run
`git status`

to see what branch you're on and what files you have staged

### Run the following commands from your git bash shell
Checkout the dev branch:
`git checkout dev`

Pull the latest changes:
`git pull`

Create a new branch with a type and a description in snake_case: 

`git checkout -b "type/desc"`

e.g:

`git checkout -b "feat/new_transformation"`

### Types of branch:
- `feat`: feature
- `fix`: a bug fix

# After you've made your changes

### Add a specific file

`git add name_of_the_file.py`

### Or add all the modified files (if the file existed on the repo already):

`git add -u`

### Commit the changes with a conventional commit message 

(prefixed with [feat, fix, test, docs, style, ci, build] and a colon):

`git commit -am "feat: my message"`

### If the pre-commits fail, run the same command again to see the things that weren't auto-fixable:

`git commit -am "feat: my message"`


### Once the pre-commits pass push to the branch
`git push`

If the branch doesn't already exist you may have to run

`git push --set-upstream origin "your/branch_name"`