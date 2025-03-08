from django.contrib import path
from .views import list_project_tasks, create_project_task, retrieve_task, update_task,delete_task


urlpatterns = [
    
    path('api/users/list-tasks/', list_project_tasks, name='list_project_tasks'),
    path('api/users/create-task/', create_project_task, name='create_project_task'),
    path('api/users/retrieve-task/', retrieve_task, name='retrieve_task'),
    path('api/users/update-task/', update_task, name='update_task'),
    path('api/users/delete-task/', delete_task, name='delete_task')
]