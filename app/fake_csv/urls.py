from django.urls import path

from .views import (
    user_login,
    SchemaListView,
    SchemaCreateView,
    SchemaDetailView,
    SchemaDeleteView,
    update_schema
)

urlpatterns = [
    path('schemas/', SchemaListView.as_view(), name='schema_list'),  # http://127.0.0.1:8000/schemas/
    path('add/', SchemaCreateView.as_view(), name='add_schemas'),  # http://127.0.0.1:8000/add/
    path('schemas/<int:pk>/update', update_schema, name='schema_edit'),
    path('schemas/<int:pk>/delete', SchemaDeleteView.as_view(), name='schema_delete'),
    path('schemas/<int:pk>/', SchemaDetailView.as_view(), name='schema_detail'),
    path('', user_login, name='login'),  # http://127.0.0.1:8000/

]
