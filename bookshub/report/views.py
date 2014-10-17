from rest_framework import generics

from .models import ReportedUser, ReportedOffer
from .serializers import ReportUserSerializer, ReportOfferSerializer


class ReportUserAPIView(generics.CreateAPIView):
    models = ReportedUser
    serializer_class = ReportUserSerializer


class ReportOfferAPIView(generics.CreateAPIView):
    models = ReportedOffer
    serializer_class = ReportOfferSerializer
