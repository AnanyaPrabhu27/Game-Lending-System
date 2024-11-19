from django.shortcuts import render, get_object_or_404, redirect
from .models import BoardGame, Review
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .forms import BoardGameForm
from django.http import HttpResponseForbidden
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from .forms import ProfileForm


def game_list(request):
    # Fetch borrowed and available games
    borrowed_games = BoardGame.objects.filter(is_available=False)
    available_games = BoardGame.objects.filter(is_available=True)

    context = {
        'borrowed_games': borrowed_games,
        'available_games': available_games,
    }
    return render(request, 'game_list.html', context)

@login_required
def borrow_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if game.is_available():
        # Ensure the user has not borrowed more than 3 games
        if request.user.borrowed_games.count() >= 3:
            messages.error(request, "You cannot borrow more than 3 games at a time.")
            return redirect('game_list')
        
        # Set the game as borrowed by the current user
        game.borrowed_by = request.user
        game.borrow_date = timezone.now()
        game.save()
        messages.success(request, f"You have borrowed {game.title}.")
    else:
        messages.error(request, f"{game.title} is already borrowed by someone else.")
    return redirect('game_list')

@login_required
def return_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    if game.borrowed_by == request.user:
        game.borrowed_by = None
        game.borrow_date = None
        game.save()
        messages.success(request, f"You have returned {game.title}.")
    else:
        messages.error(request, "You can only return games you have borrowed.")
    return redirect('game_list')


@login_required
def edit_game(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)

    # Ensure that only superusers can edit
    if not request.user.is_superuser:
        return redirect('game_list')  # Redirect to the game list page if not superuser

    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = GameForm(instance=game)

    return render(request, 'games/game_edit.html', {'form': form, 'game': game})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            # Log in the user automatically after signup
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')  # Redirect superusers to admin panel
            else:
                return redirect('game_list')  # Redirect regular users to the game list
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def game_list(request):
    # Fetching available and borrowed games separately
    available_games = BoardGame.objects.filter(is_available=True)
    borrowed_games = BoardGame.objects.filter(is_available=False)

    context = {
        'available_games': available_games,
        'borrowed_games': borrowed_games,
    }
    return render(request, 'games/game_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_game(request):
    if request.method == "POST":
        form = BoardGameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.is_available = True  # Set the game as available
            game.save()
            return redirect('game_list')  # Redirect to game list page
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
            return redirect('game_list')
    else:
        form = BoardGameForm(instance=game)
    return render(request, 'games/edit_game.html', {'form': form})

@login_required
def add_review(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    
    # Check if the user has borrowed the game
    if game.borrowed_by != request.user:
        messages.error(request, "You can only review games you have borrowed.")
        return redirect('game_list')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('game_detail', game_id=game.id)
    else:
        form = ReviewForm()
    
    return render(request, 'games/add_review.html', {'form': form, 'game': game})


@login_required
def game_detail(request, game_id):
    game = get_object_or_404(BoardGame, id=game_id)
    # Retrieve the reviews for the game, if any
    reviews = game.reviews.all()
    
    return render(request, 'games/game_detail.html', {
        'game': game,
        'reviews': reviews,
    })

@login_required
def borrow_game(request, game_id):
    game = BoardGame.objects.get(id=game_id)
    if game.is_available:
        game.borrow(request.user)
    return redirect('game_list')

@login_required
def return_game(request, game_id):
    game = BoardGame.objects.get(id=game_id)
    if game.borrowed_by == request.user:
        game.return_game()
    return redirect('game_list')

def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser)
def delete_game(request, pk):
    game = get_object_or_404(BoardGame, pk=pk)
    game.delete()
    return redirect('game_list')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('game_list')  # Redirect to the game list after saving
    else:
        form = ProfileForm(instance=user)
    return render(request, 'games/profile.html', {'form': form})

@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Ensure that the user can only edit their own review
    if review.user != request.user:
        return redirect('game_list')

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('game_detail', game_id=review.game.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'games/update_review.html', {'form': form, 'review': review})