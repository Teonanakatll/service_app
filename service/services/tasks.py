import datetime
import time

from celery import shared_task
from celery_singleton import Singleton

# @shared_task создаст независимый экземпляр задачи для каждого приложения,
# что позволит повторно использовать задачу.

# таска ждёт когда селери заберёт её на выполнение и начнёт выполнять, это может занятьи и час и если мы передадим
# сам обьект к тому времени он может измениться, поэтому стоит передавать id чтобы взять обьект с актуальными данными
from django.db import transaction
from django.db.models import F

# при изменении тасков нужно перезагрузить docker, celery сам не перезагружается
# Singleton - ориентируется на переданное id и если таска с таким аргументом есть он не создасе новую
@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    print('do something0')
    with transaction.atomic():
        time.sleep(5)
        # .annotate() - применяется только на queryset
        # select_for_update() - заблокирует обьект взятый по id Subscription
        # пока он не закончит другая твска не сможет его получить
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=(F('service__full_price') - F('service__full_price') * (F('plan__discount_percent') / 100.00))).first()

        time.sleep(20)

        subscription.price = subscription.annotated_price
        # save_model=False чтобы вызав save() в таске не конфликтовал с вызовом save() в модели (рекурсия)
        subscription.save()
    print('do something1')


# при изменении тасков нужно перезагрузить docker, celery сам не перезагружается
# Singleton - ориентируется на переданное id и если таска с таким аргументом есть он не создасе новую
@shared_task(base=Singleton)
def set_comment(subscription_id):
    from services.models import Subscription

    print('do something2')
    with transaction.atomic():
        # .annotate() - применяется только на queryset
        # select_for_update() - заблокирует обьект взятый по id Subscription
        # пока он не закончит другая твска не сможет его получить
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)

        time.sleep(27)

        subscription.comment = str(datetime.datetime.now())
        # save_model=False чтобы вызав save() в таске не конфликтовал с вызовом save() в модели (рекурсия)
        subscription.save()
    print('do something3')