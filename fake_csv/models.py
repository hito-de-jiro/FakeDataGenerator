from django.db import models


class UserModel(models.Model):
    login = models.CharField(max_length=45, verbose_name='Login')
    password = models.CharField(max_length=45, verbose_name="Password")


class NewSchemaModel(models.Model):
    name_schema = models.CharField(max_length=45, verbose_name='New schema')
    column_separator = models.CharField(max_length=45, verbose_name='Column separator')
    string_character = models.CharField(max_length=45, verbose_name='String character')
    add_column = models.ForeignKey('AddColumnModel', on_delete=models.PROTECT)


class AddColumnModel(models.Model):
    column_name = models.CharField(max_length=45, verbose_name='Column name')
    column_type = models.CharField(max_length=45, verbose_name='Column type')
    order = models.PositiveSmallIntegerField(verbose_name='Order')
    range_int = models.ForeignKey('RangeAgeModel', on_delete=models.PROTECT)


class RangeAgeModel(models.Model):
    range_from = models.PositiveSmallIntegerField(verbose_name='From')
    range_to = models.PositiveSmallIntegerField(verbose_name='To')


class DataSetsModel(models.Model):
    to_created = models.DateField(auto_now_add=True, verbose_name='Created')
    num_rows = models.PositiveIntegerField(verbose_name='Rows')
