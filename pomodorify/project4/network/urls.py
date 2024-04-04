
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_task", views.new_task, name="new_task"),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('check_true/<int:task_id>/', views.check_true, name='check_true'),
    path('check_false/<int:task_id>/', views.check_false, name='check_false'),
    path('update_pomo_counter/<int:task_id>/', views.update_pomo_counter, name='update_pomo_counter'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
  







]
