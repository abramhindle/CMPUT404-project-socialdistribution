# Heroku CLI Plugin for Heroku Exec

[![Circle CI](https://circleci.com/gh/heroku/heroku-ps-exec/tree/master.svg?style=svg)](https://circleci.com/gh/heroku/heroku-ps-exec/tree/master)
[![Build Status](https://travis-ci.org/heroku/heroku-ps-exec.svg?branch=master)](https://travis-ci.org/heroku/heroku-ps-exec)

For usage information see the [Heroku Exec documentation](https://devcenter.heroku.com/articles/heroku-exec).

<!-- commands -->
* [`heroku ps:copy FILE`](#heroku-pscopy-file)
* [`heroku ps:exec`](#heroku-psexec)
* [`heroku ps:forward PORT`](#heroku-psforward-port)
* [`heroku ps:socks`](#heroku-pssocks)

## `heroku ps:copy FILE`

Copy a file from a dyno to the local filesystem

```
USAGE
  $ heroku ps:copy FILE

OPTIONS
  -a, --app=app        (required) app to run command against
  -d, --dyno=dyno      specify the dyno to connect to
  -o, --output=output  the name of the output file
  -r, --remote=remote  git remote of app to use

DESCRIPTION
  Example:

       $ heroku ps:copy FILENAME --app murmuring-headland-14719
```

## `heroku ps:exec`

Create an SSH session to a dyno

```
USAGE
  $ heroku ps:exec

OPTIONS
  -a, --app=app        (required) app to run command against
  -d, --dyno=dyno      specify the dyno to connect to
  -r, --remote=remote  git remote of app to use
  --ssh                use native ssh
  --status             lists the status of the SSH server in the dyno

DESCRIPTION
  Example:

       $ heroku ps:exec 'node -i' --app murmuring-headland-14719
```

## `heroku ps:forward PORT`

Forward traffic on a local port to a dyno

```
USAGE
  $ heroku ps:forward PORT

OPTIONS
  -a, --app=app        (required) app to run command against
  -d, --dyno=dyno      specify the dyno to connect to
  -r, --remote=remote  git remote of app to use

DESCRIPTION
  Provide a port or comma-separated list of ports to forward.

       For example, "4000,9000:9001" will forward port 4000 to port 4000 and
       port 9000 to port 9001.

       Example:

       $ heroku ps:forward 8080 --app murmuring-headland-14719
```

## `heroku ps:socks`

Launch a SOCKS proxy into a dyno

```
USAGE
  $ heroku ps:socks

OPTIONS
  -a, --app=app        (required) app to run command against
  -d, --dyno=dyno      specify the dyno to connect to
  -r, --remote=remote  git remote of app to use

DESCRIPTION
  Example:

       $ heroku ps:socks --app murmuring-headland-14719
       Establishing credentials... done
       SOCKSv5 proxy server started on port 1080
       Use CTRL+C to stop the proxy
```
<!-- commandsstop -->
