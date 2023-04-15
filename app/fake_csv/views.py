from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from .fake_app.generator_fake_data import run_process
from .forms import AddColumnFormSet, LoginForm, SchemaForm
from .models import SchemaModel, DatasetModel


class SchemaListView(ListView):
    model = SchemaModel


# @login_required
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

        return super().form_valid(parent_form)

    def get_success_url(self):
        return reverse("schema_list")


# @login_required
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


# @login_required
class SchemaDeleteView(DeleteView):
    model = SchemaModel
    template_name = 'fake_csv/schema_delete.html'

    def get_success_url(self):
        return reverse("schema_list")


# @login_required
def detail_schema(request, pk):  # TODO: Allow only GET
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


# @login_required
def create_dataset(request, pk):
    parent_obj = get_object_or_404(SchemaModel, pk=pk)
    parent_id = parent_obj.id
    # pdb.set_trace()

    num_rows = request.POST['rows']
    range_from = 0
    range_to = 100
    data_types = ['fullname']
    file_name = 'data.csv'

    filepath = run_process(num_rows, data_types, file_name, range_from, range_to)
    if request.method == "POST":
        data = DatasetModel(schema_id=parent_id)
        data.file = request.POST.get(filepath)
        data.save()

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
                    return HttpResponse('Authenticated successfully!')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login! Try again!')
    else:
        form = LoginForm()

    return render(request, 'fake_csv/login.html', {'form': form})
