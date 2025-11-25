from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DeMatrix(models.Model):

    tmatype = models.CharField(max_length=8, blank=True)
    subunit = models.CharField(max_length=8, blank=True)
    layer = models.CharField(max_length=8, blank=True)
    seqsref = models.CharField(max_length=8, blank=True)
    cellafr = models.CharField(max_length=8, blank=True)
    cellaly = models.CharField(max_length=8, blank=True)
    mimo44 = models.CharField(max_length=8, blank=True)
    mimo44p = models.CharField(max_length=8, blank=True)
    tsua = models.CharField(max_length=8, blank=True)
    tsub = models.CharField(max_length=8, blank=True)
    laye2 = models.CharField(max_length=8, blank=True)
    cdtmpl = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return self.cdtmpl    


class Tma(models.Model):

    cella = models.CharField(max_length=8, blank=True)
    bb = models.CharField(max_length=5, blank=True)
    seq = models.CharField(max_length=4, blank=True)
    radio = models.CharField(max_length=4, blank=True)
    rutype = models.CharField(max_length=10, blank=True)
    layer = models.CharField(max_length=10, blank=True)
    mimo = models.CharField(max_length=7, blank=True)
    mimop = models.CharField(max_length=7, blank=True)
    port = models.CharField(max_length=2, blank=True)
    serial1 = models.CharField(max_length=30, blank=True)
    serial2 = models.CharField(max_length=30, blank=True)
    dlAttenuation = models.CharField(max_length=30, blank=True)
    dlTrafficDelay = models.CharField(max_length=30, blank=True)
    ulTrafficDelay = models.CharField(max_length=30, blank=True)
    tmatype = models.CharField(max_length=4, blank=True)
    subunit = models.CharField(max_length=2, blank=True)
    codtmpl = models.CharField(max_length=4, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    tsua = models.CharField(max_length=2, blank=True)
    tsub = models.CharField(max_length=2, blank=True)
    laye2 = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.cella


class ScriptTma(models.Model):

    sito = models.CharField(max_length=5, blank=True)
    script1 = models.TextField()
    script2 = models.TextField()
    bb1 = models.CharField(max_length=5, blank=True)
    bb2 = models.CharField(max_length=5, blank=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ScriptTma"
        verbose_name_plural = "ScriptsTma"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.sito

class ScriptTmaLog(models.Model):

    id = models.AutoField(primary_key=True, default=1)
    sito = models.CharField(max_length=5, blank=True)
    bb = models.CharField(max_length=5, blank=True)
    script = models.TextField()
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ScriptTmaLog"
        verbose_name_plural = "ScriptsTmaLogs"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.sito
