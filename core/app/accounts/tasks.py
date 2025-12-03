from celery import shared_task
from time import sleep
import logging

logger = logging.getLogger(__name__)

@shared_task
def sendEmail():
    sleep(3)
    print('done sending email')
    