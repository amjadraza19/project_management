from urllib import request   
from django.contrib.auth import authenticate
from django.db.models import Q 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import CustomUser
from django.utils.decorators import method_decorator

import utils as utl  


@api_view(['POST'])
def register_user(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):

    # Retrieve the username or email and password from the request data
    username_or_email = request.data.get('username')
    password = request.data.get('password')

    # Check if both username/email and password are provided
    if not username_or_email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    try:
        user = CustomUser.objects.get(
            Q(username=username_or_email) | Q(email=username_or_email)
        )
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    if not(user.check_password(password)):
        return Response({'error': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)

    if user:

        access_token = utl.generate_access_token(user)

        user.is_login = True  
        user.is_active = True  
        user.token = str(access_token)  
        user.save()      
        user_data=UserSerializer(user).data    
        return Response({'data': {'token': access_token, **user_data}}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@utl.is_auth
def user_logout(request):
    try:

        user_id = request.user_id

        user_inst = CustomUser.objects.get(id=user_id)

        user_inst.token = None

        user_inst.save()

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@utl.is_auth
def get_user_details(request, id):
    try:
        # Authorization check
        if str(request.user_id) != str(id) and not request.is_admin:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            
        user = CustomUser.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response({'data': serializer.data})
    
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@utl.is_auth
def update_user(request, id):
    try:
        if str(request.user_id) != str(id):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            
        user = CustomUser.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()
                
            serializer.save()
            return Response({'data': serializer.data})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@utl.is_auth
def delete_user(request, id):
    try:
        if str(request.user_id) != str(id) and not request.is_admin:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            
        user = CustomUser.objects.get(id=id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)