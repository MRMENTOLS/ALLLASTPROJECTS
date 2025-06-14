import os
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

DATA_FILE = "data.json"
SCHEDULE_PHOTO_PATH = os.path.join("data", "schedule_photo.jpg")
SCHEDULE_FILE_PATH = os.path.join("data", "schedule_file.pdf")


# Загружаем данные из JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        save_data({"schedule": {}, "announcements": [], "admins": []})
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Сохраняем данные в JSON
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Инициализируем данные
data = load_data()

DEFAULT_SCHEDULE = data.get("schedule", {})
ANNOUNCEMENTS = data.get("announcements", [])
ADMINS = data.get("admins", [MAIN_ADMIN_ID])