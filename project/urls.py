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
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from softdesk.views import (ProjectsViewset, ProjectCreationViewset, DeleteProjectViewset, ContributorViewset, ContributorCreationViewset,
                            IssueViewset, IssueCreationVieweset, CommentViewset, CommentCreationViewset)

router = routers.SimpleRouter()
router.register('project', ProjectsViewset, basename="project")
project_router = routers.NestedSimpleRouter(router, "project", lookup="project")
project_router.register('contributor', ContributorViewset, basename="project-contributor")
project_router.register("issue", IssueViewset, basename="projects-issue")
issue_router = routers.NestedSimpleRouter(project_router, "issue", lookup="issue")
issue_router.register("comment", CommentViewset, basename="project-issue-comment")
project_router.register("contributorCreation", ContributorCreationViewset, basename="contributorCreation")
project_router.register("issueCreation", IssueCreationVieweset, basename="issuerCreation")
issue_router.register("commentCreation", CommentCreationViewset, basename="commentCreation")
project_router.register("deleteProject", DeleteProjectViewset, basename="deleteProject")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('softdesk/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('softdesk/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("softdesk/api/", include(router.urls)),
    path("softdesk/api/", include(project_router.urls)),
    path("softdesk/api/", include(issue_router.urls)),
    path("softdesk/api/create/project/", ProjectCreationViewset.as_view(), name="project_creation"),
]
