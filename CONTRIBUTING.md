# Contributing

Thank you for your interest in contributing to the `wikipron` codebase!

This page assumes that you have already created a fork of the `wikipron` repo
under your GitHub account and have the codebase available locally for
development work. If you have followed
[these steps](https://github.com/CUNY-CL/wikipron#development),
then you are all set.

## Working on a Feature or Bug Fix

The development steps below assumes that your local Git repo has a remote
`upstream` link to `CUNY-CL/wikipron`:
   
```bash
git remote add upstream https://github.com/CUNY-CL/wikipron.git
```

After this step (which you only have to do once),
running `git remote -v` should show your local Git repo
has links to both "origin"
(pointing to your fork `<your-github-username>/wikipron`)
and "upstream" (pointing to `CUNY-CL/wikipron`).

To work on a feature or bug fix, here are the development steps: 

1. Before doing any work, check out the master branch and
   make sure that your local master branch is up-to-date with upstream master:
   
   ```bash
   git checkout master
   git pull upstream master
   ``` 
   
2. Create a new branch.
   This branch is where you will make commits of your work.
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
   create a pull request off of your branch against the `CUNY-CL/wikipron`
   repo.

6. Add an entry to
   [CHANGELOG.md](https://github.com/CUNY-CL/wikipron/blob/master/CHANGELOG.md),
   commit this change, and push this commit to your branch.

## Documentation

* If relevant, please update the top-level
  [README](https://github.com/CUNY-CL/wikipron/blob/master/README.md)
  for your changes.

* To document functions and class methods, please name them transparently and
  type them. If it helps, please add a one-liner docstring immediately
  under the function signature, in the form of `"""Docstring here"""` with
  triple double quotes. For more elaborate docstrings, please follow the
  [numpydoc docstring format](https://numpydoc.readthedocs.io/en/latest/format.html).

## Running Tests

The `wikipron` repo has continuous integration (CI) turned on,
with autobuilds running pytest and flake8 for the test suite
(in the [`tests/`](tests) directory) and code style checks, respectively.
If an autobuild at a pending pull request fails because of `pytest`, `flake8` or
`mypy` errors, then the errors must be fixed by further commits pushed to the
branch by the author.

If you would like to help avoid wasting free Internet resources
(every push triggers a new CI autobuild),
you can run the following checks locally before pushing commits:
* `mypy --ignore-missing-imports wikipron/ tests/ data/`
* `flake8 wikipron/ tests/`
* `black --line-length=79 --check wikipron/ tests/ data/`
    * You can fix any errors by running the same command without `--check`
* `pytest tests/`
