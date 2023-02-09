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
Then, to run the backend use the following command:
```shell
python app.py
```

### Frontend

Install npm packages, eg:

```shell
cd frontend
npm i
```
To run the frontend use the following command. Make sure the backend is running as well.

```shell
npm run start
```

### pre-commit

CI runs linters on your code and checks will fail if there are any issues. To help identify/fix issues before you push,
you use the [pre-commit](https://pre-commit.com/) hooks. Ensure you have pre-commit PyPi package installed (it should be
installed already if you've completed backend setup), then run

```shell
pre-commit install
```

From now on, hooks will run _prior_ to committing, if the hooks modify files, you will have to recommit. If you do not
want the hooks to run hooks, you can unselect "Run Git hooks" when committing in an IntelliJ or commit
with `--no-verify` on the command line, or uninstall hooks entirely by running `pre-commit uninstall`.

The first time committing, hooks may take some time to install.

### Deployment to Heroku

TODO (MATT): do we want autopushes to Heroku via CI? this can be setup. In the meantime, manual deployments:

#### First time setup

- [Install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
- Run `heroku login`
- Add Heroku as a git remote: `heroku git:remote -a <existing-heroku-project-name>`

#### Deploying

- Run `npm build` in `./frontend` to build the React frontend
- Run `git push heroku <your current git branch>:master`
  - If your current git branch is `master` already, you can just write `git push heroku master`
  - You can use the following alias in your `.bashrc` to make this operation require less typing: `alias whateveruwant="git push heroku $(git branch --show-current):master"`

### Other Stuff

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
