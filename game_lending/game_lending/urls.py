from django.contrib import admin
from django.urls import path, include
from games import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('games.urls')), 
    path('', views.game_list, name='game_list'),
    path('borrow/<int:game_id>/', views.borrow_game, name='borrow_game'),
    path('return/<int:game_id>/', views.return_game, name='return_game'),
    path('edit_game/<int:game_id>/', views.edit_game, name='edit_game'),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout routes
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('add_game/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('review/<int:game_id>/', views.add_review, name='add_review'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('delete_game/<int:pk>/', views.delete_game, name='delete_game'),
    path('profile/', views.profile, name='profile'),
    path('review/<int:review_id>/edit/', views.update_review, name='edit_review'),

]
