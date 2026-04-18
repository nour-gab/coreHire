from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.ai_services.services import compute_ats_score
from apps.applications.models import Application
from apps.jobs.models import Job
from apps.users.models import CandidateProfile, CompanyProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo users, jobs, profiles, and applications for CoreHire MVP"

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default="DemoPass123!",
            help="Password to set on all seeded demo users.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password = options["password"]

        admin = self._upsert_user(
            email="admin@corehire.dev",
            username="corehire_admin",
            role="admin",
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        company_a = self._upsert_user(
            email="hiring@novalabs.dev",
            username="novalabs",
            role="company",
            password=password,
        )
        company_b = self._upsert_user(
            email="jobs@atlasworks.dev",
            username="atlasworks",
            role="company",
            password=password,
        )

        candidate_a = self._upsert_user(
            email="maya.candidate@corehire.dev",
            username="maya_candidate",
            role="candidate",
            password=password,
        )
        candidate_b = self._upsert_user(
            email="sam.candidate@corehire.dev",
            username="sam_candidate",
            role="candidate",
            password=password,
        )

        CompanyProfile.objects.update_or_create(
            user=company_a,
            defaults={
                "company_name": "Nova Labs",
                "description": "Product-focused software and AI team.",
                "website": "https://novalabs.dev",
            },
        )
        CompanyProfile.objects.update_or_create(
            user=company_b,
            defaults={
                "company_name": "Atlas Works",
                "description": "Data and automation consulting studio.",
                "website": "https://atlasworks.dev",
            },
        )

        CandidateProfile.objects.update_or_create(
            user=candidate_a,
            defaults={
                "full_name": "Maya Candidate",
                "skills": ["python", "react", "sql", "git"],
                "education": "BSc Computer Science",
                "experience": "Built internship projects in full-stack web development.",
                "resume_data": {
                    "raw_text": (
                        "Python React SQL Git API integration testing dashboards "
                        "internship projects data visualization"
                    )
                },
            },
        )
        CandidateProfile.objects.update_or_create(
            user=candidate_b,
            defaults={
                "full_name": "Sam Candidate",
                "skills": ["django", "javascript", "postgresql", "docker"],
                "education": "BEng Software Engineering",
                "experience": "Delivered backend services and deployment automation projects.",
                "resume_data": {
                    "raw_text": (
                        "Django JavaScript PostgreSQL Docker REST API backend testing "
                        "deployment cloud"
                    )
                },
            },
        )

        job_1, _ = Job.objects.update_or_create(
            company=company_a,
            title="Frontend Engineering Intern",
            defaults={
                "description": "Build React UI features and integrate APIs for product workflows.",
                "responsibilities": "Implement UI components, collaborate with designers, write tests.",
                "requirements": "React JavaScript API integration communication",
                "skills": ["react", "javascript", "api", "testing"],
                "location": "Remote",
                "is_active": True,
            },
        )
        job_2, _ = Job.objects.update_or_create(
            company=company_b,
            title="Backend Engineering Intern",
            defaults={
                "description": "Develop Django APIs and optimize Postgres-backed services.",
                "responsibilities": "Ship API endpoints, improve performance, document architecture.",
                "requirements": "Python Django PostgreSQL Docker REST",
                "skills": ["python", "django", "postgresql", "docker"],
                "location": "Hybrid",
                "is_active": True,
            },
        )

        self._upsert_application(candidate_a, job_1)
        self._upsert_application(candidate_b, job_2)

        self.stdout.write(self.style.SUCCESS("Seeded demo data successfully."))
        self.stdout.write(
            "Demo users: admin@corehire.dev, hiring@novalabs.dev, jobs@atlasworks.dev, "
            "maya.candidate@corehire.dev, sam.candidate@corehire.dev"
        )
        self.stdout.write(f"Password for all demo users: {password}")

    def _upsert_user(
        self,
        email: str,
        username: str,
        role: str,
        password: str,
        is_staff: bool = False,
        is_superuser: bool = False,
    ):
        defaults = {
            "username": username,
            "role": role,
            "is_staff": is_staff,
            "is_superuser": is_superuser,
            "is_active": True,
        }
        user, created = User.objects.get_or_create(email=email, defaults=defaults)

        # Keep seeded users aligned with expected role and access flags.
        should_save = False
        for key, value in defaults.items():
            if getattr(user, key) != value:
                setattr(user, key, value)
                should_save = True

        if created or not user.check_password(password):
            user.set_password(password)
            should_save = True

        if should_save:
            user.save()

        return user

    def _upsert_application(self, candidate_user, job):
        profile, _ = CandidateProfile.objects.get_or_create(user=candidate_user)
        ats = compute_ats_score(
            job_text=f"{job.description} {job.requirements}",
            resume_text=str(profile.resume_data),
        )
        Application.objects.update_or_create(
            candidate=candidate_user,
            job=job,
            defaults={
                "status": Application.Status.APPLIED,
                "ats_score": ats["score"],
                "matched_keywords": ats["matched_keywords"],
                "missing_keywords": ats["missing_keywords"],
            },
        )
