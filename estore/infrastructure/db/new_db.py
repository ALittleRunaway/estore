from sqlalchemy import create_engine
from estore.config.config import DataBaseConfig


def new_db(db_cfg: DataBaseConfig):
    connect_string = f'mysql+pymysql://{db_cfg.username}:{db_cfg.password}@{db_cfg.host}/{db_cfg.db_name}'
    engine = create_engine(connect_string, echo=False)
    conn = engine.connect()
    return conn
