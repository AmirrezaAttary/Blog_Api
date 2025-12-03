from celery import shared_task
from .models import Comment
import logging

logger = logging.getLogger(__name__)

@shared_task
def delete_unapproved_comments():
    """
    Delete all comments that are not approved.
    """
    unapproved_comments = Comment.objects.filter(approved=False)
    count = unapproved_comments.count()
    unapproved_comments.delete()
    
    logger.info(f"Deleted {count} unapproved comments.")
    return f"Deleted {count} unapproved comments."
