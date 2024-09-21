from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        reads_only_fields = ["user","created_at","updated_at","products",]


    def create(self, validated_data):
        return Order.objects.create(**validated_data)