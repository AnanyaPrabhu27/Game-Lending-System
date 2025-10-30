from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('', views.home, name='home'),
    path('<int:game_id>/', views.game_detail, name='game_detail'),
    path('add/', views.add_game, name='add_game'),
    path('<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('<int:game_id>/delete/', views.delete_game, name='delete_game'),
    path('<int:game_id>/review/', views.add_review, name='add_review'),
    path('profile/', views.profile, name='profile'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),

]
