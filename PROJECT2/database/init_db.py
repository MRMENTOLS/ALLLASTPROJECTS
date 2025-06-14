# init_db.py

from sqlalchemy import create_engine
from models.ticket import Base, config

def init_db():
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("✅ База данных и таблицы успешно созданы!")

if __name__ == "__main__":
    init_db()