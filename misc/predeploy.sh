#!/bin/bash
mkdir -p DeployMe
cd DeployMe
git init
cd ..
cp -r ../frontend/* DeployMe
cp -r ../backend/* DeployMe
cp Deploy/settings.py DeployMe/socialdist
cd DeployMe
yarn install
rm -rf build
rm -rf node_modules
git add .
git commit -m "Ready to deploy."
echo "Predeploy process complete!"
echo "You can find DeployMe folder in $(pwd)"