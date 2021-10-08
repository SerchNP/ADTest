from celery import shared_task
from celery.utils.log import get_task_logger

from .views import getMetrobusInfo


logger = get_task_logger(__name__)

# Se define la función de la tarea que se ejecutará periodicamente
@shared_task(bind=True)
def get_metrobus_info_task(self):
	print('Leyendo datos del metrobus')
	getMetrobusInfo(self.request)
	logger.info('Datos obtenidos')
	return "Done"
