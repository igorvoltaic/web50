# This is CS50W

Each pset is kept in a separate branch 



REMINDER TO MYSELF:
To commit a new problem new branch must be created

Example:
``` 
git checkout --orphan web50/projects/2020/x/0 
# A file must be added or copied into the working dir or branch won't be created
touch index.html
git rm -rf .
index.html
git add index.html
git commit -m 'initial commit'
```
