from django.urls import path
from .views import *

urlpatterns = [
    path('take_book/', CreateBooks.as_view()),
    path('get_book/', get_user_books)
]
