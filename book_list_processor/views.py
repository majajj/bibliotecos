from django import forms
from django.shortcuts import render
from rest_framework.exceptions import ErrorDetail
from .models import Authors, Languages, Books
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .config import list_of_choices, list_of_book_parameters
import requests
from datetime import datetime
from .serializers import BooksSerializer, AuthorsSerializer, LanguagesSerializer
from django.views.generic.edit import UpdateView
# Create your views here.

class NewBookForm(forms.Form):
    title = forms.CharField(label="Title")
    publication_date = forms.DateField(label="Publication date", required=False)
    isbn = forms.CharField(label="ISBN", required=False)
    page_no = forms.IntegerField(label="Page no", required=False)
    cover_link = forms.URLField(label="Cover link", required=False)
    author = forms.CharField(label="Author")
    publication_language = forms.CharField(label="Publication language")

class BookFromAPI(forms.Form):
    field = forms.CharField(label="title")
    keyword_descr = forms.ChoiceField(label="keyword description",
        choices=list_of_choices)
    parameter = forms.CharField(label="parameter")

class BookSearchParameter(forms.Form):
    searched_field = forms.ChoiceField(label="search field",
        choices=list_of_book_parameters)
    key_word = forms.CharField(label="Key word to search")

class BookUpdate(UpdateView):
    model = Books
    fields = ['title', 'publication_date', 'isbn', 'page_no',
        'cover_link', 'author', 'publication_language']

    def get_success_url(self):
        return reverse("books")

def book_search_parameter(request):

    if request.method == "GET":
        form = BookSearchParameter(request.GET)
        if form.is_valid():
            book_data= form.data
            column = book_data["searched_field"]
            key_word = book_data["key_word"]
            if column == "author":
                data = {f'{column}__{column}__contains': key_word}
                books = Books.objects.all().filter(**data)
            elif column == "publication_language":
                books = Books.objects.all().filter(
                    publication_language__language__contains=key_word)
            else:
                data = {f'{column}__contains': key_word}
                books = Books.objects.all().filter(**data)

            return render(request, "book_list_processor/books.html",{
                "books": books
            })

        else:
            return render(request, "book_list_processor/search_keywords.html", {
            "form": form
            })
    else:
        return render(request, "book_list_processor/search_keywords.html", {
            "form": BookSearchParameter()
        })

def available_book_displaying(request):
    try:
        return render(request, "book_list_processor/books.html",{
            "books": Books.objects.all()
            })
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def get_data_from_api(title, parameter, keyword_descr):
    base_url = "https://www.googleapis.com/books/v1/volumes?q="
    url = f"{base_url}{title}+{keyword_descr}:{parameter}"
    return requests.get(url=url)



def insert_into_authors(inserted_author):
    try:
        author_id = Authors.objects.get(author=inserted_author)
        author_id = author_id.id
        return author_id
    except ObjectDoesNotExist:
        author_id = Authors.objects.create(author=inserted_author)
        author_id = Authors.objects.get(author=inserted_author)
        author_id = author_id.id
        return author_id

def insert_into_language(inserted_language):
    try:
        language_id = Languages.objects.get(language=inserted_language)
        language_id = language_id.id
        return language_id
    except ObjectDoesNotExist:
        language_id = Languages.objects.create(language=inserted_language)
        language_id = Languages.objects.get(language=inserted_language)
        language_id = language_id.id
        return language_id

def insert_into_book(inserted_title,
                    inserted_publ_date,
                    inserted_isbn,
                    inserted_page_no,
                    inserted_cover_link,
                    language_id,
                    author_id):

    new_book = Books.objects.create(title=inserted_title,
                                    author_id=author_id,
                                    publication_date=inserted_publ_date,
                                    isbn=inserted_isbn,
                                    page_no=inserted_page_no,
                                    cover_link=inserted_cover_link,
                                    publication_language_id=language_id)
    return new_book

def data_validation_language(language):

        valid_language = LanguagesSerializer(
            data={"language":language["language"]})
        if valid_language.is_valid():
            language_id = insert_into_language(
                inserted_language=language["language"])
            return language_id
        else:
            print(valid_language.errors)
            return HttpResponseRedirect(reverse("books"))

def data_validation_author(author):
        valid_author = AuthorsSerializer(
            data={"author": author["authors"][0]})
        if valid_author.is_valid():
            author_id = insert_into_authors(
                inserted_author=author["authors"][0])
            return author_id
        else:
            print(valid_author.errors)
            return HttpResponseRedirect(reverse("books"))

def data_validation_books(searched_books, i, author_id, language_id):
        volume_info = searched_books["items"][i]["volumeInfo"]
        try:
            data_to_import = {
                "title": volume_info["title"], 
                "author":author_id, 
                "publication_date": volume_info["publishedDate"][:4], 
                "isbn": volume_info["industryIdentifiers"][i]["type"],
                "page_no": volume_info["pageCount"],
                "cover_link": searched_books["items"][i]["selfLink"],
                "publication_language": language_id
                }
            valid_books = BooksSerializer(data=data_to_import)
            if valid_books.is_valid():
                insert_into_book(inserted_title=volume_info["title"],
                    inserted_publ_date=volume_info["publishedDate"][:4],
                    inserted_isbn=volume_info["industryIdentifiers"][0]["type"],
                    inserted_page_no=volume_info["pageCount"],
                    inserted_cover_link=searched_books["items"][i]["selfLink"],
                    language_id=language_id,
                    author_id=author_id)
            else:
                print(valid_books.errors)
                return HttpResponseRedirect(reverse("books"))
        except:
            return ErrorDetail


def import_from_api(searched_books):
    i=0
    for i in range(len(searched_books["items"])):
        volume_info = searched_books["items"][i]["volumeInfo"]
        language_id = data_validation_language(language=volume_info)
        author_id = data_validation_author(author=volume_info)
        data_validation_books(searched_books, i,
            author_id=author_id, language_id=language_id)


def execute_book_search(request):
    if request.method == "GET":
        form = BookFromAPI(request.GET)
        if form.is_valid():
            search_data= form.data
            searched_books = get_data_from_api(title=search_data["field"],
                parameter=search_data["parameter"],
                keyword_descr=search_data["keyword_descr"])
            searched_books = searched_books.json()
            import_from_api(searched_books=searched_books)
            form.full_clean()
            return HttpResponseRedirect(reverse("books"))
        else:
            return render(request, "book_list_processor/search.html", {
                "form": form
            })
    else:
        return render(request, "book_list_processor/search.html", {
            "form": BookFromAPI()
        })


def add_new_book(request):
    if request.method == "POST":
        form = NewBookForm(request.POST)
        if form.is_valid():
            book_data= form.data
            language_id = insert_into_language(
                inserted_language=book_data["publication_language"])
            author_id = insert_into_authors(
                inserted_author=book_data["author"])
            insert_into_book(inserted_title=book_data["title"],
                inserted_publ_date=book_data["publication_date"][:4],
                inserted_isbn=book_data["isbn"],
                inserted_page_no=book_data["page_no"],
                inserted_cover_link=book_data["cover_link"],
                language_id=language_id,
                author_id=author_id)
            form.full_clean()
            return HttpResponseRedirect(reverse("books"))
        else:
            return render(request, "book_list_processor/add.html", {
                "form": form
            })
    else:
        return render(request, "book_list_processor/add.html", {
            "form": NewBookForm()
        })