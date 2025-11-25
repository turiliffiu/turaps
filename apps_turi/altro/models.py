from django.db import models



class Tool(models.Model):
	
    x = models.CharField(max_length=2, blank=True)
    y = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.x
    










