from rest_framework import serializers

from services.models import Subscription, Plan


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('__all__')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    # добавляем поле в сериализатор значением которого служит company_name связанной модели Client (ForeignKey)
    client_name = serializers.CharField(source='client.company_name')
    # добавляем поле в сериализатор значение которого служит поле email модели user связанной с моделью client (ForeignKey/OneToOne)
    email = serializers.CharField(source='client.user.email')
    # переменная для вывода аннотированого поля
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    # договор а соглашении имён SerializerMethodField ищет функцию с префиксом get_имя_переменной
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return instance.price

    # def get_price(self, instance):
    #     return (instance.service.full_price -
    #             instance.service.full_price * (instance.plan.discount_percent / 100))

    class Meta:
        model = Subscription
        # мы можем указать 2 типа полей: поля сериализатора и поля самой модели
        # указываем plan_id это скрытое поле в которам хранится id связанной модели
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan', 'price')