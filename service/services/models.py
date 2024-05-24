from django.core.validators import MaxValueValidator
from django.db import models

from client.models import Client
from services.tasks import set_price, set_comment


class Service(models.Model):
    # сервис с полной ценой
    name = models.CharField('Название', max_length=50)
    full_price = models.PositiveSmallIntegerField('Цена')

    # при извлечении из базы данных обьекта вызывается метод __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # во время инициации обьекта сохраняем в переменную значение переменной со скидкай
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        # перед сохранением изменённого обьекта проверяем изменилось ли значение скидки
        if self.full_price != self.__full_price:
            # и если так, выбираем все связанные с планом подписки
            for subscription in self.subscriptions.all():
                # пересчитываем цену с помощю таски set_price
                set_price.delay(subscription.id)

        return super().save(*args, **kwargs)


class Plan(models.Model):
    # план определяет скидку
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField('Тариф', choices=PLAN_TYPES, max_length=10)
    # валидатор чтобы размер скидки не мог быть больше 100%, валидаторы принимают список
    discount_percent = models.PositiveSmallIntegerField('Скидка', default=0,
                                                        validators=[
                                                            MaxValueValidator(100)
                                                        ])
    # при извлечении из базы данных обьекта вызывается метод __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # во время инициации обьекта сохраняем в переменную значение переменной со скидкай
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):
        # перед сохранением изменённого обьекта проверяем изменилось ли значение скидки
        if self.discount_percent != self.__discount_percent:
            # и если так, выбираем все связанные с планом подписки
            for subscription in self.subscriptions.all():
                # пересчитываем цену с помощю таски set_price
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)

        return super().save(*args, **kwargs)

class Subscription(models.Model):
    # модель хранит подписку кокогото клиента на какойто сервис по какому то плану
    # related_name - имя по которым данная модель будет доступна из первичной модели
    # client.subscriptions.all()
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveSmallIntegerField(default=0)
    comment = models.CharField(max_length=50, default='')


    # минус такого подхода в том что если у связанных моделей меняется цена или скидка
    # в Subscription сохранённая цена будет не актуальной.
    # таску следует запускать в связанных моделях при изменении цены или скидки

    # чтобы небыло конфликта с рекурсивным вызовом save(), таска передаёт save(save_model=True),
    # а в модели он по умолчанию save_model=True
    # def save(self, *args, save_model=True, **kwargs):
    #     # чтобы не вызывалась по кругу
    #     if save_model:
    #         # устанавливаем новую цену с помощю таски set_price
    #         set_price.delay(self.id)
    #
    #     return super().save(*args, **kwargs)