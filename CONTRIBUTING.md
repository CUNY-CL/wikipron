# Contributing

Thank you for your interest in contributing to the `wikipron` codebase!

## Setting Up A Development Environment

1. Create a fork of the `wikipron` repo on GitHub.
2. Make sure you are in some sort of a virtual environment
   (venv, virtualenv, conda, etc).
3. Download and install the library in the "editable" mode
   together with the core and dev dependencies within the virtual environment:

    ```bash
    git clone https://github.com/<your-github-username>/wikipron.git
    cd wikipron
    pip install --upgrade pip setuptools
    pip install -r requirements.txt
    pip install --no-deps -e .
    ```
   
4. Add the upstream `kylebgorman/wikipron` repo link:
   
   ```bash
   git remote add upstream https://github.com/kylebgorman/wikipron.git
   ```
   
   After this step, running `git remote -v` should show your local Git repo
   has links to both "origin" (pointing to your fork `<your-github-username>/wikipron`)
   and "upstream" (pointing to `kylebgorman/wikipron`).

## Working on a Feature or Bug Fix

1. Before doing any work, check out the master branch and
   make sure that your local master branch is up-to-date with upstream master:
   
   ```bash
   git checkout master
   git pull upstream master
   ``` 
   
2. Create a new branch. This branch is where you will make commits of your work.
   (As best practice, never make commits while on a master branch.
   Running `git branch` tells you which branch you are on.)
   
   ```bash
   git checkout -b new-branch-name
   ```
   
3. Make as many commits as needed for your work.
4. When you feel your work is ready for a pull request,
   push your branch to your fork.

   ```bash
   git push origin new-branch-name
   ```
5. Go to your fork `https://github.com/<your-github-username>/wikipron` and
   create a pull request off of your branch against the `kylebgorman/wikipron` repo.

## Running Tests

The `wikipron` repo has continuous integration (CI) turned on,
with autobuilds running pytest and flake8 for the test suite
(in [`test_wikipron.py`](test_wikipron.py)) and code style checks, respectively.
If an autobuild at a pending pull request fails because of pytest or flake8
errors, then the errors must be fixed by further commits pushed to the branch
by the author.

If you would like to help avoid wasting free Internet resources
(every push triggers a new CI autobuild),
you can run pytest and flake8 checks locally before pushing commits:

```bash
flake8 wikipron.py test_wikipron.py
pytest -vv test_wikipron.py
```
