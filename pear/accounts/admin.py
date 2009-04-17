from django.contrib import admin

from pear.accounts import models

admin.site.register(models.PearUser, admin.ModelAdmin)
