from django.contrib import admin
from django.urls import path, include
from games import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.game_list, name='game_list'),
    path('borrow/<int:game_id>/', views.borrow_game, name='borrow_game'),
    path('return/<int:game_id>/', views.return_game, name='return_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout routes
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('add/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('review/<int:game_id>/', views.add_review, name='add_review'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),

]
