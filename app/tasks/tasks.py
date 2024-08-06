from celery import shared_task
from .models import Task
import logging

logger = logging.getLogger(__name__)

@shared_task
def log_completed_tasks():
    completed_tasks_count = Task.objects.filter(completed=True).count() 
    logger.info(f'Number of tasks marked as completed: {completed_tasks_count}')
