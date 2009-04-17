from django.contrib import admin

from pear.accounts import models

class PearUserOptions(admin.ModelAdmin):
  list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 
                  'is_superuser', 'last_login', 'date_joined')
  list_filter = ('is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login',)
  exclude = ('username', 'password', 'last_login', 'date_joined',)

admin.site.register(models.PearUser, PearUserOptions)
