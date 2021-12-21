# this file is for app "djnago-crontab"
# this help in scheduling tasks
# we use it for database backup


# Does not work on windows 

from django.core.management import call_command

def my_scheduled_job():
  try:
    call_command('dbbackup')
  except:
    pass


# some crontab terminal commands 
# https://pypi.org/project/django-crontab/
# python manage.py crontab add
# python manage.py crontab show
# python manage.py crontab remove