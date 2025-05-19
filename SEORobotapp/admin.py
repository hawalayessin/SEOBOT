from django.contrib import admin

from .models import Page
from .models import Category
from .models import SEOMetadata

# Register your models here.
admin.site.register(Page)
admin.site.register(Category)
admin.site.register(SEOMetadata)