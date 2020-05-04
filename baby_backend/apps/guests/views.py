from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from baby_backend.utils.utils import unique_guest_vendor_username_generator, random_string_generator
from ..accounts.serializers import UserRootSerializer
from ..accounts.permissions import IsStaffOrGuestReadOnly
from .permissions import IsAssociatedWithGuest
from .models import GuestVendor
from .serializers import GuestVendorSerializer, GuestVendorRootSerializer


class GuestVendorViewSet(ModelViewSet):
    queryset = GuestVendor.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrGuestReadOnly, IsAssociatedWithGuest]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return GuestVendorRootSerializer
        return GuestVendorSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'guestvendor'):
            qs = GuestVendor.objects.filter(user=self.request.user)
        else:
            qs = GuestVendor.objects.all()
        return qs

    @action(detail=False, permission_classes=[IsAdminUser])
    def generate_guestvendor(self, request, pk=None):
        unique_guest_username = unique_guest_vendor_username_generator()
        random_guest_password = random_string_generator()

        # user creation
        user_data = {'username': unique_guest_username, 'password': random_guest_password}
        user_serializer = UserRootSerializer(data=user_data, context={'request': request})
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        guest_user_obj = User.objects.get(username=user_serializer.data['username'])
        guest_user_obj.set_password(user_serializer.data['password'])

        guest_data = {'user': user_serializer.data['url']}
        guest_serializer = self.get_serializer(data=guest_data, context={'request': request})
        guest_serializer.is_valid(raise_exception=True)
        guest_serializer.save()

        guest_infos = {'username': unique_guest_username, 'password': random_guest_password}
        guest_infos.update(guest_serializer.data)

        return Response(guest_infos, status=status.HTTP_201_CREATED)
