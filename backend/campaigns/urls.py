from django.urls import path
from .views import create_campaign, submit_campaign, review_campaign

urlpatterns = [
    path("create/", create_campaign),
    path("<uuid:id>/submit/", submit_campaign),
    path("<uuid:id>/review/", review_campaign),
]
