from django.db import models
from django.urls import reverse
import math
from django.contrib.auth.models import User


class Adpr(models.Model):
    
    cella = models.CharField(max_length=6, blank=True)
    bb = models.CharField(max_length=5, blank=True)
    seq = models.CharField(max_length=4, blank=True)
    rusref = models.CharField(max_length=4, blank=True)
    rutype = models.CharField(max_length=10, blank=True)
    layer = models.CharField(max_length=10, blank=True)
    mxmod = models.CharField(max_length=2, blank=True)
    mimo = models.CharField(max_length=7, blank=True)
    tma = models.CharField(max_length=2, blank=True)
    ret = models.CharField(max_length=10, blank=True)
    tilt = models.CharField(max_length=3, blank=True)
    atdl = models.CharField(max_length=3, blank=True)
    rtel = models.CharField(max_length=3, blank=True)
    sistema = models.CharField(max_length=15, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.cella


class Scan(models.Model):
    bb = models.CharField(max_length=5, blank=True)
    radio = models.CharField(max_length=70, blank=True)
    seq = models.CharField(max_length=4, blank=True)
    port = models.CharField(max_length=1, blank=True)
    type = models.CharField(max_length=20, blank=True)
    unique_id = models.CharField(max_length=30, blank=True)
    product_number = models.CharField(max_length=20, blank=True)
    freq1tma = models.CharField(max_length=5, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.unique_id



class ValoriTma(models.Model):
    productNumber = models.CharField(max_length=20, blank=True)	
    layer = models.CharField(max_length=2, blank=True)	
    dlAttenuation = models.CharField(max_length=4, blank=True)	
    dlTrafficDelay = models.CharField(max_length=4, blank=True)	
    ulTrafficDelay = models.CharField(max_length=4, blank=True)	
    tma_type = models.CharField(max_length=4, blank=True)	
    subunit = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.productNumber

