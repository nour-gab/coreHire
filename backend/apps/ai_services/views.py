from rest_framework import permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.jobs.models import Job
from apps.users.models import CandidateProfile

from .services import (
    compute_ats_score,
    fetch_github_insights,
    generate_job_from_description,
    parse_linkedin_profile_simulation,
    parse_pdf_resume,
    resume_improvement_suggestions,
    simple_chat_reply,
)


class AnalyzeResumeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        resume_text = request.data.get("resume_text", "")
        pdf_file = request.FILES.get("cv")
        job_text = request.data.get("job_text", "")

        if pdf_file:
            resume_text = parse_pdf_resume(pdf_file)

        if not resume_text:
            return Response({"detail": "No resume content provided."}, status=status.HTTP_400_BAD_REQUEST)

        profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
        profile.resume_data = {"raw_text": resume_text[:20000]}
        profile.save(update_fields=["resume_data"])

        suggestions = resume_improvement_suggestions(resume_text=resume_text, job_text=job_text)
        return Response(
            {
                "structured_resume": {"raw_text": resume_text[:3000]},
                "suggestions": suggestions,
            }
        )


class ATSScoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        job_id = request.data.get("job_id")
        resume_text = request.data.get("resume_text", "")

        if job_id:
            job = Job.objects.filter(pk=job_id).first()
            if not job:
                return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
            job_text = f"{job.description} {job.requirements}"
        else:
            job_text = request.data.get("job_text", "")

        if not resume_text and request.user.role == "candidate":
            profile = CandidateProfile.objects.filter(user=request.user).first()
            resume_text = str(profile.resume_data) if profile else ""

        data = compute_ats_score(job_text=job_text, resume_text=resume_text)
        return Response(data)


class GenerateJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        raw_description = request.data.get("description", "")
        if not raw_description:
            return Response({"detail": "description is required."}, status=status.HTTP_400_BAD_REQUEST)
        generated = generate_job_from_description(raw_description)
        return Response(generated)


class RecommendJobsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = CandidateProfile.objects.filter(user=request.user).first()
        candidate_text = str(profile.resume_data) if profile else ""

        recommendations = []
        for job in Job.objects.filter(is_active=True)[:50]:
            score_data = compute_ats_score(
                job_text=f"{job.description} {job.requirements}",
                resume_text=candidate_text,
            )
            recommendations.append(
                {
                    "job_id": job.id,
                    "title": job.title,
                    "company_id": job.company_id,
                    "score": score_data["score"],
                }
            )

        recommendations.sort(key=lambda item: item["score"], reverse=True)
        return Response(recommendations[:10])


class MicroSuggestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        resume_text = request.data.get("resume_text", "")
        job_text = request.data.get("job_text", "")
        return Response(resume_improvement_suggestions(resume_text, job_text))


class ChatbotView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "")
        role = request.data.get("role", request.user.role)
        if not message:
            return Response({"detail": "message is required."}, status=status.HTTP_400_BAD_REQUEST)
        reply = simple_chat_reply(role=role, message=message)
        return Response({"reply": reply})


class ImportProfileDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        github_url = request.data.get("github_url", "")
        linkedin_text = request.data.get("linkedin_text", "")

        github_data = fetch_github_insights(github_url) if github_url else {}
        linkedin_data = parse_linkedin_profile_simulation(linkedin_text) if linkedin_text else {}

        profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
        existing = profile.resume_data or {}
        existing["github"] = github_data
        existing["linkedin"] = linkedin_data
        profile.resume_data = existing
        profile.github_url = github_url or profile.github_url
        profile.save(update_fields=["resume_data", "github_url"])

        return Response({"github": github_data, "linkedin": linkedin_data})
