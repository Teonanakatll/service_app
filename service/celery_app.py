# получаем доступ к переменной среды, устанавливаем переменную среды
import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

# создаём переменную в которую передаём инициированный celery с именем service
app = Celery('service')
app.config_from_object('django.conf:settings')
# переменная из settings.py
app.conf.broker_url = settings.CELERY_BROKER_URL
# чтобы celery искал таски во всех папках
app.autodiscover_tasks()

# создаём таск
@app.task()
def debug_task():
    time.sleep(20)
    print('Hello from debug_task')