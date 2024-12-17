from cs2_obs_stats import app, db, Player

with app.app_context():
    players = Player.query.all()
    for player in players:
        if player.kills is None:
            player.kills = 0
        if player.deaths is None:
            player.deaths = 0
        if player.wins is None:
            player.wins = 0
        if player.losses is None:
            player.losses = 0
        if player.mvps is None:
            player.mvps = 0
        if player.assists is None:
            player.assists = 0
        if player.score is None:
            player.score = 0
        if player.match_kills is None:
            player.match_kills = 0
        if player.match_deaths is None:
            player.match_deaths = 0
        if player.match_mvps is None:
            player.match_mvps = 0
        if player.match_assists is None:
            player.match_assists = 0
        if player.match_score is None:
            player.match_score = 0
        if player.is_processed is None:
            player.is_processed = False
        if player.last_activity is None:
            player.last_activity = "menu"
        if player.wins_match is None:
            player.wins_match = 0
        if player.losses_match is None:
            player.losses_match = 0
    db.session.commit()
