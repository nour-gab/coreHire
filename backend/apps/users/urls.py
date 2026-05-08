from django.urls import re_path

from .views import (
    CandidateProfileView,
    CompanyProfileView,
    LoginView,
    MeView,
    RefreshView,
    RegisterView,
)

urlpatterns = [
    re_path(r"^register/?$", RegisterView.as_view(), name="register"),
    re_path(r"^login/?$", LoginView.as_view(), name="login"),
    re_path(r"^refresh/?$", RefreshView.as_view(), name="refresh"),
    re_path(r"^me/?$", MeView.as_view(), name="me"),
    re_path(r"^candidate/profile/?$", CandidateProfileView.as_view(), name="candidate-profile"),
    re_path(r"^company/profile/?$", CompanyProfileView.as_view(), name="company-profile"),
]
