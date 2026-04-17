from django.urls import path

from .views import (
    CandidateProfileView,
    CompanyProfileView,
    LoginView,
    MeView,
    RefreshView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("candidate/profile/", CandidateProfileView.as_view(), name="candidate-profile"),
    path("company/profile/", CompanyProfileView.as_view(), name="company-profile"),
]
