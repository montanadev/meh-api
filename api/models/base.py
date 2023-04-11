from django.db import models


class BaseModel(object):
    created_at = models.DateTimeField(auto_now_add=True)
