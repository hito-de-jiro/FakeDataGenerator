from django.urls import path

from .views import (
    login,
    # data_schemas, new_schema, data_sets,
    SchemaListView, SchemaCreateView, SchemaUpdateView, delete_column
)

urlpatterns = [
    path('login/', login),  # http://127.0.0.1:8000/login/
    path('', SchemaListView.as_view(), name='index'),  # http://127.0.0.1:8000/login/
    # path('data_schemas/', data_schemas, name="data_schemas"),  # http://127.0.0.1:8000/data_schemas/
    # path('data_sets/', data_sets, name="data_sets"),  # http://127.0.0.1:8000/data_sets/
    # path('new_schema/', new_schema, name="new_schema"),  # http://127.0.0.1:8000/new_schema/

    path('schemas/', SchemaListView.as_view(), name='data_schemas'),
    path('new-schema/', SchemaCreateView.as_view(), name='new_schema'),
    path('update-schema/<int:pk>', SchemaUpdateView.as_view(), name='update_schema'),
    path('delete-column/<int:pk>', delete_column, name='delete_column'),
]
