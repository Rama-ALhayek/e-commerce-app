import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('src')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    مهمة اختبارية للتأكد من أن Celery يعمل بشكل صحيح
    """
    print(f'Request: {self.request!r}')
