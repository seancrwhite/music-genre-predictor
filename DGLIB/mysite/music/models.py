# from django.db import models
# #
# # class Document(models.Model):
# #     upload_by = models.ForeignKey('auth.User', related_name='uploaded_documents')
# #     datestamp = models.DateTimeField(auto_now_add=True)
# #     document = models.Field(upload_to='uploads/')
# #
# #
# # class MainModel(models.Model):
# #     title = models.CharField(max_length=42)
# #     document = models.ForeignKey(Document)
#
# class Profile(models.Model):
#    name = models.CharField(max_length = 50)
#    audio = models.FileField(upload_to = 'audio')
#
#    class Meta:
#       db_table = "profile"
#

# -*- coding: utf-8 -*-
from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')