from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import AddColumnFormSet, LoginForm, ColumnForm, SchemaForm
from .models import SchemaModel


# import pdb


class SchemaListView(ListView):
    model = SchemaModel
    template_name = 'schema_list.html'


class SchemaDetailView(DetailView):
    model = SchemaModel
    template_name = 'detail'
    fields = '__all__'
    success_url = "data_sets.html"


class SchemaCreateView(CreateView):
    model = SchemaModel
    fields = [
        'name',
        'column_separator',
        'string_character',
    ]

    def get_context_data(self, **kwargs):
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

        # pdb.set_trace()
        if columns_fs.is_valid():
            for instance in columns_fs:
                if instance in columns_fs.deleted_forms:
                    continue
                column = instance.save(commit=False)
                column.schema = new_parent
                print(1111)
                column.save()

        else:

            print(columns_fs.errors)
            return self.form_invalid(parent_form)
        # pdb.set_trace()

        return super().form_valid(parent_form)

    def get_success_url(self):
        return reverse("schema_list")


class SchemaUpdateView(UpdateView):
    model = SchemaModel
    template_name = 'edit'
    fields = '__all__'

    success_url = "/"


class SchemaDeleteView(DeleteView):
    model = SchemaModel
    template_name = 'schema_delete.html'
    success_url = reverse_lazy('schema_list')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'fake_csv/login.html', {'form': form})
