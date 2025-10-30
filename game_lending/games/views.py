from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import BoardGame, Review
from .forms import BoardGameForm, ReviewForm, ProfileForm

# ---------- Pages ----------
from django.contrib.auth import logout
from django.shortcuts import redirect

def safe_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')   # ✅ after logout, go to login page
    # if GET or anything else
    return redirect('game_list') 


def home(request):
    return render(request, 'games/home.html')

@login_required
def game_list(request):
    available_games = BoardGame.objects.filter(is_available=True)
    borrowed_games = BoardGame.objects.filter(is_available=False)
    return render(request, 'games/game_list.html', {
        'available_games': available_games,
        'borrowed_games': borrowed_games,
    })


# ---------- Auth ----------

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('game_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ---------- Game Actions ----------

@login_required
def add_game(request):
    if request.method == "POST":
        form = BoardGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.is_available = True
            game.save()
            messages.success(request, f"{game.title} added successfully!")
            return redirect('game_list')
    else:
        form = BoardGameForm()
    return render(request, 'games/add_game.html', {'form': form})


@login_required
def edit_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if request.method == 'POST':
        form = BoardGameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, f"{game.title} updated successfully!")
            return redirect('game_list')
    else:
        form = BoardGameForm(instance=game)
    return render(request, 'games/edit_game.html', {'form': form, 'game': game})


@login_required
def delete_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if request.method == 'POST':
        game.delete()
        messages.success(request, "Game deleted successfully.")
        return redirect('game_list')
    return redirect('game_list')


@login_required
def borrow_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if request.user.borrowed_games.count() >= 3:
        messages.error(request, "You cannot borrow more than 3 games.")
    elif game.is_available:
        game.borrowed_by = request.user
        game.borrowed_date = timezone.now()
        game.due_date = game.borrowed_date + timedelta(days=7)
        game.is_available = False
        game.save()
        messages.success(request, f"You have borrowed {game.title}.")
    else:
        messages.error(request, f"{game.title} is already borrowed.")
    return redirect('game_list')


@login_required
def return_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if game.borrowed_by == request.user:
        game.borrowed_by = None
        game.is_available = True
        game.borrowed_date = None
        game.due_date = None
        game.save()
        messages.success(request, f"You returned {game.title}.")
    else:
        messages.error(request, "You can only return games you borrowed.")
    return redirect('game_list')


@login_required
def game_detail(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    reviews = game.reviews.all()
    return render(request, 'games/game_detail.html', {'game': game, 'reviews': reviews})


@login_required
def add_review(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully.")
            return redirect('game_detail', game_id=game.id)
    else:
        form = ReviewForm()
    return render(request, 'games/add_review.html', {'form': form, 'game': game})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('game_list')
    else:
        form = ProfileForm(instance=user)
    return render(request, 'games/profile.html', {'form': form})
