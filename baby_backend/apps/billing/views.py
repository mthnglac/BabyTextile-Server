from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..accounts.permissions import IsStaffReadOnly
from .models import BillingProfile, Charge
from .serializers import BillingProfileSerializer, ChargeSerializer


class BillingProfileViewSet(ModelViewSet):
    queryset = BillingProfile.objects.all()
    serializer_class = BillingProfileSerializer
    permission_classes = [IsAuthenticated, IsStaffReadOnly]


class ChargeViewSet(ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated, IsStaffReadOnly]

    def perform_create(self, serializer):
        serializer.save(billing_profile=self.request.user.billing_profile)
