# fake_csv/views.py
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import format
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


@login_required
def status_dataset(request):
    """Get dataset status."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    pk = request.path.split('/ajax/')[1]
    if is_ajax:
        if request.method == "GET":
            dataset = DatasetModel.objects.get(id=pk)
            return JsonResponse({
                'dataset_status': dataset.status,
            })

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


@login_required
def create_dataset_ajax(request, pk):
    """Create ajax dataset."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":
            parent_obj = get_object_or_404(SchemaModel, pk=pk)
            num_rows = request.POST['rows']

            # new dataset model
            now = datetime.now().strftime("%d%m%Y_%H%M%S")
            new_dataset = DatasetModel(schema_id=parent_obj.id, status='Wait', file=f'{parent_obj.name}_{now}.csv')
            new_dataset.save()

            # run create_dataset_task
            columns = ColumnModel.objects.filter(schema_id=parent_obj.id)
            create_dataset_task(
                pk_dataset=new_dataset.id,
                num_rows=num_rows,
                data_dict={column.name: [column.type, column.range_from, column.range_to] for column in columns},
                file_name=new_dataset.file,
                column_separator=parent_obj.column_separator,
                string_character=parent_obj.string_character
            )
            # return data in json format
            return JsonResponse({
                'dataset_id': new_dataset.id,
                'dataset_created': format(new_dataset.created, format_string=settings.DATETIME_FORMAT),
                'dataset_status': new_dataset.status,
                'dataset_file': new_dataset.file,
            })

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


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
