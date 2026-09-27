from django.contrib import admin
from .models import Project,ImageGallary


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link', 'github_link')
    search_fields = ('title', 'description')

@admin.register(ImageGallary)
class ImageGallaryAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
    search_fields = ('project__title',)

    

