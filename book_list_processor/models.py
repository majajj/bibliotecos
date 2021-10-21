
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.

#autorzy
#jezyki
#ksiazki

class Authors(models.Model):
    author = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.author

class Languages(models.Model):
    language = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.language

class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    publication_date = models.DateField(format="%Y")
    isbn = models.CharField(max_length=46)
    page_no = models.IntegerField()
    cover_link = models.CharField(max_length=1000)
    pulication_language = models.ForeignKey(Languages, on_delete=CASCADE, related_name="languages")

    def __str__(self):
        return self