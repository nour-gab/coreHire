from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Job
from .serializers import JobSerializer


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.company_id == request.user.id


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwnerOrReadOnly]
    queryset = Job.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == "company":
            return Job.objects.filter(company=user)
        return Job.objects.filter(is_active=True)

    def perform_create(self, serializer):
        if self.request.user.role != "company":
            raise PermissionDenied("Only company users can create jobs.")
        serializer.save(company=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role != "company":
            raise PermissionDenied("Only company users can update jobs.")
        serializer.save()
