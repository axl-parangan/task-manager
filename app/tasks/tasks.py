from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from .models import Task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='low_priority')
def log_completed_tasks(self):
    try:
        completed_tasks_count = Task.objects.filter(completed=True).count()
        logger.info(f"Number of completed tasks: {completed_tasks_count}")
    except Exception as exc:
        logger.error(f"Error in log_completed_tasks: {exc}")
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=300, queue='default')
def clean_old_tasks(self):
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_tasks = Task.objects.filter(created_at__lt=thirty_days_ago)
        deleted_count = old_tasks.delete()[0]
        logger.info(f"Deleted {deleted_count} old tasks")
    except SoftTimeLimitExceeded:
        logger.warning("Task clean_old_tasks reached soft time limit")
        raise
    except Exception as exc:
        logger.error(f"Error in clean_old_tasks: {exc}")
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=5, default_retry_delay=60, rate_limit='10/m', queue='high_priority')
def process_task(self, task_id):
    try:
        task = Task.objects.get(id=task_id)
        # Process the task...
        logger.info(f"Processed task {task_id}")
    except Task.DoesNotExist:
        logger.warning(f"Task {task_id} not found")
    except Exception as exc:
        logger.error(f"Error processing task {task_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * 2 ** self.request.retries)
        