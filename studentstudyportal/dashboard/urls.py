from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('homework',views.homework, name='homework'),
    path('update_homework/<int:pk>',views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>',views.delete_homework, name="delete-homework"),
    path('youtube',views.youtube,name="youtube"),
    path('books',views.books,name="books"),
    path('dictionary',views.dictionary,name="dictionary"),
    path('wiki',views.wiki,name="wiki"),
    
]