from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    company_email = serializers.EmailField(source="company.email", read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "company",
            "company_email",
            "title",
            "description",
            "responsibilities",
            "requirements",
            "skills",
            "location",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["company", "created_at", "updated_at"]
