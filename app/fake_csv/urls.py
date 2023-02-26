from django.urls import path

from .views import (
    login,
    SchemaListView,
    SchemaCreateView
)

urlpatterns = [
    path('schemas/', SchemaListView.as_view(template_name="fake_scv/schemamodel_list.html"), name='schema_list'),
    path('add/', SchemaCreateView.as_view(template_name="fake_csv/schema_form.html"), name='add_schemas'),
    path('', login, name='login/'),  # http://127.0.0.1:8000/login/

]

