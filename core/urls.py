from django.urls import path
from . import views

urlpatterns = [
    path('',views.TaskList , name="task"),
    path('create',views.CreateList , name="create"),
    path('delete/<int:task_id>/', views.deletetask, name='delete_task'),
    path('view/<int:view_id>/', views.Viewtask, name='view'),
    path('edit/<int:edit_id>/', views.edittask, name='edit'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]