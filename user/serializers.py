from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Freelancer, Company

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)


class ActivationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()


class FreelancerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Freelancer
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    employees = UserSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'
