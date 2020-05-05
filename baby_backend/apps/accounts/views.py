from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAssociatedWithUser, IsStaffReadOnlyOrVendorPatchOnly
from .serializers import UserRootSerializer, UserSerializer, UserVendorSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsStaffReadOnlyOrVendorPatchOnly, IsAssociatedWithUser]
    ordering = ['username']

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return UserRootSerializer
        elif hasattr(self.request.user, 'vendor'):
            return UserVendorSerializer
        return UserSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'vendor'):
            qs = User.objects.filter(pk=self.request.user.pk)
        else:
            qs = User.objects.all()  # for superuser and staff users
        return qs

    def get_object(self):
        if self.request.user.is_superuser and self.kwargs['pk'] == 'me':
            return self.request.user
        elif hasattr(self.request.user, 'vendor') and self.kwargs['pk'] == 'me':
            return self.request.user
        else:
            return super(UserViewSet, self).get_object()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def set_staff(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except Exception as e:
            if settings.DEBUG:
                print(e)
            raise NotFound(
                detail={
                    'message':
                        _('Some error occurred while getting information.')})
        else:
            user.is_staff = True
            user.save()
        return Response({'message': _('The user is now staff.')})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def unset_staff(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except Exception as e:
            if settings.DEBUG:
                print(e)
            raise NotFound(
                detail={
                    'message':
                        _('Some error occurred while getting information.')})
        else:
            user.is_staff = False
            user.save()
        return Response({'message': _('The user is no staff anymore.')})
