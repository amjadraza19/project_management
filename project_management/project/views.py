from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
import utils as utl
from .models import Project, ProjectMember
from .serializers import ProjectSerializer

@api_view(['GET'])
@utl.is_auth
def list_projects(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | 
        Q(members__user=request.user)
    ).distinct()
    serializer = ProjectSerializer(projects, many=True)
    return Response({'data': serializer.data})

@api_view(['POST'])
@utl.is_auth
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save(owner=request.user)
        ProjectMember.objects.create(
            project=project,
            user=request.user,
            role='Admin'
        )
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@utl.is_auth
def get_project(request, id):
    try:
        project = Project.objects.get(id=id)
        if not project.members.filter(user=request.user).exists() and project.owner != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ProjectSerializer(project)
        return Response({'data': serializer.data})
        
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@utl.is_auth
def update_project(request, id):
    try:
        project = Project.objects.get(id=id)
        if project.owner != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        partial = request.method == 'PATCH'
        serializer = ProjectSerializer(project, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@utl.is_auth
def delete_project(request, id):
    try:
        project = Project.objects.get(id=id)
        if project.owner != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
        project.delete()
        return Response({'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)