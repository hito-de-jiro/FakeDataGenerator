from django.urls import path

from .tasks import create_dataset
from .views import (
    user_login,
    SchemaListView,
    SchemaCreateView,
    SchemaDeleteView,
    update_schema,
    detail_schema,
)

urlpatterns = [
    path('schemas/', SchemaListView.as_view(), name='schema_list'),  # http://127.0.0.1:8000/schemas/
    path('add/', SchemaCreateView.as_view(), name='add_schemas'),  # http://127.0.0.1:8000/add/
    path('schemas/<int:pk>/update', update_schema, name='schema_edit'),
    path('schemas/<int:pk>/delete', SchemaDeleteView.as_view(), name='schema_delete'),
    path('schemas/<int:pk>/detail', detail_schema, name='schema_detail'),
    path('schemas/<int:pk>/dataset', create_dataset, name='create_dataset'),
    path('', user_login, name='login'),  # http://127.0.0.1:8000/
]
