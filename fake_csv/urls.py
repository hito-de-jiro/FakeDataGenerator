from django.urls import path

from .views import login, data_schemas, new_schema, data_sets, draft_column


urlpatterns = [
    path('login/', login),  # http://127.0.0.1:8000/login/
    path('dataschemas/', data_schemas),  # http://127.0.0.1:8000/dataschemas/
    path('newschema/', new_schema),  # http://127.0.0.1:8000/newschema/
    path('datasets/', data_sets),  # http://127.0.0.1:8000/datasets/
    path('draftcolumn/', draft_column),  # http://127.0.0.1:8000/draftcolumn/
]