from django.shortcuts import render


def login(request):
    # Start page
    return render(request, 'fake_csv/login.html')


def new_schema(request):
    return render(request, 'fake_csv/new_schema.html')


def data_schemas(request):
    return render(request, 'fake_csv/data_schemas.html')


def data_sets(request):
    return render(request, 'fake_csv/data_sets.html')


def draft_column(request):
    return render(request, 'fake_csv/_new_column.html')
