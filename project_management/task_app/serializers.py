from rest_framework import serializers
from .models import Task
from users.serializers import UserSerializer
from project.serializers import ProjectSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'description', 
            'status', 
            'priority', 
            'assigned_to', 
            'project', 
            'created_at', 
            'due_date'
        ]
        read_only_fields = ['project', 'created_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title', 
            'description', 
            'status', 
            'priority', 
            'assigned_to', 
            'due_date'
        ]
        extra_kwargs = {
            'assigned_to': {'required': False}
        }