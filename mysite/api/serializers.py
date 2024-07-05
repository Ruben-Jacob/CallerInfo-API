from rest_framework import serializers
from .models import User, Contact, Spam

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ['id', 'phone_number', 'marked_by']
