from celery.schedules import crontab

# Broker settings
broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'

# Task serialization format
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# Enable UTC timezone
enable_utc = True

# Set the default queue name
task_default_queue = 'default'

# Configure task routes
task_routes = {
    'tasks.tasks.log_completed_tasks': {'queue': 'low_priority'},
    'tasks.tasks.clean_old_tasks': {'queue': 'default'},
    'tasks.tasks.process_task': {'queue': 'high_priority'},
}

# Configure periodic tasks
beat_schedule = {
    'log-completed-tasks-every-minute': {
        'task': 'tasks.tasks.log_completed_tasks',
        'schedule': crontab(minute='*'),
    },
    'clean-old-tasks-daily': {
        'task': 'tasks.tasks.clean_old_tasks',
        'schedule': crontab(hour=0, minute=0),
    },
}

# Concurrency settings
worker_concurrency = 4  # Adjust based on your server's capacity

# Task time limits
task_time_limit = 60 * 5  # 5 minutes
task_soft_time_limit = 60  # 1 minute

# Maximum tasks per child
worker_max_tasks_per_child = 100

# Prefetch multiplier
worker_prefetch_multiplier = 4