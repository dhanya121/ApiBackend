from rest_framework import serializers
from .models import UserData, Calculation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = ['id', 'operation', 'operand1', 'operand2', 'result', 'created_at']