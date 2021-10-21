from django.urls import path

from .views import \
    BookUpdate, \
    available_book_displaying,\
    execute_book_search, \
    add_new_book, \
    book_search_parameter


urlpatterns = [
    path('execute-book-search/', execute_book_search, name="search"),
    path('available-book-displaying/', available_book_displaying, name="books"),
    path('add-new-book/', add_new_book, name="add"),
    path('books-form/<int:pk>/', BookUpdate.as_view(), name="books_form"),
    path('search-keywords/', book_search_parameter, name="search_keywords")
]
