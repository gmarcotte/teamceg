from django.contrib import admin
from pear.projects.models import Author

admin.site.register(Author, AuthorAdmin)