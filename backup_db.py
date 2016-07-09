import sys
import os
import subprocess
from datetime import datetime
import argparse
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from config import *

def get_type():
  # listen for type
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--type', 
    metavar='T', 
    type=str, 
    help='specify if this is an minute15, hourly, or daily backup')

  args = parser.parse_args()
  return args.type

def get_filename():
  #set up directory
  if not os.path.exists(directory_name_for_temp_backups):
    os.makedirs(directory_name_for_temp_backups)

  # get dates for filename
  now = datetime.now()
  date = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
  hour = str(now.hour).zfill(2)
  minute = str(now.minute).zfill(2)
  second = str(now.second).zfill(2)

  # name the file
  filename = None
  filename_starter = filename_prefix + '-'

  if backup_type == 'hourly':
    filename = filename_starter + str(backup_type) + '-' + hour + '.sql'

  if backup_type == 'minute15':
    filename = filename_starter + str(backup_type) + '-' + minute + '.sql'

  if backup_type == 'daily':
    filename = filename_starter + str(backup_type) + '-' + date + '.sql'

  if backup_type == None:
    filename = filename_starter + date + '-'  + hour + ':'  + minute + ':' + second + '.sql'
  
  return filename

def get_db_dump():
  print "starting db dump"
  filename = get_filename()

  dump = subprocess.Popen(['pg_dump', 
    '--dbname', dbname, 
    '--username', username, 
    '--port', port, 
    '--host', host, 
    '--file',filename], 
    stdout=subprocess.PIPE)

  dump.wait()
  save_to_aws(filename)

  print "db dump completed"

def save_to_aws(filename):
  aws_conn = S3Connection(aws_access_key, aws_secret_access_key)
  bucket = aws_conn.get_bucket(aws_bucket)
  aws_dump = bucket.new_key(os.path.join(directory_name_for_temp_backups, filename))

  #if daily archive, save to a seperate folder
  if backup_type == 'daily':
    aws_dump = bucket.new_key(os.path.join(directory_name_for_temp_backups, directory_name_for_archive_backups, filename))
    
  aws_dump.set_contents_from_filename(filename)

  print "aws upload complete"

  delete_local_files(filename)

def delete_local_files(filename):
  os.remove(filename)
  print "local file deleted"

backup_type = get_type()
get_db_dump()
