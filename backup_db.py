import sys
import os
import subprocess
from datetime import datetime
import argparse
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from config import *

def get_filename():

  #set up directory
  if not os.path.exists('backups'):
    os.makedirs('backups')

  # get dates for filename
  now = datetime.now()
  date = str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2)
  hour = str(now.hour).zfill(2)
  minute = str(now.minute).zfill(2)

  # listen for type
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--type', 
    metavar='T', 
    type=str, 
    help='specify if this is an hourly or daily backup')

  args = parser.parse_args()
  backup_type = args.type

  # name the file
  filename = None
  filename_starter = filename_prefix + '-' + str(backup_type)

  if backup_type == 'hourly':
    filename = filename_starter + '-' + hour + '.sql'

  if backup_type == 'minute15':
    filename = filename_prefix + '-' + minute + '.sql'

  if backup_type == 'daily':
    filname = filename_starter + '-' + date + '.sql'
  
  return os.path.join('backups', filename)

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
  aws_dump = bucket.new_key(filename)
  aws_dump.set_contents_from_filename(filename)

  print "aws upload complete"

  delete_local_files(filename)

def delete_local_files(filename):
  os.remove(filename)
  print "local file deleted"

get_db_dump()

