from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CandidateProfile, CompanyProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "role"]


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = [
            "id",
            "full_name",
            "skills",
            "education",
            "experience",
            "github_url",
            "linkedin_url",
            "cv_file",
            "resume_data",
        ]


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ["id", "company_name", "description", "website"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "username", "password", "role", "first_name", "last_name"]

    def create(self, validated_data):
        role = validated_data.get("role", "candidate")
        user = User.objects.create_user(**validated_data)
        if role == "candidate":
            CandidateProfile.objects.get_or_create(user=user)
        elif role == "company":
            CompanyProfile.objects.get_or_create(user=user, defaults={"company_name": user.username})
        return user
