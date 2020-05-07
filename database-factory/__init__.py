import logging


from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import config


logger = logging.getLogger(__name__)


class Tables:
    USER = "user"

    _base_prepared = False

    def __call__(self, table):
        if not self._base_prepared:
            Base.prepare(db_engine, reflect=True)
            self._base_prepared = True

        return Base.classes.__getattr__(table)


class Database:
    @staticmethod
    def get_engine_pool():
        db = config.DB
        driver = config.DB_DRIVER
        user = config.DB_USER
        pw = config.DB_PASSWORD
        url = config.DB_URL
        name = config.DB_NAME

        try:
            engine = create_engine(f"{db}+{driver}://{user}:{pw}@{url}/{name}")
            logger.info("DB pool engine started")
            return engine
        except Exception as e:
            logger.error(f"DB start_engine failed - {e}")


Base = automap_base()
db_engine = Database().get_engine_pool()

SessionFactory = sessionmaker(autocommit=False)
TableFactory = Tables()
