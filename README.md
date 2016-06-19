# Boto Backup

A simple python script that backs up a psql database with AWS.

## What does it do?

It is a simple script that connects to a remote database, runs a database dump, and saves the dumpfile to an AWS account. It integrates easily with cron to run daily, hourly and every 15 minute database dumps. You can also run a one-off backup.

For my projects, I use this so that their is a unique daily file for each day, while the 15min and hourly files only include the data from the most recent run through.

## How do I use it?

* Clone the repo   
  * `git clone https://github.com/cmajel/boto-backup.git`
  
* Make a virtualenv for dependencies  
  * `virtualenv backups`  
  
* Install your dependencies
  * `pip install -r requirements.txt`
  
* Fill out the data in the config file. You will need:
  * a prefix for your filenames
  * Your psql credentials. Make sure your have dump privilages set up. If you haven't already done so, set up a `.pgpass` file so you are not prompted for your password. [Learn more about .pgpass here](https://www.postgresql.org/docs/9.3/static/libpq-pgpass.html)
  * Your AWS credentials and which bucket you would like to store them in
  
* Give it a test drive
  * `python backup_db.py`
  
* If all looks good, try setting it up to run at an interval with cron. [There is a sample cronjob here](https://github.com/cmajel/boto-backup/blob/master/sample_crontab.txt)



