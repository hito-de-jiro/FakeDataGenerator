from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import AddColumnFormSet, LoginForm, ColumnForm, SchemaForm
from .models import SchemaModel

import pdb


class SchemaListView(ListView):
    model = SchemaModel


class SchemaDetailView(DetailView):
    model = SchemaModel
    fields = '__all__'
    template_name = 'fake_csv/data_sets.html'
    success_url = 'schema_detail'

    def get_success_url(self):
        return reverse("schema_edit")


class SchemaCreateView(CreateView):
    model = SchemaModel
    template_name = "fake_csv/schema_form.html"
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

        if columns_fs.is_valid():
            for instance in columns_fs:
                if instance in columns_fs.deleted_forms:
                    continue
                column = instance.save(commit=False)
                column.schema = new_parent
                column.save()
        else:
            return self.form_invalid(parent_form)
        # pdb.set_trace()

        return super().form_valid(parent_form)

    def get_success_url(self):
        return reverse("schema_list")


def update_schema(request, pk):
    parent_obj = get_object_or_404(SchemaModel, pk=pk)
    if request.method == 'POST':
        parent_form = SchemaForm(request.POST, instance=parent_obj)
        formset = AddColumnFormSet(request.POST, instance=parent_obj)
        if parent_form.is_valid():
            parent_form.save()
            if formset.is_valid():
                formset.save()
                return redirect('schema_list')
    else:
        parent_form = SchemaForm(instance=parent_obj)
        formset = AddColumnFormSet(instance=parent_obj)

    formset.extra = 0
    context = {
        'form': parent_form,
        'columns': formset,
    }

    return render(request, 'fake_csv/schema_update.html', context=context)


class SchemaDeleteView(DeleteView):
    model = SchemaModel
    template_name = 'fake_csv/schema_delete.html'

    def get_success_url(self):
        return reverse("schema_list")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully!')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login! Try again!')
    else:
        form = LoginForm()

    return render(request, 'fake_csv/login.html', {'form': form})
