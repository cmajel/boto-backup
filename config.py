
# Naming -----------------------------------------------------------------
#   Your file names will be `filename_prefix-daily-YYYYMMDD` for daily
#   backups and `filename_prefix-hourly-HH` for hourly backups

filename_prefix = ''
directory_name_for_temp_backups = ''
directory_name_for_archive_backups = ''

## Database --------------------------------------------------------------

dbname = ''
username = ''
port = ''
host = ''

# remember to set up your .pgpass file
# https://www.postgresql.org/docs/9.3/static/libpq-pgpass.html
# Make sure you also adjust the permissions to read/write
# `chmod 0600 .pgpass`

## AWS Account -----------------------------------------------------------
aws_access_key = ''
aws_secret_access_key = ''
aws_bucket = ''
