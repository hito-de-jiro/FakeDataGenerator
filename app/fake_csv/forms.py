from django import forms
from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm,
    TextInput,
    Select,
    NumberInput,
    inlineformset_factory, BaseInlineFormSet,
)


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
                'required': 'true',
            }),
            'type': Select(attrs={
                'class': 'type_column',
            }),
            'range_from': NumberInput(attrs={
                'class': 'range_from',
            },
            ),
            'range_to': NumberInput(attrs={
                'class': 'range_to',
            }),
            'order': NumberInput(attrs={
                'class': 'order_column',
                'required': 'true',
            }),
        }

    def clean_title(self):
        order = self.cleaned_data['order']
        if order == 1:
            raise ValidationError('Please correct the duplicate values below.')
        return order


class HideDeleteCheckbox(BaseInlineFormSet):
    pass


AddColumnFormSet = inlineformset_factory(
    SchemaModel, ColumnModel, form=ColumnForm,
    extra=1, can_delete=True, can_delete_extra=True,
)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
