from django.urls import path

from .views import (
    user_login,
    SchemaListView,
    SchemaCreateView, SchemaUpdateView, SchemaDetailView
)

urlpatterns = [
    path('schemas/', SchemaListView.as_view(template_name="fake_scv/schemamodel_list.html"),
         name='schema_list'),
    path('add/', SchemaCreateView.as_view(template_name="fake_csv/schema_form.html"),
         name='add_schemas'),
    path('<pk>/update', SchemaUpdateView.as_view(), name='edit'),
    path('schemas/<int:pk>/', SchemaDetailView.as_view(), name='data_sets'),
    path('', user_login, name='login/'),  # http://127.0.0.1:8000/login/

]

