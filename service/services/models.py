from django.core.validators import MaxValueValidator
from django.db import models

from client.models import Client


class Service(models.Model):
    # сервис с полной ценой
    name = models.CharField('Название', max_length=50)
    full_price = models.PositiveSmallIntegerField('Цена')


class Plan(models.Model):
    # план определяет скидку
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_tupe = models.CharField('Тариф', choices=PLAN_TYPES, max_length=10)
    # валидатор чтобы размер скидки не мог быть больше 100%, валидаторы принимают список
    discount_percent = models.PositiveSmallIntegerField('Скидка', default=0,
                                                        validators=[
                                                            MaxValueValidator(100)
                                                        ])

class Subscription(models.Model):
    # модель хранит подписку кокогото клиента на какойто сервис по какому то плану
    # related_name - имя по которым данная модель будет доступна из первичной модели
    # client.subscriptions.all()
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)