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

    class Meta:
        model = Subscription
        # мы можем указать 2 типа полей: поля сериализатора и поля самой модели
        # указываем plan_id это скрытое поле в которам хранится id связанной модели
        fields = ('id', 'plan_id', 'client_name', 'email', 'plan')