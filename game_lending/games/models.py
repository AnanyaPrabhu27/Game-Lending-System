from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class BoardGame(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    player_count = models.IntegerField()
    borrowed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowed_games')
    borrowed_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)  # Indicates if the game is available for borrowing

    def __str__(self):
        return self.title

    def borrow(self, user):
        """
        Borrow the game if it's available. Updates the borrowed_by, borrowed_date, due_date, and is_available fields.
        """
        if self.is_available:  # Ensure the game is available
            self.is_available = False
            self.borrowed_by = user
            self.borrowed_date = timezone.now().date()
            self.due_date = self.borrowed_date + timedelta(days=7)  # Set a 7-day borrowing period
            self.save()

    def return_game(self):
        """
        Return the game. Clears the borrowing details and marks it as available.
        """
        self.is_available = True
        self.borrowed_by = None
        self.borrowed_date = None
        self.due_date = None
        self.return_date = timezone.now()  # Log the return time
        self.save()


class Review(models.Model):
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.game.title} by {self.user.username}"