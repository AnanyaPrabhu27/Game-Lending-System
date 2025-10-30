from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from games import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 🌟 Homepage
    path('', views.home, name='home'),

    # 🎲 Game actions
    path('games/', include('games.urls')),  # Routes to games app URLs

    # 👤 Auth routes
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/reset
    path('signup/', views.signup, name='signup'),
    path('accounts/logout/', views.safe_logout, name='logout'),

    # 🕹️ Borrow / return / reviews (defined in games/views.py)
    path('borrow/<int:game_id>/', views.borrow_game, name='borrow_game'),
    path('return/<int:game_id>/', views.return_game, name='return_game'),
    path('review/<int:game_id>/', views.add_review, name='add_review'),
]
