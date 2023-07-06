from rest_framework import viewsets

from .models import Activity
from .permissions import IsAuthorOrAdmin
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet для карточек."""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthorOrAdmin,)
