from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    candidate_email = serializers.CharField(source="candidate.email", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "candidate",
            "candidate_email",
            "job",
            "job_title",
            "status",
            "ats_score",
            "matched_keywords",
            "missing_keywords",
            "created_at",
        ]
        read_only_fields = [
            "candidate",
            "ats_score",
            "matched_keywords",
            "missing_keywords",
            "created_at",
        ]
