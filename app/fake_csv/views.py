# fake_csv/views.py
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from .forms import AddColumnFormSet, LoginForm, SchemaForm
from .models import SchemaModel, DatasetModel, ColumnModel
from .tasks import create_dataset_task


class SchemaListView(ListView):
    model = SchemaModel


class SchemaCreateView(LoginRequiredMixin, CreateView):
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

        return super().form_valid(parent_form)

    def get_success_url(self):
        return reverse("schema_list")


@login_required
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


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = SchemaModel
    template_name = 'fake_csv/schema_delete.html'

    def get_success_url(self):
        return reverse("schema_list")


@login_required
def detail_schema(request, pk):
    if request.method == 'GET':
        # do fix double request
        parent_obj = get_object_or_404(SchemaModel, pk=pk)
        parent_id = parent_obj.id
        parent_form = SchemaForm(instance=parent_obj)
        formset = AddColumnFormSet(instance=parent_obj)
        datasets = DatasetModel.objects.filter(schema_id=parent_id)
        formset.extra = 0
        context = {
            'form': parent_form,
            'columns': formset,
            'datasets': datasets,
        }
        return render(request, 'fake_csv/schema_detail.html', context=context)
    else:
        return reverse("schema_list")


def status_dataset(request):
    """Get dataset status."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    pk = request.path.split('/ajax/')[1]
    if is_ajax:
        if request.method == "GET":
            dataset = DatasetModel.objects.get(id=pk)
            return JsonResponse({'context': dataset.status})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


@login_required
def create_dataset(request, pk):
    """Create dataset."""
    now = datetime.now().strftime("%d%m%Y_%H%M%S_%f")[:-3]
    parent_obj = get_object_or_404(SchemaModel, pk=pk)
    parent_id = parent_obj.id
    columns = ColumnModel.objects.filter(schema_id=parent_id)

    num_rows = request.POST['rows']
    data_dict = {column.name: [column.type, column.range_from, column.range_to] for column in columns}
    file_name = f'{parent_obj.name}_{now}.csv'
    column_separator = parent_obj.column_separator
    string_character = parent_obj.string_character

    # set status -- Wait
    data = DatasetModel(schema_id=parent_id)
    data.status = 'Wait'
    data.save()
    pk_dataset = data.id

    create_dataset_task(
        pk_dataset,
        num_rows,
        data_dict,
        file_name,
        column_separator,
        string_character)

    return redirect('schema_detail', pk=pk)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('schema_list')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login! Try again!')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
