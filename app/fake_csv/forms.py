from django.forms import ModelForm, TextInput, Select, NumberInput, inlineformset_factory

from .models import SchemaModel, ColumnModel


class SchemaForm(ModelForm):
    class Meta:
        model = SchemaModel
        fields = '__all__'
        widgets = {
            'name_schema': TextInput(
                attrs={
                    'class': 'form-group col-md-6',
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
        # INPUT_CLASS = 'input is-primary'
        # widgets = {
        #     'name': TextInput(attrs={
        #         'class': INPUT_CLASS,
        #     }),
        #     'type': Select(attrs={
        #         'class': 'select is-primary',
        #     }),
        #     'range_from': NumberInput(attrs={
        #         'class': INPUT_CLASS,
        #     }),
        #     'range_to': NumberInput(attrs={
        #         'class': INPUT_CLASS,
        #     }),
        #     'order': NumberInput(attrs={
        #         'class': INPUT_CLASS,
        #     }),
        # }


AddColumnFormSet = inlineformset_factory(
    SchemaModel, ColumnModel, form=ColumnForm,
    extra=1, can_delete=True, can_delete_extra=True
)
