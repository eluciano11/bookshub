from rest_framework.response import Response

from . import serializers
from rest_framework import generics
from ..utils.response import ErrorResponse


class CreateBookAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.CreateBookSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)
