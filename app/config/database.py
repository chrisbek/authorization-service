from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Session, create_engine, SQLModel

Base = declarative_base()
SQLModel.metadata = Base.metadata


class DatabaseFactory:
    @staticmethod
    def get_session(
            dialect_and_driver: str = "mysql+pymysql",
            username: str = "root",
            password: str = "root",
            host: str = "172.30.0.4",
            port: str = "3306",
            database: str = "local_authorization"
    ) -> Session:
        # dialect+driver://username:password@host:port/database
        db_url = f"{dialect_and_driver}://{username}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_url, echo=True)
        return Session(engine, expire_on_commit=False)
