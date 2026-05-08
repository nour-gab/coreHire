from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet

router = DefaultRouter()
router.register("", ApplicationViewSet, basename="applications")

urlpatterns = router.urls
urlpatterns += [
	re_path(r"^$", ApplicationViewSet.as_view({"get": "list", "post": "create"}), name="applications-list"),
	re_path(
		r"^(?P<pk>[^/.]+)/?$",
		ApplicationViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
		name="applications-detail",
	),
]
