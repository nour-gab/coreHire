from django.urls import path

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
    path("analyze-resume/", AnalyzeResumeView.as_view(), name="analyze-resume"),
    path("ats-score/", ATSScoreView.as_view(), name="ats-score"),
    path("generate-job/", GenerateJobView.as_view(), name="generate-job"),
    path("recommend-jobs/", RecommendJobsView.as_view(), name="recommend-jobs"),
    path("micro-suggestions/", MicroSuggestionsView.as_view(), name="micro-suggestions"),
    path("chat/", ChatbotView.as_view(), name="chat"),
    path("import-profile-data/", ImportProfileDataView.as_view(), name="import-profile-data"),
]
