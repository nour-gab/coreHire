from unittest.mock import patch

from django.test import TestCase

from apps.ai_services.services import compute_ats_score


class ATSScoringServiceTests(TestCase):
    @patch("apps.ai_services.services.extract_keywords")
    def test_compute_ats_score_returns_expected_percentage(self, mock_extract_keywords):
        mock_extract_keywords.side_effect = [
            ["python", "react", "sql"],
            ["python", "react", "django"],
        ]

        result = compute_ats_score("job text", "resume text")

        self.assertEqual(result["score"], 66.67)
        self.assertEqual(sorted(result["matched_keywords"]), ["python", "react"])
        self.assertEqual(result["missing_keywords"], ["sql"])

    @patch("apps.ai_services.services.extract_keywords", return_value=[])
    def test_compute_ats_score_with_empty_job_keywords(self, _mock_extract_keywords):
        result = compute_ats_score("", "resume text")
        self.assertEqual(result, {"score": 0.0, "matched_keywords": [], "missing_keywords": []})
