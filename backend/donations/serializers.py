from rest_framework import serializers
from .models import Donation, DonationRequest


# =========================
# DONATION SERIALIZER
# =========================
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # إضافة تفاصيل المستخدم إن وُجد
        if instance.user:
            representation["user_details"] = {
                "id": instance.user.id,
                "name": instance.user.first_name or instance.user.username,
                "email": instance.user.email,
                "phone": getattr(instance.user, "phone", None),
            }
        else:
            representation["user_details"] = None

        return representation

# =========================
# DONATION CREATE SERIALIZER (Guest + User)
# =========================
class DonationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            "title",
            "description",
            "donation_type",
            "image",
            "location",
            "amount",
        ]


# =========================
# DONATION REQUEST SERIALIZER
# =========================
class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = "__all__"
        read_only_fields = ["user", "status", "created_at"]
        extra_kwargs = {
            # دعم Guest بدون أخطاء
            "user": {"required": False, "allow_null": True},
            "proof_document": {"required": False, "allow_null": True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # إضافة تفاصيل المستخدم إن وُجد
        if instance.user:
            representation["user_details"] = {
                "id": instance.user.id,
                "name": instance.user.first_name or instance.user.username,
                "email": instance.user.email,
                "phone": getattr(instance.user, "phone", None),
            }
        else:
            representation["user_details"] = None

        return representation
