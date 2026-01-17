from django.db import models
from django.conf import settings


# =========================
# DONATION IMAGE PATH
# =========================
def donation_image_upload_path(instance, filename):
    if instance.user and instance.user.pk:
        return f"donations/{instance.user.pk}/{filename}"
    return f"donations/guest/{filename}"



# =========================
# DONATION MODEL
# =========================
class Donation(models.Model):
    DONATION_TYPES = [
        ("blood", "Blood Donation"),
        ("organ", "Organ Donation"),
        ("money", "Financial Donation"),
        ("food", "Food Donation"),
        ("adahi", "Adahi (Sacrifice)"),
        ("clothes", "Clothes Donation"),
        ("furniture", "Furniture Donation"),
        ("medical", "Medical Equipment"),
        ("household", "Household Items"),
        ("water", "Clean Water"),
        ("baby", "Baby Supplies"),
        ("toys", "Toys Donation"),
        ("education", "Education Support"),
        ("electronics", "Electronics"),
        ("cleaning", "Cleaning Supplies"),
        ("medicine_support", "Medicine Support"),
        ("pets", "Pet Support & Adoption"),
        ("volunteer", "Volunteer Time"),
        ("skills", "Professional Help"),
        ("families", "Family Support"),
        ("refugees", "Refugee Support"),
        ("orphans", "Orphan Sponsorship"),
        ("charity_general", "General Charity"),
        ("food_coupons", "Food Coupons"),
    ]

    # User (optional – guest allowed)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="donations",
        null=True,
        blank=True
    )

    # Guest Contact Info
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    donation_type = models.CharField(max_length=50, choices=DONATION_TYPES)

    image = models.ImageField(
        upload_to=donation_image_upload_path,
        null=True,
        blank=True
    )

    location = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_completed = models.BooleanField(default=False)
    approved_by_ngo = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        owner = self.user.username if self.user else "Guest"
        return f"{self.title} ({owner})"


# =========================
# REQUEST PROOF PATH
# =========================
def proof_upload_path(instance, filename):
    return f"requests/proofs/{filename}"


# =========================
# DONATION REQUEST MODEL (✔ معدل فقط هنا)
# =========================
class DonationRequest(models.Model):
    # user اختياري (Guest + JWT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="donation_requests",
        null=True,
        blank=True
    )

    # بيانات صاحب الطلب
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    category = models.CharField(
        max_length=50,
        choices=Donation.DONATION_TYPES
    )

    description = models.TextField()

    proof_document = models.FileField(
        upload_to=proof_upload_path,
        null=True,
        blank=True
    )

    # 🔥 التعديل الوحيد: نظام حالة بدل is_approved
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.name} - {self.category} ({self.status})"
