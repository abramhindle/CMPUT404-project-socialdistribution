# CMPUT404-project-socialdistribution

## Getting started


### Backend
Create and activate a python virtual environment and install from `requirements.txt`. For example:
```shell
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend: todo

### pre-commit
CI runs linters on your code and checks will fail if there are any issues. To help identify/fix issues before you push, you use the [pre-commit](https://pre-commit.com/) hooks. Ensure you have pre-commit PyPi package installed (it should be installed already if you've completed backend setup), then run
```shell
pre-commit install
```
From now on, hooks will run _prior_ to committing, if the hooks modify files, you will have to recommit. If you do not want the hooks to run hooks, you can unselect "Run Git hooks" when committing in an IntelliJ or commit with `--no-verify` on the command line, or uninstall hooks entirely by running `pre-commit uninstall`.

The first time commmitting, hooks may take some time to install.
### Deployment to Heroku

TODO (MATT)
See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!

## Contributing

Send a pull request and be sure to update this file with your name.

## Contributors / Licensing

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma
    Nhan Nguyen
