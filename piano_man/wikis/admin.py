from models import VCSWiki
from django.contrib import admin

class VCSWikiAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(VCSWiki,VCSWikiAdmin)


