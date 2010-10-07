from django.db import models
from django_vcs.models import CodeRepository
from wikis.models import VCSWiki
import jsonfield


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    description_type = models.CharField(max_length=20,blank=True)
    repo = models.ForeignKey(CodeRepository,related_name='project_code',blank=True,null=True)
    wiki = models.ForeignKey(VCSWiki,related_name='project_wikis',blank=True,null=True)
    upload_location = models.CharField(max_length=255,blank=True)
    config_options = jsonfield.JSONField(blank=True,null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('projects.views.project', (self.slug,), {})



