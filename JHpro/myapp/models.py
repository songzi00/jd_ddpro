# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    press = models.CharField(max_length=255, blank=True, null=True)
    book_date = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    com_num = models.CharField(max_length=255, blank=True, null=True)
    book_size = models.CharField(max_length=255, blank=True, null=True)
    book_number = models.CharField(max_length=255, blank=True, null=True)
    book_type = models.CharField(max_length=32, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'
