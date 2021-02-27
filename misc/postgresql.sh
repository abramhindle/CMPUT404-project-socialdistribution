#!/bin/bash
database_password=12345678 # need to match the password in django settings
version=13.2-alpine # do not touch unless you know what you are doing
data_volume_name=postgresql_data_volume
container_name=postgres

if [[ $(whoami) != root ]]
then
    echo Is root user: no
else
    echo Is root user: yes
    echo You must run this script as non-root user!
    exit 1
fi
if [[ -n $(docker --version) ]]
then
    echo Docker installed: yes 
else
    echo Docker installed: no
    echo You must install Docker first!
    exit 1
fi
if [[  $(docker image list | grep postgres | awk '{print $2}') == $version ]]
then
    echo Postgresql $version image found: yes
else
    echo Postgresql $version image found: no
    echo Pulling now...
    docker pull postgres:$version
    echo Successfully pulled.
fi
if [[ -n $(docker volume ls | grep $data_volume_name) ]]
then
    echo Postgresql data volume found: yes
else
    echo Postgresql data volume found: no
    echo Creating now...
    docker volume create $data_volume_name
    echo Successfully created.
fi
if [[ -n $(docker container ls -a | grep $container_name | awk '{print $5}' | grep 'Exited') ]]
then
    docker container start $container_name
    echo Mountpoint is: $(docker volume inspect $data_volume_name | grep Mountpoint | grep -oE '(/\w+)+')
    exit 0
fi
if [[ ! -n $(docker container ls -a | grep $container_name) ]]
then
    docker run --name $container_name -v $data_volume_name:/var/lib/postgresql/data -e POSTGRES_PASSWORD=$database_password -p 5432:5432 -d postgres:$version
    echo Mountpoint is: $(docker volume inspect $data_volume_name | grep Mountpoint | grep -oE '(/\w+)+')
fi