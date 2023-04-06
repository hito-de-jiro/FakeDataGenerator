from django.db import models
from django.urls import reverse


class SchemaModel(models.Model):
    name = models.CharField(max_length=45, verbose_name='Name schema')
    SEPARATOR_COLUMN = (
        ('coma', 'Coma'),
        ('pipe', 'Pipe'),
        ('semicolon', 'Semicolon'),
        ('tab', 'Tab'),
    )
    column_separator = models.CharField(max_length=45,
                                        verbose_name='Column separator',
                                        choices=SEPARATOR_COLUMN,
                                        default='coma')
    CHARACTER_STRING = (
        ('double-quote', 'Double-quote'),
        ('quote', 'Quote'),
    )
    string_character = models.CharField(max_length=45,
                                        verbose_name='String character',
                                        choices=CHARACTER_STRING,
                                        default='double-quote')
    modified = models.DateTimeField(auto_now=True, verbose_name='modified')

    class Meta:
        verbose_name = "schema"
        verbose_name_plural = "schemas"

    def __str__(self):
        return self.name


class ColumnModel(models.Model):
    name = models.CharField(max_length=45, verbose_name='Column name')
    TYPE_COLUMN = (
        ('fullname', 'Full name'),
        ('age', 'Age'),
        ('phone', 'Phone'),
        ('email', 'E-mail'),
        ('address', 'Address'),
    )
    type = models.CharField(max_length=45,
                            verbose_name='Column type',
                            default='fullname',
                            choices=TYPE_COLUMN)
    range_from = models.PositiveSmallIntegerField(verbose_name='From', null=True, blank=True)
    range_to = models.PositiveSmallIntegerField(verbose_name='To', null=True, blank=True)
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE, null=True)
    order = models.PositiveSmallIntegerField(verbose_name='Order', null=True, blank=True)

    class Meta:
        verbose_name = "column"
        verbose_name_plural = "columns"

    def __str__(self):
        return self.name


class DataSetsModel(models.Model):
    created = models.DateField(auto_now_add=True, verbose_name='Created')
    num_rows = models.PositiveIntegerField(verbose_name='Rows')
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('data_sets', args=[str(self.schema)])
