from django.forms import ModelForm, TextInput, Select, NumberInput, inlineformset_factory

from .models import SchemaModel, ColumnModel


class SchemaForm(ModelForm):
    class Meta:
        model = SchemaModel
        fields = '__all__'
        widgets = {
            'name_schema': TextInput(
                attrs={
                    'class': 'input is-primary',
                }
            ),
            'column_separator': Select(
                attrs={
                    'class': 'select is-primary',
                    'id': 'id_column_separator',
                }
            ),
            'string_character': Select(
                attrs={
                    'class': 'string_character',
                }
            ),
        }


class ColumnForm(ModelForm):
    class Meta:
        model = ColumnModel
        fields = '__all__'
        widgets = {
            'column_name': TextInput(attrs={
                'class': 'input is-primary',
            }),
            'column_type': Select(attrs={
                'class': 'select is-primary',
            }),
            'range_from': NumberInput(attrs={
                'class': 'input is-primary',
            }),
            'range_to': NumberInput(attrs={
                'class': 'input is-primary',
            }),
            'order': NumberInput(attrs={
                'class': 'input is-primary',
            }),
        }


AddColumnFormSet = inlineformset_factory(
    SchemaModel, ColumnModel, form=ColumnForm,
    extra=1, can_delete=True, can_delete_extra=True
)
