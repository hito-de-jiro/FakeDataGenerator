from django.urls import path, re_path

from .views import (
    user_login,
    SchemaListView,
    SchemaCreateView,
    SchemaDeleteView,
    update_schema,
    detail_schema,
    status_dataset,
    create_dataset_ajax,
)

urlpatterns = [
    path('schemas/', SchemaListView.as_view(), name='schema_list'),
    path('add/', SchemaCreateView.as_view(), name='add_schemas'),
    path('schemas/<int:pk>/update', update_schema, name='schema_edit'),
    path('schemas/<int:pk>/delete', SchemaDeleteView.as_view(), name='schema_delete'),
    path('schemas/<int:pk>/detail', detail_schema, name='schema_detail'),
    path('schemas/<int:pk>/', create_dataset_ajax, name='create_dataset_ajax'),
    re_path(r'schemas/[\d]*/ajax/[\d]*', status_dataset, name='ajax_detail'),
    path('', user_login, name='login'),
]
