# CS2 Stats Tracker
**CS2 Stats Tracker** is a Flask-based web application for tracking player statistics in Counter-Strike 2. It displays real-time match statistics and overall player statistics. The application integrates with CS2's Game State Integration (GSI) system to fetch live game data.

## Features

- Real-time match statistics, including kills, deaths, MVPs, and match score.
- Cumulative overall statistics for kills, deaths, wins, losses, and MVPs.
- Dynamic switching between match and overall statistics based on the player's game activity.
- Integration with CS2 using GSI for live updates.

## Installation

1. Clone the repository:
```
git clone https://github.com/your_username/cs2-stats-tracker.git
cd cs2-stats-tracker
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Configure CS2 for Game State Integration:

- Copy the `obs_integration.cfg` file to the following location:
```
steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\gamestate_integration\
```
4. Set your player name in `cs2_obs_stats.py`:
```
PLAYER_NAME = "Your_Nick_Steam"
```
5. Initialize the database:
```
python fix_nulls.py
```
6. Run the application:
```
python cs2_obs_stats.py
```
7. Open the stats page in your browser at:
```
http://localhost:5000/stats
```
## File Descriptions 
- `cs2_obs_stats.py`: Main server file for handling GSI data and rendering statistics.

- `fix_nulls.py`: Initializes the database and ensures all fields have default values.

- `templates/stats.html`: Displays player statistics in a browser-friendly format.

- `obs_integration.cfg`: Configuration file for integrating with CS2's GSI system.

## Requirements
See `requirements.txt` for dependencies. This project uses Python 3.10.10.

# CS2 Stats Tracker

**CS2 Stats Tracker** — это веб-приложение на Flask для отслеживания статистики игрока в Counter-Strike 2. Оно отображает статистику матча в реальном времени и общую статистику игрока. Приложение интегрируется с системой Game State Integration (GSI) CS2 для получения данных о матче.

## Возможности
- Статистика матча в реальном времени, включая убийства, смерти, MVP и очки матча.
- Общая статистика игрока, включая убийства, смерти, победы, поражения и MVP.
- Динамическое переключение между матчевой и общей статистикой в зависимости от активности игрока.
- Интеграция с CS2 через GSI для обновлений в реальном времени.

## Установка
1. Клонируйте репозиторий:
```
git clone https://github.com/your_username/cs2-stats-tracker.git
cd cs2-stats-tracker
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
3. Настройте GSI для CS2:

- Скопируйте файл `obs_integration.cfg` в директорию:
```
steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\gamestate_integration\
```
4. Укажите имя игрока в `cs2_obs_stats.py`:
```
PLAYER_NAME = "Ваше_Ник_Steam"
```
5. Инициализируйте базу данных:
```
python fix_nulls.py
```
6. Запустите приложение:
```
python cs2_obs_stats.py
```
7. Откройте статистику в браузере по адресу:
```
http://localhost:5000/stats
```
## Описание файлов
- `cs2_obs_stats.py`: Основной сервер для обработки данных GSI и отображения статистики.
- `fix_nulls.py`: Инициализирует базу данных и устанавливает значения по умолчанию.
- `templates/stats.html`: Отображает статистику игрока в браузере.
- `obs_integration.cfg`: Конфигурационный файл для интеграции с GSI CS2.
## Зависимости
См. requirements.txt для списка зависимостей. Этот проект использует Python 3.10.10.
