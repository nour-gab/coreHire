from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import JobViewSet

router = DefaultRouter()
router.register("", JobViewSet, basename="jobs")

urlpatterns = router.urls
urlpatterns += [
	re_path(r"^$", JobViewSet.as_view({"get": "list", "post": "create"}), name="jobs-list"),
	re_path(
		r"^(?P<pk>[^/.]+)/?$",
		JobViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
		name="jobs-detail",
	),
]
