
from rest_framework import serializers    
from django.db import models
from .models import Books, Languages, Authors
# from typing_extensions import Required

class AuthorsSerializer(serializers.Serializer):
    author = serializers.CharField( max_length=255)

    class Meta:
        model = Authors

class LanguagesSerializer(serializers.Serializer):
    language = serializers.CharField( max_length=255)

    class Meta:
        model = Languages

class BooksSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    author = serializers.CharField()
    publication_date = serializers.CharField()
    isbn = serializers.CharField(max_length=46)
    page_no = serializers.IntegerField()
    cover_link = serializers.CharField(max_length=1000)
    publication_language = serializers.CharField()

    class Meta:
        model = Books
        optional_fields = ['publication_date', 'isbn', 'page_no', 'cover_link']