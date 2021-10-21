from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.utils.translation import templatize
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
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
    author = models.ForeignKey(Authors, on_delete=models.CASCADE,
        related_name="authors")
    publication_date = models.PositiveIntegerField(
            validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.datetime.now().year)],
            help_text="Use the following format: <YYYY>")
    isbn = models.CharField(max_length=46)
    page_no = models.IntegerField()
    cover_link = models.CharField(max_length=1000)
    publication_language = models.ForeignKey(Languages, on_delete=CASCADE,
        related_name="languages")

    def __str__(self):
        template = """{0.title} {0.author} {0.publication_date} 
            {0.isbn} {0.page_no} {0.cover_link} {0.publication_language}
            """
        return template.format(self)

