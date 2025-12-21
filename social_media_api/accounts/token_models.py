from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token as BaseToken

class Token(BaseToken):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='auth_token',
        on_delete=models.CASCADE
    )
    
    class Meta:
        abstract = True