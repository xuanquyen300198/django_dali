# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import FieldDoesNotExist
from django.db import models

# Create your models here.
class table_color_tmp(models.Model):
    code_hex = models.CharField(max_length=100)
    code_dali = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    code_img = models.CharField(max_length=100)
    def as_dict(self):
        return {'code_hex': self.code_hex, 'code_dali': self.code_dali,'code_img': self.code_img}
class table_color_fomat(models.Model):
    code_hex = models.CharField(max_length=100)
    code_dali = models.CharField(max_length=100)
    number_img = models.IntegerField() 
    code_rgb = models.CharField(default=None, blank=True, null=True,max_length=100)
    def as_dict(self):
        return {'code_hex': self.code_hex, 'code_dali': self.code_dali,'number_img': self.number_img,'code_rgb': self.code_rgb}

class ImageObj(models.Model):
    caption=models.CharField(max_length=100)
    image=models.ImageField(upload_to="img/%y")
    def __str__(self):
        return self.caption
