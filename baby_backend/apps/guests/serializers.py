from rest_framework import serializers

from .models import GuestVendor


class GuestVendorRootSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GuestVendor
        fields = ['url', 'pk', 'guest_vendor_unique_id', 'user', 'is_active', 'updated_at', 'created_at']


class GuestVendorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = GuestVendor
        fields = ['url', 'pk', 'user', 'is_active']
        read_only_fields = ['is_active']
