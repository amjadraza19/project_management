from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from task_app.models import Task
from .serializers import CommentSerializer, CommentCreateSerializer
import utils as utl

@api_view(['GET'])
@utl.is_auth
def list_task_comments(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if not task.project.members.filter(user=request.user).exists():
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response({'data': serializer.data})
    
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@utl.is_auth
def create_task_comment(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if not task.project.members.filter(user=request.user).exists():
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(
                user=request.user,
                task=task
            )
            full_serializer = CommentSerializer(comment)
            return Response({'data': full_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@utl.is_auth
def retrieve_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
        if not comment.task.project.members.filter(user=request.user).exists():
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(comment)
        return Response({'data': serializer.data})
    
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@utl.is_auth
def update_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
        if comment.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        partial = request.method == 'PATCH'
        serializer = CommentCreateSerializer(comment, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            full_serializer = CommentSerializer(comment)
            return Response({'data': full_serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@utl.is_auth
def delete_comment(request, id):
    try:
        comment = Comment.objects.get(id=id)
        if comment.user != request.user and comment.task.project.owner != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)