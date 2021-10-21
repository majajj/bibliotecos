from django.shortcuts import render
from django.views import generic
from rest_framework_json_api import filters
from rest_framework_json_api import django_filters
from rest_framework import viewsets#, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from book_list_processor.serializers import BooksSerializer
from book_list_processor.models import Books

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer


class SearchViewset(generic.ListView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'authors__author',
        'publication_date', 'languages__publication_language']
