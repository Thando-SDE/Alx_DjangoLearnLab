from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """View to list all notifications for the current user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Return notifications for the current user, newest first
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-timestamp')

class MarkNotificationAsReadView(generics.UpdateAPIView):
    """View to mark a notification as read"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        
        # Check if the notification belongs to the current user
        if notification.recipient != request.user:
            return Response(
                {'error': 'You do not have permission to mark this notification as read'},
                status=403
            )
        
        notification.is_read = True
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)