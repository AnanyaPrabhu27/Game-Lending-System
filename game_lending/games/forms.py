from django import forms
from .models import BoardGame, Review
from django.contrib.auth.models import User

class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title', 'description', 'genre', 'player_count']  # Specify the fields to include in the form


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'placeholder': 'Write your review here...'}),

       }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class GameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title', 'description', 'genre', 'player_count']
