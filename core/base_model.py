from core.dbconnector import BaseDB, ISALITE_MYSQL
from core.dbconnector.models import Model

from config import (
    DB_CHARSET,
    DB_DATABASE,
    DB_PASSWORD,
    DB_USER,
    DB_DEBUG,
    DB_HOST,
    DB_PORT
)


# Mysql Table Object Model
class BaseModel(Model):
    def __init__(self, table):
        super().__init__(table, db_conn=BaseDB(ISALITE_MYSQL).init(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
            charset=DB_CHARSET,
            debug=DB_DEBUG
        ))
