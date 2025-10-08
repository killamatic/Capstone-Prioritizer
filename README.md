# Capstone-Prioritizer
## Linear Regression Priority Prediction Event Scheduler
An event prioritizing application with personalization through machine learning

![Welcome image alt text](Images/readme/Welcome.jpg)


navigate to main on vscode start:
cd event_prioritizer/Capstone-Prioritizer/

To engage the venv: 
source venv/Scripts/activate

run the program
python main.py



if the pytest is not running, python executable may be taken from previous version on local machine, and disregard tkinter installation: (when inside venv)
where python
 Copy the path of the first instance from where python to the copy_python_path_here variable in the next command
"copy_python_path_here" -m pytest test_ui.py



Make sure the MySQL server is running on the computer
windows > services
Setup the mysql instance
//need to use program files path because MySQL is not in PATH
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < setup_db.sql
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < setup_db_updated.sql

from Capstone-prioritizer folder// where main is use this command to setup the db assuming that the MySQL setup was done according to the MySQL base settings
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < ./db/setup_db_updated.sql


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

had to install 
pip install -U scikit-learn for the ML, need to add this to the required softwares & requirements.txt
pip install mysql-connector-python faker pandas