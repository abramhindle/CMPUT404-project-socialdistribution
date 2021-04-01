# Deploy Steps

1. Change frontend/src/requests/URL.js file, change domain, remotedomain, port, etc.
2. Change backend/presentation/Viewsets/URL.py file, change domain and remotedomain.
3. Run misc/predeploy.sh
4. Change misc/deploy.sh file, herokuappname should be your heroku app name.v