from rest_framework import viewsets, permissions, generics
from .models import User, Contact, Spam
from .serializers import UserSerializer, ContactSerializer, SpamSerializer
from .serializers import UserSerializer, SearchResultSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpamViewSet(viewsets.ModelViewSet):
    queryset = Spam.objects.all()
    serializer_class = SpamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
