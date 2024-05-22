from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=50)
    price=models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_borrowed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title
    
    
    
    
