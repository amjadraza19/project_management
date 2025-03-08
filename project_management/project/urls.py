from django.contrib import path
from .views import list_projects, create_project, get_project, update_project,delete_project


urlpatterns = [
    
    path('api/users/list-projects/', list_projects, name='list_projects'),
    path('api/users/create-project/', create_project, name='create_project'),
    path('api/users/get-project/', get_project, name='get_project'),
    path('api/users/update-project/', update_project, name='update_project'),
    path('api/users/delete-project/', delete_project, name='delete_project'),
]