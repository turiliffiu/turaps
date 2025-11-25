from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AdprGsm(models.Model):
    
    cella = models.CharField(max_length=6, blank=True)
    bb = models.CharField(max_length=5, blank=True)
    bsc = models.CharField(max_length=5, blank=True)
    tg = models.CharField(max_length=5, blank=True)
    sdcch = models.CharField(max_length=3, blank=True)
    portanti = models.CharField(max_length=3, blank=True)    
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cella
    
class TmplGsm(models.Model):
    cod = models.CharField(max_length=4, blank=True)
    tmpl = models.TextField(max_length=4500, blank=True)
    
    def __str__(self):
        return self.cod

class ScriptGsm(models.Model):

    sito = models.CharField(max_length=5, blank=True)
    script = models.TextField()
    bb = models.CharField(max_length=5, blank=True)
    bsc = models.CharField(max_length=5, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ScriptGsm"
        verbose_name_plural = "ScriptsGsm"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.sito

class ScriptGsmLog(models.Model):

    id = models.AutoField(primary_key=True, default=1)
    sito = models.CharField(max_length=5, blank=True)
    bb = models.CharField(max_length=5, blank=True)
    script = models.TextField()
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ScriptGsmLog"
        verbose_name_plural = "ScriptsGsmLogs"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.sito