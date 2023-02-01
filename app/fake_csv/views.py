from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView
)

from fake_csv.forms import (
    SchemaForm,
    ColumnForm,
    AddColumnFormSet
)
from fake_csv.models import (
    SchemaModel,
    ColumnModel,
    DataSetsModel
)


def login(request):
    # Start page
    return render(request, 'fake_csv/login.html')


# def new_schema(request):
#     schema_form = SchemaForm()
#     column_form = ColumnForm()
#     context = {
#         'schema_form': schema_form,
#         'column_form': column_form,
#     }
#     return render(request, 'fake_csv/new_schema.html', context)
#
#
# def data_schemas(request):
#     return render(request, 'fake_csv/data_schemas.html')
#
#
# def data_sets(request):
#     return render(request, 'fake_csv/data_sets.html')


class SchemaInLine:
    form_class = SchemaForm
    model = SchemaModel
    template_name = 'fake_csv/new_schema.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('schema:list_columns')

    def formset_columns_valid(self, formset):
        columns = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for column in columns:
            column.schema = self.object
            column.save()


class SchemaCreateView(SchemaInLine, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(SchemaCreateView, self).get_context_data(**kwargs)
        ctx['named_formset'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'columns': AddColumnFormSet(prefix='columns')
            }
        else:
            return {
                'columns': AddColumnFormSet(self.request.POST or None,
                                            self.request.FILES or None,
                                            prefix='columns')
            }


class SchemaUpdateView(SchemaInLine, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(SchemaUpdateView, self).get_context_data(**kwargs)
        ctx['named_formset'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'columns': AddColumnFormSet(self.request.POST or None,
                                        self.request.FILES or None,
                                        instance=self.object,
                                        prefix='columns')
        }


class SchemaListView(ListView):
    model = SchemaModel
    template_name = 'fake_csv/data_schemas.html'
    context_object_name = 'schemas'


def delete_column(request, pk):
    try:
        column = ColumnModel.objects.get(id=pk)
    except ColumnModel.DoesNotExist:
        messages.success(
            request, 'Object does not exist'
        )
        return redirect('schemas:update_schemas', pk=column.schema.id)

    column.delete()
    messages.success(
        request, 'Column deleted successfully'
    )
    return redirect('schemas:update_schemas', pk=column.schema.id)


def delete_schema(request, pk):
    try:
        schemas = SchemaModel.objects.get(id=pk)
    except SchemaModel.DoesNotExist:
        messages.success(
            request, 'Object does not exist'
        )
        return redirect('schema:update_schema', pk=id)

