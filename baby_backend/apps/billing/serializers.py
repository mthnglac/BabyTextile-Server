from rest_framework import serializers

from .models import BillingProfile, Charge


class BillingProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BillingProfile
        fields = ['url', 'pk', 'id', 'user', 'is_active', 'created_at', 'updated_at', 'charge_set']
        extra_kwargs = {
            'charge_set': {'required': False}
        }


class ChargeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Charge
        fields = ['url', 'pk', 'billing_profile', 'paid', 'refunded', 'updated_at', 'created_at']
