from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count
import logging

from notifications.models import Notification
from .models import Donation, DonationRequest
from .serializers import (
    DonationSerializer,
    DonationCreateSerializer,
    DonationRequestSerializer
)


logger = logging.getLogger(__name__)

# =========================
# DONATIONS
# =========================

# ✔ عرض جميع التبرعات
class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all().order_by("-created_at")
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]


# ✔ إنشاء تبرع جديد (User / Guest) — ✅ معدل
class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationCreateSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None

        donation = serializer.save(
            user=user,
            approved_by_ngo=True,
            is_completed=False
        )

        if user:
            Notification.objects.create(
                user=user,
                message=f"Your donation '{donation.title}' was created successfully."
            )



# ✔ تفاصيل / تعديل / حذف تبرع
class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        old = self.get_object()
        donation = serializer.save()

        # 🔔 إشعار عند تغيير حالة التبرع
        if old.is_completed != donation.is_completed and donation.user:
            status = "completed" if donation.is_completed else "pending"

            Notification.objects.create(
                user=donation.user,
                message=f"Your donation '{donation.title}' was marked as {status}."
            )


# ✔ عرض التبرعات حسب النوع
class DonationByTypeView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Donation.objects.filter(
            donation_type=self.kwargs.get("donation_type")
        ).order_by("-created_at")


# =========================
# DONATION REQUESTS
# =========================

# ✔ إنشاء طلب مساعدة
class DonationRequestCreateView(generics.CreateAPIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


# ✔ عرض الطلبات المعلّقة فقط
class PendingDonationRequestsView(generics.ListAPIView):
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return DonationRequest.objects.filter(
            status="pending"
        ).order_by("-created_at")


# ✔ تعديل حالة الطلب
class DonationRequestUpdateView(generics.UpdateAPIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        old = self.get_object()
        request_obj = serializer.save()

        if old.status != request_obj.status and request_obj.user:
            Notification.objects.create(
                user=request_obj.user,
                message=f"Your help request was {request_obj.status}."
            )


# ✔ حذف الطلب
class DonationRequestDeleteView(generics.DestroyAPIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationRequestSerializer
    permission_classes = [permissions.IsAdminUser]


# =========================
# DASHBOARD – DONATIONS
# =========================
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def dashboard_donations_stats(request):
    User = get_user_model()
    approved_donations = Donation.objects.filter(approved_by_ngo=True)

    return Response({
        "total_users": User.objects.count(),
        "total_donations": Donation.objects.count(),
        "active_cases": approved_donations.filter(is_completed=False).count(),
        "recent_donations": DonationSerializer(
            approved_donations.order_by("-created_at")[:5],
            many=True
        ).data,
        "donations_by_category": [
            {"name": item["donation_type"], "value": item["count"]}
            for item in Donation.objects
            .values("donation_type")
            .annotate(count=Count("id"))
        ],
    })


# =========================
# DASHBOARD – REQUESTS
# =========================
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def dashboard_requests_stats(request):
    return Response({
        "total_requests": DonationRequest.objects.count(),
        "pending_requests": DonationRequest.objects.filter(status="pending").count(),
        "approved_requests": DonationRequest.objects.filter(status="approved").count(),
        "rejected_requests": DonationRequest.objects.filter(status="rejected").count(),
        "recent_requests": DonationRequestSerializer(
            DonationRequest.objects.order_by("-created_at")[:5],
            many=True
        ).data,
    })
