from models import Project, AvailableOption, ProjectOptionSelection
from django.contrib import admin


class AvailableOptionAdmin(admin.ModelAdmin):
    pass

class ProjectOptionSelectionAdmin(admin.TabularInline):
    model = ProjectOptionSelection

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProjectOptionSelectionAdmin,]


admin.site.register(Project,ProjectAdmin)
admin.site.register(AvailableOption,AvailableOptionAdmin)
