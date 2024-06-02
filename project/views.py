from rest_framework import viewsets

from .models import Project, Gig, GigReport, ProjectReport
from .serializers import ProjectSerializer, GigSerializer, GigReportSerializer, ProjectReportSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer


class GigReportViewSet(viewsets.ModelViewSet):
    queryset = GigReport.objects.all()
    serializer_class = GigReportSerializer


class ProjectReportViewSet(viewsets.ModelViewSet):
    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer
