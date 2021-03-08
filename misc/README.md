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