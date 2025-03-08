from rest_framework import serializers
from .models import Project, ProjectMember, Task
from users.serializers import UserSerializer

class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProjectMember
        fields = ['user', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = ProjectMemberSerializer(source='projectmember_set', many=True, required=False)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'members']
    
    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        project = Project.objects.create(**validated_data)
        # Add owner as admin by default
        ProjectMember.objects.create(project=project, user=project.owner, role='Admin')
        return project

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['project']