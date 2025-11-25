from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import math


class Sezione(models.Model):
    """
    Modello generico di una sezione del Forum.
    Le sezioni dividono il sito per categorie di discussione.
    Ciascuna sezione contiene svariate Discussioni.
    Le sezioni vengono create dagli amministratori del sito.
    """

    nome_sezione = models.CharField(max_length=80)
    descrizione = models.CharField(max_length=150, blank=True, null=True)
    logo_sezione = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = "Sezione"
        verbose_name_plural = "Sezioni"

    def __str__(self):
        return self.nome_sezione

    def get_absolute_url(self):
        return reverse("sezione_view", kwargs={"pk": self.pk})

    def get_last_discussions(self):
        """Restituisce le ultime due discussioni della sezione, ordinate per data"""
        return Discussione.objects.filter(sezione_appartenenza=self).order_by("-data_creazione")[:2]

    def get_number_of_posts_in_section(self):
        """Restituisce il numero di post totali presenti in una istanza di sezione"""
        return Post.objects.filter(discussione__sezione_appartenenza=self).count()


class Discussione(models.Model):
    """
    Il modello di una singola discussione del forum.
    Ogni discussione "fa parte" di una specifica sezione.
    Le discussioni possono essere create da tutti gli utenti del sito.
    """

    titolo = models.CharField(max_length=120)
    data_creazione = models.DateTimeField(auto_now_add=True)
    autore_discussione = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="discussioni"
    )
    sezione_appartenenza = models.ForeignKey(Sezione, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Discussione"
        verbose_name_plural = "Discussioni"

    def __str__(self):
        return self.titolo

    def get_absolute_url(self):
        return reverse("visualizza_discussione", kwargs={"pk": self.pk})

    def get_n_pages(self):
        """
        Restituisce il numero di pagina presenti in una istanza di Discussione.
        math.ceil https://docs.python.org/3.6/library/math.html#math.ceil
        restituisce il numero intero successivo al float passato come parametro (es 3.1 ==> 4)
        o restituisce lo stesso numero se intero
        """
        posts_discussione = self.post_set.count()
        n_pagine = math.ceil(posts_discussione / 5)
        return n_pagine


class Post(models.Model):
    """
    Il modello di un singolo Post.
    I post rappresentano i singoli messaggi delle discussioni, e per questo motivo
    ogni post "fa parte" di una specifica discussione.
    Ogni user del sito può partecipare alle discussioni aggiungendo nuovi post.
    """

    autore_post = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    discussione = models.ForeignKey(Discussione, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        """per comodità di lettura dalla sezione admin"""
        return self.autore_post.username