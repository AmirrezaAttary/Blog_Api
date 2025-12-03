from celery import shared_task
from .models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_unverified_users():
    """
    Delete all users who are not verified.
    """
    unverified_users = User.objects.filter(is_verified=False)
    count = unverified_users.count()
    unverified_users.delete()
    
    logger.info(f"Deleted {count} unverified users.")
    return f"Deleted {count} unverified users."
