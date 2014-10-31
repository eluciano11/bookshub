from rest_framework import generics

from .models import ReportedUser, ReportedOffer, ReportedBook
from .serializers import (ReportUserSerializer, ReportOfferSerializer,
                          ReportBookSerializer)


class ReportUserAPIView(generics.CreateAPIView):
    models = ReportedUser
    serializer_class = ReportUserSerializer


class ReportOfferAPIView(generics.CreateAPIView):
    models = ReportedOffer
    serializer_class = ReportOfferSerializer


class ReportBookAPIView(generics.CreateAPIView):
    models = ReportedBook
    serializer_class = ReportBookSerializer
