from django.forms import ModelForm, TextInput, Select, NumberInput, inlineformset_factory

from .models import SchemaModel, ColumnModel


class SchemaForm(ModelForm):
    class Meta:
        model = SchemaModel
        fields = '__all__'

        widgets = {
            'name_schema': TextInput(
                attrs={
                    'class': 'name_schema',
                }
            ),
            'column_separator': Select(
                attrs={
                    'class': 'column_separator',

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
            'name': TextInput(attrs={
                'class': 'name_column',
            }),
            'type': Select(attrs={
                'class': 'type_column',
            }),
            'range_from': NumberInput(attrs={
                'class': 'range_from',
                # 'style': 'visibility: hidden',
            },
            ),
            'range_to': NumberInput(attrs={
                'class': 'range_to',
                # 'style': 'visibility: hidden',
            }),
            'order': NumberInput(attrs={
                'class': 'order_column',
            }),
        }



AddColumnFormSet = inlineformset_factory(
    SchemaModel, ColumnModel, form=ColumnForm,
    extra=1, can_delete=True, can_delete_extra=True
)
