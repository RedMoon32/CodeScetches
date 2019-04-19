from django.urls import path
from Tasks.MainViews import *

urlpatterns = [
    path('tasks/', TasksManageView.as_view()),
    path('tasks/my/', MyTasksManageView.as_view()),
    path('applications/', ApplicationManageView.as_view()),
    path('applications/my/', MyApplicationManageView.as_view())
]
# tasks/ - get post
# tasks/my/ -get post patch
# applications/ - get post
# applications/my/ - get post put
