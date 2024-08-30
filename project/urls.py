"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os.path import basename

from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LoginView
from softdesk.views import ProjectsViewset, ContributorsViewset, IssuesViewset, CommentViewset
from authentication.views import Home

router = routers.SimpleRouter()
router.register('projects', ProjectsViewset, basename="projects")
project_router = routers.NestedSimpleRouter(router, r"projects", lookup="project")
project_router.register('contributors', ContributorsViewset, basename="contributors")
project_router.register("issues", IssuesViewset, basename="issues")
issue_router = routers.NestedSimpleRouter(project_router, r"issues", lookup="issue")
issue_router.register("comments", CommentViewset, basename="comments")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('softdesk/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('softdesk/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r"softdesk/api/", include(router.urls)),
    path(r"", include(project_router.urls)),
    path(r"", include(issue_router.urls)),
]
