from django.contrib import admin

# Register your models here.
from .models import Books, KeywordsToSearch, Languages, Authors

admin.site.register(Books)
admin.site.register(Languages)
admin.site.register(Authors)
admin.site.register(KeywordsToSearch)