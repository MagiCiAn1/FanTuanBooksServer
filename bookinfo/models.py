# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BookInfo(models.Model):
	id = models.IntegerField(primary_key=True, auto_created=True)
	bookName = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	intro = models.TextField()
	img = models.CharField(max_length=255)
	type = models.CharField(max_length=255)
	base_link = models.TextField()