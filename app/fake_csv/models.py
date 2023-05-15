from django.db import models


class SchemaModel(models.Model):
    name = models.CharField(max_length=45, verbose_name='Name schema')
    SEPARATOR_COLUMN = (
        (',', 'Coma'),
        ('|', 'Pipe'),
        (';', 'Semicolon'),
        ('    ', 'Tab'),
    )
    column_separator = models.CharField(max_length=45,
                                        verbose_name='Column separator',
                                        choices=SEPARATOR_COLUMN,
                                        default='coma')
    CHARACTER_STRING = (
        ('"', 'Double-quote'),
        ("'", 'Quote'),
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
        ('integer', 'Integer'),
        ('phone', 'Phone'),
        ('email', 'E-mail'),
        ('address', 'Address'),
    )
    type = models.CharField(max_length=45,
                            verbose_name='Column type',
                            default='fullname',
                            choices=TYPE_COLUMN)
    range_from = models.PositiveSmallIntegerField(default=16, verbose_name='From', null=True, blank=True)
    range_to = models.PositiveSmallIntegerField(default=65, verbose_name='To', null=True, blank=True)
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE, null=True)
    order = models.PositiveSmallIntegerField(verbose_name='Order', null=True, blank=True)

    class Meta:
        verbose_name = "column"
        verbose_name_plural = "columns"
        ordering = ['order']

    def __str__(self):
        return self.name


class DatasetModel(models.Model):
    created = models.DateField(auto_now_add=True, verbose_name='Created')
    status = models.CharField(default='Processing...', max_length=45,
                              null=True, verbose_name='Status')
    file = models.CharField(default='File does not exist.', max_length=100, null=True, verbose_name='path_to_file')
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "dataset"
        verbose_name_plural = "datasets"
