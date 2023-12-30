from django.urls import path

from .views import *

urlpatterns = [
    path('<str:pk>', history_home_view, name='history-home'),
    path('<str:pk>/create/', history_create_view, name='history-create'),
    path('<str:pk>/details/<str:historyId>', history_detail_view, name='history-detail'),
    path('<str:pk>/update/<str:historyId>/', history_update_view, name='history-update'),
    path('<str:pk>/delete/<str:historyId>/', history_delete_view, name='history-delete'),
]
