from django.db import models
# Create your models here.

class TmplTma(models.Model):
    cod = models.CharField(max_length=4, blank=True)
    tmpl = models.TextField(max_length=4500, blank=True)
    
    def __str__(self):
        return self.cod