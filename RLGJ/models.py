# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Kaqin(models.Model):
    idcard = models.CharField(max_length=255, blank=True, null=True)
    passtime = models.DateTimeField(db_column='passTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'kaqin'


class ZzfkjVisit(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    idcard = models.CharField(max_length=255, blank=True, null=True)
    idcardimg = models.CharField(db_column='idCardImg', max_length=255, blank=True, null=True)  # Field name made lowercase.
    loginimag = models.CharField(db_column='loginImag', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(blank=True, null=True)
    isblacklist = models.IntegerField(db_column='isBlackList', blank=True, null=True)  # Field name made lowercase.
    inblackdate = models.DateTimeField(db_column='inBlackDate', blank=True, null=True)  # Field name made lowercase.
    outblackdate = models.DateTimeField(db_column='outBlackDate', blank=True, null=True)  # Field name made lowercase.
    addtime = models.DateTimeField(db_column='addTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'zzfkj_visit'
