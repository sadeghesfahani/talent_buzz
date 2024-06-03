from rest_framework import serializers

from user.serializers import CompanySerializer
from .models import Project, Gig, GigReport, ProjectReport, GigApplication, ProjectApplication


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class GigSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = CompanySerializer(read_only=True)

    class Meta:
        model = Gig
        fields = '__all__'


class GigReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GigReport
        fields = '__all__'


class ProjectReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectReport
        fields = '__all__'


class GigApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GigApplication
        fields = '__all__'


class ProjectApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectApplication
        fields = '__all__'
