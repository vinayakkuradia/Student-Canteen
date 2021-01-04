from rest_framework import serializers
from . models import Order, payment_methods, meal_types


class OrdersDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id', 'datetime', 'plate_count', 'payment_method', 'meal_type', 'confirmation_status')


class OrdersAdminDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrdersSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    ordered_by = serializers.CharField()
    datetime = serializers.DateTimeField()
    plate_count = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=payment_methods)
    meal_type = serializers.ChoiceField(choices=meal_types)
    confirmation_status = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
    '''
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        Order.save()
        return Order'''