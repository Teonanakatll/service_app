from django.db.models import Prefetch, F, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from client.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related('plan',
        # для модели client запрашиваем связанного user, и берём только поле company_name,
        # и поле email из связанной модели user (OneToOne)
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')))\
        .annotate(price=(F('service__full_price') -
                         F('service__full_price') *
                         # 100.00 чтобы получить в результате дробь
                         (F('plan__discount_percent') / 100.00)))
    serializer_class = SubscriptionSerializer

    # переопределяем метод list который отвечает за обработку запросса и формирования ответа клиенту
    def list(self, request, *args, **kwargs):
        # вызываем базовый фильтр кверисета
        queryset = self.filter_queryset(self.get_queryset())
        # вызываем базовый метод list
        response = super().list(request, *args, **kwargs)

        # присваиваем данные response зночению словаря с ключём result
        response_data = {'result': response.data}

        # присваиваем данный словарь словарю дата в response
        response.data = response_data
        # добавляем в словерь ещё один ключ total_amount c агригигированной суммой анотированных значений
        # и методом get() берём значение, aggregate в любом случае добавляет 1 запросс
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        return response



















