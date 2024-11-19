from django.db import migrations

def create_initial_games(apps, schema_editor):
    BoardGame = apps.get_model('games', 'BoardGame')
    initial_games = [
        BoardGame(title="Chess", description="A classic strategy game", genre="Strategy", player_count=2),
        BoardGame(title="Monopoly", description="A real estate trading game", genre="Economic", player_count=4),
        BoardGame(title="Scrabble", description="A word game for vocabulary building", genre="Word", player_count=4),
        BoardGame(title="Clue", description="A mystery deduction game", genre="Mystery", player_count=6),
    ]
    BoardGame.objects.bulk_create(initial_games)

class Migration(migrations.Migration):
    dependencies = [
        ('games', '0003_alter_boardgame_borrowed_by'),  # Adjust this based on your latest migration file name
    ]

    operations = [
        migrations.RunPython(create_initial_games),
    ]
