from django.urls import path, re_path
from .views import (
    person_list_view,
    person_detail_view,    
    person_create_view,
    person_update_view,
    person_delete_view,
    phone_add_view,
    email_add_view,
    phone_delete_view,
    email_delete_view,
    search_view
)

app_name = 'book'

urlpatterns = [
    path('', person_list_view),    
    path('create/', person_create_view),
    path('<int:id_person>/', person_detail_view, name='person_detail'),
    path('<int:id_person>/update/', person_update_view),
    path('<int:id_person>/delete/', person_delete_view),
    path('<int:id_person>/add-number/', phone_add_view),
    path('<int:id_person>/add-email/', email_add_view),
    path('<int:id_person>/delete-number/<int:id_phone>/', phone_delete_view),
    path('<int:id_person>/delete-email/<int:id_email>/', email_delete_view),
    re_path(r'search/', search_view, name='search_list')
]
