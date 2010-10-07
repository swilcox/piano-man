from django.db import models
from django_vcs.models import CodeRepository
from wikis.models import VCSWiki


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    description_type = models.CharField(max_length=20,blank=True)
    repo = models.ForeignKey(CodeRepository,related_name='project_code',blank=True,null=True)
    wiki = models.ForeignKey(VCSWiki,related_name='project_wikis',blank=True,null=True)
    upload_location = models.CharField(max_length=255,blank=True)
    
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('projects.views.project', (self.slug,), {})


class AvailableOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ProjectOptionSelection(models.Model):
    project = models.ForeignKey(Project,related_name='configuration')
    option = models.ForeignKey(AvailableOption,related_name='selection')
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.option) + str(self.value)

