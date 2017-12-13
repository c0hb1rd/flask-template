from core.dbconnector import BaseDB
from core.dbconnector.models import Model

from config import (
    DB_CHARSET,
    DB_DATABASE,
    DB_PASSWORD,
    DB_USER,
    DB_DEBUG
)


# Mysql Table Object Model
class BaseModel(Model):
    def __init__(self, table, field):
        super().__init__(table, field, db_conn=BaseDB(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            charset=DB_CHARSET,
            debug=DB_DEBUG
        ))
