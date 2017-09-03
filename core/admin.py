from django.contrib import admin
from core.models import Wiki

class WikiAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wiki, WikiAdmin)
