from celery import shared_task

# @shared_task создаст независимый экземпляр задачи для каждого приложения,
# что позволит повторно использовать задачу.

# таска ждёт когда селери заберёт её на выполнение и начнёт выполнять, это может занятьи и час и если мы передадим
# сам обьект к тому времени он может измениться, поэтому стоит передавать id чтобы взять обьект с актуальными данными
from django.db.models import F

# при изменении тасков нужно перезагрузить docker, celery сам не перезагружается
@shared_task
def set_price(subscription_id):
    from services.models import Subscription
    # .annotate() - применяется только на queryset
    subscription = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=(F('service__full_price') - F('service__full_price') * (F('plan__discount_percent') / 100.00))).first()


    subscription.price = subscription.annotated_price
    # save_model=False чтобы вызав save() в таске не конфликтовал с вызовом save() в модели (рекурсия)
    subscription.save()