from rest_framework import serializers
from .models import Project, Gig, GigReport, ProjectReport

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class GigSerializer(serializers.ModelSerializer):
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
