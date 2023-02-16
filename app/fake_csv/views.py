from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import AddColumnFormSet
from .models import SchemaModel


def login(request):
    # Start page
    return render(request, 'fake_csv/login.html')


class SchemaListView(ListView):
    model = SchemaModel
    template_name = 'schema_list.html'


class SchemaCreateView(CreateView):
    model = SchemaModel
    fields = [
        'name',
        'column_separator',
        'string_character'
    ]

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = AddColumnFormSet(self.request.POST)
        else:
            data['columns'] = AddColumnFormSet()
        return data

    def form_valid(self, parent_form):
        context = self.get_context_data()
        columns_fs: AddColumnFormSet = context['columns']

        new_parent = parent_form.save()

        if columns_fs.is_valid():
            for instance in columns_fs:
                # import pdb
                # pdb.set_trace()
                column = instance.save(commit=False)
                column.schema = new_parent
                column.save()

        return super().form_valid(parent_form)

    def get_success_url(self):
        return reverse("schema_list")
