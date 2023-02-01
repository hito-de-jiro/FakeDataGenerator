from django.db import models


class SchemaModel(models.Model):
    name_schema = models.CharField(max_length=45, verbose_name='Name schema')
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
    modified = models.DateTimeField(auto_now_add=True, verbose_name='modified')

    def __str__(self):
        return self.name_schema


class ColumnModel(models.Model):
    column_name = models.CharField(max_length=45, verbose_name='Column name')
    TYPE_COLUMN = (
        ('fullname', 'Full name'),
        ('age', 'Age'),
        ('phone', 'Phone'),
        ('email', 'E-mail'),
        ('address', 'Address'),
    )
    column_type = models.CharField(max_length=45,
                                   verbose_name='Column type',
                                   choices=TYPE_COLUMN)
    range_from = models.PositiveSmallIntegerField(default=18, verbose_name='From')
    range_to = models.PositiveSmallIntegerField(default=60, verbose_name='To')
    order = models.PositiveSmallIntegerField(verbose_name='Order')
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.schema.name_schema


class DataSetsModel(models.Model):
    to_created = models.DateField(auto_now_add=True, verbose_name='Created')
    num_rows = models.PositiveIntegerField(verbose_name='Rows')
