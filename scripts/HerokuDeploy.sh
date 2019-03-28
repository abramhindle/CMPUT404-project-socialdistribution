cd ../

cd backend
git add -A
git commit -a -m "Redeploying Back End to Heroku"
git push heroku master
heroku run --app radiant-savannah-77591 python manage.py migrate

cd ../
cd frontend
git add -A
git commit -a -m "Redeploying Front End to Heroku"
git push heroku master


