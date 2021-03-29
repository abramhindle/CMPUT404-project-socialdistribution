# Miscellaneous

Some odds and ends.

1. `Name`: postgresql.sh  
   `Description`: Setup PostgreSQL server locally using Docker.  
   `Note`: 
      * a. If Docker doesn't installed on your Mac, `brew install --cask docker`, then `open /Applications/Docker.app`.  
      * b. How to remove docker volume: `docker volume rm postgresql_data_volume`  

   `Usage`: `chmod +x postgresql.sh && ./postgresql.sh`
2. `Name`: predeploy.sh  
   `Description`: As its name suggests, this script will setup everything needed before deploy.  
   `Usage`: `chmod +x predeploy.sh && ./predeploy.sh`  
   `Note`: This script depends on the project file struct, so please do not change file structure unless you know what you are doing.

3. `Name`: deploy.sh  
   `Description`: As its name suggests, this script will deploy the app on heroku.  
   `Usage`: `chmod +x deploy.sh && ./deploy.sh`  
   `Note`:
      * a. This script depends on the project file struct, so please do not change file structure unless you know what you are doing.  
      * b. You should change the scripts variable herokuappname to your own app name (eg. herokuappname=yourappname).    
4. `Name`: createsu.sh    
   `Description`: Create an superuser on the remote deployed heroku app.    
   `Usage`: `chmod +x createsu.sh && ./createsu.sh`    
   `Note`:
      * You should change the scripts variable herokuappname to your own app name (eg. herokuappname=yourappname).
5. `Name`: gen.py    
   `Description`: Generate http basic auth header.    
   `Usage`: `python3 gen.py`    
   `Note`:
      * You should using python3 to run the script.
6. `Name`: env.py    
   `Description`: Environment variables used when deploy.    
   `Usage`: `python3 env.py`    
   `Note`:
      * a. Before use, you should change the configurations accordingly.
      * b. This will simply print out a base64 encoded string.
      * c. Usually this script will be used with deploy.sh at the same time.
