from rest_framework import generics

from .models import Message
from .serializers import ContactSerializer


class ContactAPIView(generics.CreateAPIView):
    model = Message
    serializer_class = ContactSerializer
