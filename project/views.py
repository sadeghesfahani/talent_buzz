from django.db.models import Q, Count, F
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project, Gig, GigReport, ProjectReport, ProjectApplication, GigApplication
from .permissions import IsOwnerOrReadOnly
from .serializers import ProjectSerializer, GigSerializer, GigReportSerializer, ProjectReportSerializer, \
    ProjectApplicationSerializer, GigApplicationSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class GigViewSet(viewsets.ModelViewSet):
    queryset = Gig.objects.all()
    serializer_class = GigSerializer

    def get_queryset(self):
        user = self.request.user
        gigs = self.annotate_gigs_with_accepted_freelancers_count()
        gigs = self.filter_gigs_by_freelancers_count(gigs)
        gigs = self.exclude_gigs_with_user_application(gigs, user)
        return gigs.distinct()

    @staticmethod
    def annotate_gigs_with_accepted_freelancers_count():
        return Gig.objects.annotate(
            accepted_freelancers_count=Count('freelancers', filter=Q(freelancers__gigapplication__status=1)))

    @staticmethod
    def filter_gigs_by_freelancers_count(gigs):
        return gigs.filter(
            Q(accepted_freelancers_count__lt=F('number_of_freelancers')) | Q(number_of_freelancers__isnull=True))

    @staticmethod
    def exclude_gigs_with_user_application(gigs, user):
        return gigs.exclude(gig_application__freelancer__user=user)


class GigReportViewSet(viewsets.ModelViewSet):
    queryset = GigReport.objects.all()
    serializer_class = GigReportSerializer


class ProjectReportViewSet(viewsets.ModelViewSet):
    queryset = ProjectReport.objects.all()
    serializer_class = ProjectReportSerializer


class GigApplicationViewSet(viewsets.ModelViewSet):
    queryset = GigApplication.objects.all()
    serializer_class = GigApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Assuming user is either the owner of the gig or the freelancer who submitted the application
        return GigApplication.objects.filter(
            Q(gig__project__associated_user=user) | Q(freelancer__user=user)
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def accept(self, request, pk=None):
        application = self.get_object()
        self.check_object_permissions(request, application)
        application.status = 1  # Accepted
        application.save()
        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def reject(self, request, pk=None):
        application = self.get_object()
        self.check_object_permissions(request, application)
        application.status = 2  # Rejected
        application.save()
        return Response({'status': 'rejected'})


class ProjectApplicationViewSet(viewsets.ModelViewSet):
    queryset = ProjectApplication.objects.all()
    serializer_class = ProjectApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Assuming user is either the owner of the project or the freelancer who submitted the application
        print(user.username)
        return ProjectApplication.objects.filter(
            Q(project__associated_user=user) | Q(freelancer__user=user)
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def accept(self, request, pk=None):
        application = self.get_object()
        self.check_object_permissions(request, application)
        application.status = 1  # Accepted
        application.save()
        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def reject(self, request, pk=None):
        application = self.get_object()
        self.check_object_permissions(request, application)
        application.status = 2  # Rejected
        application.save()
        return Response({'status': 'rejected'})


class AcceptedGigsView(generics.ListAPIView):
    serializer_class = GigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Gig.objects.filter(
            Q(gig_application__freelancer__user=user, gig_application__status=1)
        ).distinct()


class PendingGigsView(generics.ListAPIView):
    serializer_class = GigSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Gig.objects.filter(
            Q(gig_application__freelancer__user=user, gig_application__status=0)
        ).distinct()


class AcceptedProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter projects where the user is either the owner or has accepted applications
        return Project.objects.filter(
            Q(associated_user=user) |
            Q(project_application__freelancer__user=user, project_application__status=1)
        ).distinct()


class PendingProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter projects where the user is either the owner or has pending applications
        return Project.objects.filter(
            Q(associated_user=user) |
            Q(project_application__freelancer__user=user, project_application__status=0)
        ).distinct()
