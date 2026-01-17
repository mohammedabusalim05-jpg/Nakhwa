from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsNGO, IsAdmin
from .models import Campaign

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsNGO])
def create_campaign(request):
    campaign = Campaign.objects.create(
        title=request.data.get("title"),
        description=request.data.get("description", ""),
        ngo=request.user
    )
    return Response({"id": campaign.id, "status": campaign.status})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsNGO])
def submit_campaign(request, id):
    campaign = Campaign.objects.get(id=id, ngo=request.user)
    campaign.status = "PendingVerification"
    campaign.save()
    return Response({"status": campaign.status})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdmin])
def review_campaign(request, id):
    campaign = Campaign.objects.get(id=id)
    campaign.status = request.data.get("status")
    campaign.save()
    return Response({"status": campaign.status})
