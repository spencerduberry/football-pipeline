# Creating a feature

### At any point run
```shell
git status
```

to see what branch you're on and what files you have staged

### Run the following commands from your git bash shell
Checkout the dev branch:
```shell
git checkout dev
```

Pull the latest changes:
```shell
git pull
```

Create a new branch with a type and a description in snake_case:

```shell
git checkout -b "type/desc"
```

e.g:

```shell
git checkout -b "feat/new_transformation"
```

### Types of branch:
- `feat`: feature
- `fix`: a bug fix

# Once on your new branch

run:
```shell
uv sync ; uv venv ; source .venv/bin/activate
```

# Complete the feature for the ticket
Make the changes you need to make for the feature you're working on.

# After you've made your changes

### Add a specific file

```shell
git add name_of_the_file.py
```

### Or add all the modified files (if the file existed on the repo already):

```shell
git add -u
```

### Commit the changes with a conventional commit message

(prefixed with [feat, fix, test, docs, style, ci, build] and a colon):

```shell
git commit -am "feat: my message"
```

### If the pre-commits fail, run the same command again to see the things that weren't auto-fixable:

```shell
git commit -am "feat: my message"
```


### Once the pre-commits pass push to the branch
```shell
git push
```

If the branch doesn't already exist you may have to run

```shell
git push --set-upstream origin "your/branch_name"
```


# Lazy approach:
Put this function in a scratch file and use it to combine all the steps above before working on the feature:
```python
def create_new_feature(branch_name: str) -> None:
    cmd = [
        "git checkout dev",
        "git pull",
        f'git checkout -b "{branch_name}"',
        f'git push -u origin "{branch_name}"',
        "uv venv",
        "source .venv/bin/activate",
        "uv sync --all-packages",
        "uv run pre-commit install",
    ]
    print("\n".join(cmd))


create_new_feature("feat/some_branch")
```
### output
copy the output into your git bash shell and run it to set up your dev environment
```shell
git checkout dev
git pull
git checkout -b "feat/some_branch"
git push -u origin "feat/some_branch"
uv venv
source .venv/bin/activate
uv sync --all-packages
uv run pre-commit install
```
