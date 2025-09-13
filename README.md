# Capstone-Prioritizer
An event prioritizing application with personalization through system training
# title
## subtitle
### sub-subtitles
This text is **bolded**  
![This is the alt text, this image is the welcome image to the readme](Images/readme/Welcome.jpg)


To engage the venv:
source venv/Scripts/activate





Make sure the MySQL server is running on the computer
windows > services
Setup the mysql instance
//need to use program files path because MySQL is not in PATH
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < setup_db.sql


If MySQL becomes corrupted, 
delete the data folder 
reinitialize the service:
mysqlid --initialize





Installing MySQL:
https://dev.mysql.com/downloads/installer/
get non web version
select full install for any development purposes
    //Should be able to select servers only if final executable version


Navigate to the setup_db.sql file folder and run //if mysql is in path
mysql -u root -p < setup_db.sql
//setup_db.sql will create a user, create the database, and define the schema after this has been run, the application should be able to connect to the setup db


