from django.db import models
from .Category import Category

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    dateLastUpdate = models.DateField(auto_now=True)
    idCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)

    def change_metadata(self, metadata):
        metadata.idPage = self.id
        metadata.save()

    
