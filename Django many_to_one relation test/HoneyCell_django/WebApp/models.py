from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Reporter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return "%s %s, %s" %(self.first_name, self.last_name, self.email)

    class Meta:
        ordering = ('first_name', )


class Article(models.Model):
    # if you delete a reporter, his article also will be deleted
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    headline = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    pub_date = models.DateField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s, %s, %s" %(self.headline, self.content, self.pub_date)

    class Meta:
        ordering = ('headline', )