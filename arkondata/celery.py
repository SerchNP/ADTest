from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arkondata.settings')

app = Celery('arkondata')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Configuraciones de la zona horaria
app.conf.enable_utc = False
app.conf.update(timezone='America/Mexico_City')

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
# 	# Calls test('hello') every 10 seconds.
# 	sender.add_periodic_task(crontab(minute='3', test.s('hello'))

# PARA TAREAS PERIODICAS
app.conf.beat_schedule = {
	'every-hour-metrobus': {
		'task': 'pipeline.tasks.get_metrobus_info_task',
		'schedule': crontab(hour='*/1', minute=0),
		'args':None,
	}
}

# Celery Beat Settings
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def test(arg):
    print(arg)

@app.task(bind=True)
def debug_task(self):
	print('request', self.request)
