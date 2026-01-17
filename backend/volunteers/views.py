from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsVolunteer, IsAdmin
from .models import VolunteerApplication
from notifications.models import Notification

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsVolunteer])
def submit_application(request):
    app = VolunteerApplication.objects.create(
        volunteer=request.user,
        campaign_id=request.data["campaign_id"],
        status="CREATED"
    )
    return Response({"id": app.id, "status": app.status})

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def open_application(request, id):
    app = VolunteerApplication.objects.get(id=id)
    app.status = "UNDER_REVIEW"
    app.save()
    return Response({"status": app.status})

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def approve_application(request, id):
    app = VolunteerApplication.objects.get(id=id)
    app.status = "APPROVED"
    app.save()

    Notification.objects.create(
        user=app.volunteer,
        message="Your volunteer application has been APPROVED."
    )

    return Response({"status": app.status})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdmin])
def reject_application(request, id):
    app = VolunteerApplication.objects.get(id=id)
    app.status = "REJECTED"
    app.save()

    Notification.objects.create(
        user=app.volunteer,
        message="Your volunteer application has been REJECTED."
    )

    return Response({"status": app.status})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsVolunteer])
def join_task(request, id):
    app = VolunteerApplication.objects.get(id=id, volunteer=request.user)
    app.status = "ACTIVE"
    app.save()
    return Response({"status": app.status})

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsVolunteer])
def finish_task(request, id):
    app = VolunteerApplication.objects.get(id=id, volunteer=request.user)
    app.status = "COMPLETED"
    app.save()
    return Response({"status": app.status})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_application(request, id):
    app = VolunteerApplication.objects.get(id=id)
    app.status = "CANCELLED"
    app.save()
    return Response({"status": app.status})

# ⭐⭐⭐ NEW – Admin Dashboard ⭐⭐⭐
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin])
def list_under_review(request):
    qs = VolunteerApplication.objects.filter(status="UNDER_REVIEW")
    data = [
        {
            "id": str(app.id),
            "volunteer": app.volunteer.email,
            "campaign": app.campaign.title,
            "status": app.status,
        }
        for app in qs
    ]
    return Response(data)
