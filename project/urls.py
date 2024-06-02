from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.views import ProjectViewSet, GigViewSet, GigReportViewSet, ProjectReportViewSet, GigApplicationViewSet, \
    ProjectApplicationViewSet, AcceptedGigsView, PendingGigsView, AcceptedProjectsView, PendingProjectsView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'gigs', GigViewSet)
router.register(r'gig-reports', GigReportViewSet)
router.register(r'project-reports', ProjectReportViewSet)
router.register(r'gig-applications', GigApplicationViewSet)
router.register(r'project-applications', ProjectApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accepted-gigs/', AcceptedGigsView.as_view(), name='accepted-gigs'),
    path('pending-gigs/', PendingGigsView.as_view(), name='pending-gigs'),
    path('accepted-projects/', AcceptedProjectsView.as_view(), name='accepted-projects'),
    path('pending-projects/', PendingProjectsView.as_view(), name='pending-projects'),
]
