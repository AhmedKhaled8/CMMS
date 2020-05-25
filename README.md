# CMMS 
### Team Members:

| Name   | Section    | B.N. |
|--------|------------|------|
| Ahmed Khaled    | 1 | 4  |
| Bassam Moustafa  | 1  | 22 |
| Shaden Ahmed   | 1  | 44  |
| Tarek Allam | 2 | 2|

##### For details, please check the report in ```CMMS_report.pdf```. It contain a brief of the application with screenshots provided of the results.
##### Video that explains the work flow of the applicaion: [video](https://drive.google.com/file/d/1QBW1b_XIxGKN8yEGeF-j1wwepOGL1sd2/view)
##### The database used in the project including the managers, techniciains, reports, and devices in ```cmms.sql```
##### To use the application:
* Make sure that you have installed the packages in ```dependents.txt```
* Make sure that the sql server is running on your device.
* In line 37 in ```application.py```, change the username and password of your sql server as the following:
    * ```engine = create_engine("mysql+pymysql://{username}:{password}@localhost/CMMS",echo = None)```
* For example our username and password are ```root``` and ```sqldata```, so the line 37 would be like this:

    * ```engine = create_engine("mysql+pymysql://root:sqldata@localhost/CMMS",echo = None)```
* Using ```flask```, set the ```FLASK_APP``` to ```application.py``` through terminal either on
  * Linux: ```export FLASK_APP=application.py```
  * Windows (Use the command window not the shell): ```set FLASK_APP=application.py```
* Run the flask application by typing in command line ```flask run```

