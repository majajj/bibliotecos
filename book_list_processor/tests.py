from book_list_processor.models import Authors, Books, Languages
import unittest
from django.test import TestCase
from django.test.client import Client
from rest_framework import response


from .views import insert_into_language


def test_language(language, expected_language):
    if insert_into_language(language) != expected_language:
        print(f"""ERROR!!! on insert_into_language({language}), 
        expected {expected_language}""")

# Create your tests here.
class Tests(TestCase):
    
    def setUp(self):
        author_id = Authors.objects.create(author='Austen')
        language_id = Languages.objects.create(language='en')
        a1 = Books.objects.create(title="Perswazje",
            author=author_id,
            publication_date='1999',
            isbn='ISBN_10',
            page_no=246,
            cover_link='https://www.googleapis.com/books/v1/volumes/aQg_AwEACAAJ)', # noqa
            publication_language=language_id) 

    def test_1(self):
        self.assertTrue(insert_into_language('en')==1)

    def test_2(self):
        self.assertTrue(insert_into_language('pl')==2)

    def test_valid_add(self):
        c = Client()
        response = c.get("/book-list-processor/add-new-book/")
        self.assertEqual(response.status_code, 200)

    def test_valid_books(self):
        c = Client()
        response = c.get("/book-list-processor/available-book-displaying/")
        self.assertEqual(response.status_code, 200)

    def test_books_form(self):
        book1 = Books.objects.get(pk=1)
        c = Client()
        response = c.get(f"/book-list-processor/books-form/{book1.id}/")
        self.assertEqual(response.status_code, 200)

    def test_search_keywords(self):
        c = Client()
        response = c.get(f"/book-list-processor/search-keywords/")
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        c = Client()
        response = c.get(f"/book-list-processor/execute-book-search/")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()