import math
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Sezione(models.Model):
    """ 
    Le sezioni dividono il sito per categorie di discussione.
    ciascuna sezione contiene svariate Discussioni create dagli 
    amministratori del sito.
    """
    nome_sezione = models.CharField(max_length=80)
    logo_sezione = models.ImageField(blank=True, null=True)
    descrizione = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return self.nome_sezione
    
    def get_absolute_url(self):
        return reverse("sezione_view",kwargs={"pk":self.pk})
    
    def get_last_discussions(self):
        return Discussione.objects.filter(
            sezione_appartenenza = self
        ).order_by("-data_creazione")[:2]
    
    def get_number_of_posts_in_section(self):
        return Post.objects.filter(discussione__sezione_appartenenza = self).count()

    class Meta:
        verbose_name = "Sezione"
        verbose_name_plural = "Sezioni"


class Discussione(models.Model):
    """
    Le discussioni sono create dagli utenti e rappresentano 
    la categoria dei vari Posts.
    """
    
    titolo = models.CharField(max_length=120)
    data_creazione = models.DateTimeField(auto_now_add=True)
    sezione_appartenenza = models.ForeignKey(Sezione,on_delete=models.CASCADE)
    autore_discussione = models.ForeignKey(User,on_delete=models.CASCADE,related_name="discussioni")

    def __str__(self):
        return self.titolo
    
    def get_absolute_url(self):
        return reverse("discussione_view",kwargs={"pk":self.pk})

    def get_n_pages(self):
        posts_discussione = self.post_set.count()
        n_page = math.ceil(posts_discussione / 5)
        return n_page

    class Meta:
        verbose_name = "Discussione"
        verbose_name_plural = "Discussioni"


class Post(models.Model):
    """ 
    Il post è creato dal Utente e caratterizza il 
    contenuto della discussione. 
    """
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    autore_post = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    discussione = models.ForeignKey(Discussione, on_delete=models.CASCADE)

    def __str__(self):
        return self.autore_post.username

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
