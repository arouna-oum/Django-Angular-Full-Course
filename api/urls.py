from django.urls import path, include
from . import views

urlpatterns = [
    path('rtoken/', views.TokenRefreshView.as_view()),
    path('user/login/', views.LoginUserView.as_view()),
    path('user/', views.CreateUser.as_view(), name="user"),
    path('notes/', views.NoteListCreate.as_view(), name="note_list"),
    path('notes_all/', views.NoteList.as_view(), name="note_list_all"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(),  name="delete_note"),
    path("home/", views.home),
    path("logout/", views.logout_view)
]
