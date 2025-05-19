from django.db import models

class Category(models.Model):
    categoryTitle = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)

    def add_page(self, page):
        page.idCategory = self.id
        page.save()
