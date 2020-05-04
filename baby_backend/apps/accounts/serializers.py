from django.contrib.auth.models import User
from rest_framework import serializers


class UserRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'password', 'billing_profile', 'cart', 'vendor', 'customer']
        extra_kwargs = {
            'billing_profile': {'required': False},
            'cart': {'required': False},
            'vendor': {'required': False},
            'customer': {'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password') if 'password' in validated_data else None
        user = super(UserRootSerializer, self).update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create(self, validated_data):
        user = super(UserRootSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserVendorSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'pk', 'email', 'username', 'password', 'first_name', 'last_name', 'password']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'password', 'email', 'first_name', 'last_name', 'password']
