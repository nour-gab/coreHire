from django.urls import path, re_path

from .views import (
    ATSScoreView,
    AnalyzeResumeView,
    ChatbotView,
    GenerateJobView,
    ImportProfileDataView,
    MicroSuggestionsView,
    RecommendJobsView,
)

urlpatterns = [
    re_path(r"^analyze-resume/?$", AnalyzeResumeView.as_view(), name="analyze-resume"),
    re_path(r"^ats-score/?$", ATSScoreView.as_view(), name="ats-score"),
    re_path(r"^generate-job/?$", GenerateJobView.as_view(), name="generate-job"),
    re_path(r"^recommend-jobs/?$", RecommendJobsView.as_view(), name="recommend-jobs"),
    re_path(r"^micro-suggestions/?$", MicroSuggestionsView.as_view(), name="micro-suggestions"),
    re_path(r"^chat/?$", ChatbotView.as_view(), name="chat"),
    re_path(r"^import-profile-data/?$", ImportProfileDataView.as_view(), name="import-profile-data"),
]
