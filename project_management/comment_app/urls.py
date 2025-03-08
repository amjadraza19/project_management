from django.contrib import path
from .views import list_task_comments, create_task_comment, retrieve_comment,update_comment,delete_comment


urlpatterns = [
    
    path('api/users/list-comments/', list_task_comments, name='list_task_comments'),
    path('api/users/create-comment/', create_task_comment, name='create_task_comment'),
    path('api/users/retrieve-comment/', retrieve_comment, name='retrieve_comment'),
    path('api/users/update-comment/', update_comment, name='update_comment'),
    path('api/users/delete-comment/', delete_comment, name='delete_comment'),
]