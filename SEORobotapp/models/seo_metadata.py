from django.db import models
from .Page import Page

class SEOMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    meta_key = models.CharField(max_length=255)
    meta_value = models.CharField(max_length=255)
    idPage = models.ForeignKey(Page, on_delete=models.CASCADE)
