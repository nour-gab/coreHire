from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from apps.ai_services.services import compute_ats_score
from apps.jobs.models import Job
from apps.users.models import CandidateProfile

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Application.objects.select_related("job", "candidate").all()

    def get_queryset(self):
        user = self.request.user
        if user.role == "candidate":
            return self.queryset.filter(candidate=user)
        if user.role == "company":
            return self.queryset.filter(job__company=user)
        return self.queryset

    def perform_create(self, serializer):
        if self.request.user.role != "candidate":
            raise PermissionDenied("Only candidate users can apply for jobs.")

        job_id = self.request.data.get("job")
        if not job_id:
            raise PermissionDenied("A job id is required.")

        job = Job.objects.filter(pk=job_id, is_active=True).first()
        if not job:
            raise PermissionDenied("Selected job is not available.")

        candidate_profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        score_data = compute_ats_score(
            job_text=f"{job.description} {job.requirements}",
            resume_text=str(candidate_profile.resume_data),
        )
        serializer.save(
            candidate=self.request.user,
            ats_score=score_data["score"],
            matched_keywords=score_data["matched_keywords"],
            missing_keywords=score_data["missing_keywords"],
        )
