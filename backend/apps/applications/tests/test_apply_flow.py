from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.applications.models import Application
from apps.jobs.models import Job
from apps.users.models import CandidateProfile

User = get_user_model()


class ApplicationFlowTests(APITestCase):
    def setUp(self):
        self.company = User.objects.create_user(
            email="company@test.dev",
            username="company_user",
            password="Pass12345!",
            role="company",
        )
        self.candidate = User.objects.create_user(
            email="candidate@test.dev",
            username="candidate_user",
            password="Pass12345!",
            role="candidate",
        )

        CandidateProfile.objects.create(
            user=self.candidate,
            resume_data={"raw_text": "python react sql api integration testing"},
        )

        self.job = Job.objects.create(
            company=self.company,
            title="Software Intern",
            description="Work on APIs and frontend features",
            requirements="python react sql communication",
            skills=["python", "react", "sql"],
        )

    @patch(
        "apps.applications.views.compute_ats_score",
        return_value={"score": 82.5, "matched_keywords": ["python"], "missing_keywords": ["sql"]},
    )
    def test_candidate_can_apply_and_get_ats_data(self, _mock_compute):
        self.client.force_authenticate(user=self.candidate)
        response = self.client.post("/applications/", {"job": self.job.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        application = Application.objects.get(candidate=self.candidate, job=self.job)
        self.assertGreaterEqual(application.ats_score, 0)
        self.assertLessEqual(application.ats_score, 100)
        self.assertIsInstance(application.matched_keywords, list)
        self.assertIsInstance(application.missing_keywords, list)

    def test_company_cannot_apply_as_candidate(self):
        self.client.force_authenticate(user=self.company)
        response = self.client.post("/applications/", {"job": self.job.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
