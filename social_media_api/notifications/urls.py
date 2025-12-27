from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/mark-read/', views.MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
]
