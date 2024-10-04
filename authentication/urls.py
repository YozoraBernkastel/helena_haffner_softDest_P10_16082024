from django.urls import path
from authentication import views
from rest_framework_nested import routers
from django.urls import path, include


router = routers.SimpleRouter()
router.register("delete", views.DeleteViewSet, basename="delete")

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("", include(router.urls)),
]
