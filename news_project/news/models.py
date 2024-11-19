from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category}'
    
class New(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    post_by = models.CharField(max_length=255)
    count_view = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images/',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.title}'
