from rest_framework import generics

from .models import ReportedUser
from .serializers import ReportUserSerializer


class ReportUserAPIView(generics.CreateAPIView):
    models = ReportedUser
    serializer_class = ReportUserSerializer
