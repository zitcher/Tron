# Tron
CS 1410 Tron AI

## Testing a game:
`python gamerunner.py -bots [student/random/wall/ta1/ta2] [student/random/wall/ta1/ta2] -map [path to map]`

Example: `python gamerunner.py -bots student student -map maps/joust.txt`
# How to change branches
`git checkout -b [branch_name]`

# Commits
1. Go to folder `cd [path]`

2. Add changes `git add .`

3. Create a commit `git commit -m "[commit name]"`

4. push the commit `git push origin [branch-name]`

# How to make a PR
1. Go to folder `cd [path]`

2. Get up to date with master: `git checkout master`, `git pull origin master`,  `git checkout [branch_name]`, `git rebase master`

3. Fix all merge conflicts. There are many good tools out there!

4. Push the merge: `git push -f origin [branch-name]`

5. Go to the repository page: https://github.com/zachooz/Tron

6. Click create a pull request

7. Choose the correct branches
