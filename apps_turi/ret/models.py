from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ScriptRet(models.Model):

    sito = models.CharField(max_length=5, blank=True)
    script1 = models.TextField()
    script2 = models.TextField()
    bb1 = models.CharField(max_length=5, blank=True)
    bb2 = models.CharField(max_length=5, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ScriptRet"
        verbose_name_plural = "ScriptsRet"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.sito



class ScriptRetLog(models.Model):

    id = models.AutoField(primary_key=True, default=1)
    sito = models.CharField(max_length=5, blank=True)
    bb = models.CharField(max_length=5, blank=True)
    script = models.TextField()
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ScriptRetLog"
        verbose_name_plural = "ScriptsRetLogs"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.sito


class TmplRet(models.Model):
    cod = models.CharField(max_length=4, blank=True)
    tmpl = models.TextField(max_length=4500, blank=True)
    
    def __str__(self):
        return self.cod


class FindBanda(models.Model):
  
    cell = models.CharField(max_length=10, blank=True)
    banda = models.CharField(max_length=20, blank=True)
    label = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.cell


class SwapMatrix(models.Model):
  
    sito = models.CharField(max_length=10, blank=True)
    sttr = models.CharField(max_length=10, blank=True)
    seceq = models.CharField(max_length=10, blank=True)
    banda = models.CharField(max_length=20, blank=True)
    serial = models.CharField(max_length=20, blank=True)
    radctrl = models.CharField(max_length=10, blank=True)
    porta = models.CharField(max_length=10, blank=True)
    prog = models.CharField(max_length=10, blank=True)
    eltlt = models.CharField(max_length=10, blank=True)
    usrlbl = models.CharField(max_length=10, blank=True)
    tmplt = models.CharField(max_length=10, blank=True)
    sistema = models.CharField(max_length=15, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.sito


class CellRet(models.Model):
    master = models.BooleanField(blank=True, default=False)
    bb = models.CharField(max_length=5, blank=True)
    cell = models.CharField(max_length=10, blank=True)
    seq = models.CharField(max_length=5, blank=True)
    radio = models.CharField(max_length=5, blank=True)
    mimo = models.CharField(max_length=5, blank=True)
    tilt = models.CharField(max_length=5, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    sistema = models.CharField(max_length=15, blank=True)
    ordine = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.cell
    

class RET(models.Model):
    bb = models.CharField(max_length=5, blank=True)
    radio = models.CharField(max_length=4, blank=True)
    port = models.CharField(max_length=2, blank=True)
    serial = models.CharField(max_length=30, blank=True)
    cell = models.CharField(max_length=10, blank=True)
    seq = models.CharField(max_length=5, blank=True)
    tilt = models.CharField(max_length=5, blank=True)
    sistema = models.CharField(max_length=15, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    ordine = models.IntegerField(blank=True, null=True)
   
    

    def __str__(self):
        return self.serial
