from django.contrib import path
from .views import register_user, user_login, user_logout, get_user_details,update_user,delete_user


urlpatterns = [
    
    path('api/users/register/', register_user, name='register_user'),
    path('api/users/login/', user_login, name='user_login'),
    path('api/users/logout/', user_logout, name='user_logout'),
    path('api/users/get-user/', get_user_details, name='get_user_details'),
    path('api/users/update-user/', update_user, name='update_user'),
    path('api/users/delete-user/', delete_user, name='delete_user')
]