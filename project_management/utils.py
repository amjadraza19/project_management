from functools import wraps
from urllib import request, response
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from django.http import HttpResponse, JsonResponse

# Secret key for signing the JWT
SECRET_KEY = settings.SECRET_KEY

# Token expiration time
ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)


def generate_access_token(user):
    # Set the expiration time for the access token by adding the ACCESS_TOKEN_LIFETIME to the current UTC time
    expiration = datetime.utcnow() + ACCESS_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow() # Set the issued at time to the current UTC time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    expiration = datetime.utcnow() + REFRESH_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        # Attempt to decode the JWT token using the specified secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({"message": "Token is expired"}, status=status.HTTP_498_INVALID_TOKEN)
    except jwt.InvalidTokenError:
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)


def is_auth(fun):
    @wraps(fun)
    def wrap(request, *args, **kwargs):
        # Debugging prints to check the request headers and arguments
        print("Line 49>>>", request.headers)
        print("Line 50", request, *args, **kwargs)
        try:
            # Extracting the 'Authorization' token from the request headers
            token = request.headers.get('Authorization')

            if not token:
                return JsonResponse({"message": "Token is missing!"}, status=status.HTTP_403_FORBIDDEN)

            decode_token_result = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # (token)

            # Attach the decoded token result to the request object for later use
            request.decoded_token_result = decode_token_result

            # Extract the user ID from the decoded token and attach it to the request object
            request.user_id = request.decoded_token_result.get("user_id")

            # Call the original function with the updated request object and return its response
            return fun(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token is expired"}, status=status.HTTP_498_INVALID_TOKEN)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)

    return wrap  # Return the wrapper function


