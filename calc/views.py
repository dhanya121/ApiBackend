
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, CalculationSerializer
from rest_framework.response import Response
from .models import Calculation
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser



# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CalculationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser] # permission class changed

    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
  

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

blacklisted_tokens = set()  # Define blacklisted_tokens as a global variable



class LogoutView(APIView):
    def post(self, request):
        token = request.data.get('refresh_token')

        if token:
            blacklisted_tokens.add(token)
            return Response({'message': 'Logout successful'})
        return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
