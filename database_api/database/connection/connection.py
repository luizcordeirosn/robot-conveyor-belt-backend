from dotenv import dotenv_values, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

config = dotenv_values(find_dotenv())

engine = create_engine(
    f"mysql://{config.get('MYSQL_ROOT_USER')}:{config.get('MYSQL_ROOT_PASSWORD')}@{config.get('MYSQL_HOST')}:{config.get('MYSQL_PORT')}/{config.get('MYSQL_DATABASE')}",
    echo=True,
)
# engine = create_engine("mysql://root:root123@127.0.0.1:3306/database_api_db")


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Session:
    return SessionLocal()
