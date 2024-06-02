from rest_framework.routers import DefaultRouter
from django.urls import path, include
from project.views import ProjectViewSet, GigViewSet, GigReportViewSet, ProjectReportViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'gigs', GigViewSet)
router.register(r'gig-reports', GigReportViewSet)
router.register(r'project-reports', ProjectReportViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
