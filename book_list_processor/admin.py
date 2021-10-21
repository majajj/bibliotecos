from django.contrib import admin

# Register your models here.
from .models import Books, Languages, Authors

admin.site.register(Books)
admin.site.register(Languages)
admin.site.register(Authors)