from django.urls import path
from .views import *

urlpatterns = [
    path('add_image/', add_image, name='add_image'),
    path('image_list/', image_list, name='image_list'),
    path('delete_image/', delete_image, name='delete_image'),
    path('add_tag/', add_tag, name='add_tag'),  # Добавьте эту строку
    path('add_tag_to_image/<int:image_id>/', add_tag_to_image, name='add_tag_to_image'),
    path('delete_tag/', delete_tag, name='delete_tag'),
    path('',index,name='index')
]
