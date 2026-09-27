from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    tech_stack = models.CharField(max_length=200,blank=True, null=True)
    image = models.ImageField(upload_to='project_images/')
    github_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class ImageGallary(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

    class Meta:
        verbose_name_plural = 'Image Gallaries'

    def __str__(self):
        return f"Image for {self.project.title}"
