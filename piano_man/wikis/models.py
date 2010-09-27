from django.db import models
from django_vcs.models import CodeRepository

class VCSWiki(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    repo = models.ForeignKey(CodeRepository)

    def __unicode__(self):
        return self.name

