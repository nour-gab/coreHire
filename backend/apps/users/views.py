from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import CandidateProfile, CompanyProfile
from .serializers import (
    CandidateProfileSerializer,
    CompanyProfileSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        profile_data = None

        if request.user.role == "candidate":
            profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
            profile_data = CandidateProfileSerializer(profile).data
        elif request.user.role == "company":
            profile, _ = CompanyProfile.objects.get_or_create(
                user=request.user,
                defaults={"company_name": request.user.username or request.user.email},
            )
            profile_data = CompanyProfileSerializer(profile).data

        return Response({"user": user_data, "profile": profile_data})


class CandidateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role != "candidate":
            raise PermissionDenied("Candidate profile access is only available for candidate users.")
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return profile


class CompanyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role != "company":
            raise PermissionDenied("Company profile access is only available for company users.")
        profile, _ = CompanyProfile.objects.get_or_create(
            user=self.request.user,
            defaults={"company_name": self.request.user.username or self.request.user.email},
        )
        return profile
