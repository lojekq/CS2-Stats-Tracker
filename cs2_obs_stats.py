import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import logging
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cs2_stats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# # Настройка логирования
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='[%(asctime)s] %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("cs2_obs_stats.log", encoding='utf-8'),
#         logging.StreamHandler(sys.stdout)
#     ]
# )

# Инициализация SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Модель Player с общей и временной статистикой и флагом обработки
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    kills = db.Column(db.Integer, default=0, nullable=False)
    deaths = db.Column(db.Integer, default=0, nullable=False)
    wins = db.Column(db.Integer, default=0, nullable=False)
    losses = db.Column(db.Integer, default=0, nullable=False)
    mvps = db.Column(db.Integer, default=0, nullable=False)
    assists = db.Column(db.Integer, default=0, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    match_kills = db.Column(db.Integer, default=0, nullable=False)
    match_deaths = db.Column(db.Integer, default=0, nullable=False)
    match_mvps = db.Column(db.Integer, default=0, nullable=False)
    match_assists = db.Column(db.Integer, default=0, nullable=False)
    match_score = db.Column(db.Integer, default=0, nullable=False)
    is_processed = db.Column(db.Boolean, default=False, nullable=False)

    # Хранение последнего состояния activity
    last_activity = db.Column(db.String(20), default="menu", nullable=False)

    def __repr__(self):
        return f'<Player {self.name}>'

    def to_dict(self):
        return {
            "kills": self.kills,
            "deaths": self.deaths,
            "wins": self.wins,
            "losses": self.losses,
            "mvps": self.mvps,
            "assists": self.assists,
            "score": self.score,
            "match_kills": self.match_kills,
            "match_deaths": self.match_deaths,
            "match_mvps": self.match_mvps,
            "match_assists": self.match_assists,
            "match_score": self.match_score,
            "wins_match": self.wins,  # Победы текущего матча
            "losses_match": self.losses,  # Поражения текущего матча
            "activity": self.last_activity,  # Используем последнее состояние
        }


# Создание таблиц
with app.app_context():
    db.create_all()

# Имя игрока
PLAYER_NAME = "YOUR_NICK_STEAM"

@app.route('/', methods=['POST'])
def receive_game_state():
    data = request.json
    if not data:
        logging.warning("Получен пустой POST-запрос.")
        return jsonify({"status": "no data"}), 400

    logging.debug(f"Получены данные GSI: {json.dumps(data, indent=2, ensure_ascii=False)}")

    try:
        player_data = data.get('player', {})
        if player_data:
            player_name_in_data = player_data.get('name', '').lower()
            activity = player_data.get('activity', 'menu')  # Извлекаем activity из данных
            if player_name_in_data == PLAYER_NAME.lower():
                match_stats = player_data.get('match_stats', {})
                player = Player.query.filter_by(name=PLAYER_NAME).first()
                if not player:
                    player = Player(name=PLAYER_NAME)
                    db.session.add(player)

                # Обновляем временную статистику
                if match_stats:
                    player.match_kills = match_stats.get('kills', 0)
                    player.match_deaths = match_stats.get('deaths', 0)
                    player.match_mvps = match_stats.get('mvps', 0)
                    player.match_assists = match_stats.get('assists', 0)
                    player.match_score = match_stats.get('score', 0)

                # Обновляем состояние activity
                player.last_activity = activity
                db.session.commit()

        map_data = data.get('map', {})
        phase = map_data.get('phase', '')

        if phase == "gameover":
            player = Player.query.filter_by(name=PLAYER_NAME).first()
            if player and not player.is_processed:
                logging.info("Игра завершена. Перенос временной статистики в общую.")
                player.kills += player.match_kills
                player.deaths += player.match_deaths
                player.mvps += player.match_mvps
                player.assists += player.match_assists
                player.score += player.match_score

                # Обработка побед и поражений
                player_team = player_data.get('team', '')
                round_info = data.get('round', {})
                winning_team = round_info.get('win_team', '')

                if player_team and winning_team:
                    if player_team == winning_team:
                        player.wins += 1
                        logging.info(f"Победа для {PLAYER_NAME}. Всего побед: {player.wins}")
                    else:
                        player.losses += 1
                        logging.info(f"Поражение для {PLAYER_NAME}. Всего поражений: {player.losses}")

                player.match_kills = 0
                player.match_deaths = 0
                player.match_mvps = 0
                player.match_assists = 0
                player.match_score = 0

                player.is_processed = True
                db.session.commit()
                logging.info(f"Обновлено: Общие убийства: {player.kills}, Общие смерти: {player.deaths}, Общие MVPs: {player.mvps}, Общие ассисты: {player.assists}, Общий счёт: {player.score}")

        if phase == "live":
            player = Player.query.filter_by(name=PLAYER_NAME).first()
            if player:
                player.is_processed = False  # Сбрасываем флаг при начале новой игры
                db.session.commit()

    except Exception as e:
        logging.error(f"Ошибка при обработке данных GSI: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success"}), 200



def update_match_result(winner_team, loser_team, data):
    player = Player.query.filter_by(name=PLAYER_NAME).first()
    if not player:
        player = Player(name=PLAYER_NAME)
        db.session.add(player)

    player_team = data.get('player', {}).get('team', '')
    if player_team not in ["T", "CT"]:
        logging.warning(f"Неизвестная команда игрока: {player_team}")
        player_team = "Unknown"

    if player_team == winner_team:
        player.wins += 1
        logging.info(f"Победа для {PLAYER_NAME}. Всего побед: {player.wins}")
    elif player_team == loser_team:
        player.losses += 1
        logging.info(f"Поражение для {PLAYER_NAME}. Всего поражений: {player.losses}")

    db.session.commit()
    socketio.emit('update_stats', player.to_dict())

@app.route('/stats', methods=['GET'])
def stats_page():
    return render_template('stats.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    player = Player.query.filter_by(name=PLAYER_NAME).first()
    if not player:
        return jsonify({
            "kills": 0,
            "deaths": 0,
            "wins": 0,
            "losses": 0,
            "mvps": 0,
            "assists": 0,
            "score": 0,
            "match_kills": 0,
            "match_deaths": 0,
            "match_mvps": 0,
            "match_assists": 0,
            "match_score": 0,
            "activity": "menu",  # По умолчанию "menu"
        })
    return jsonify(player.to_dict())

if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5000)
