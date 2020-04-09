import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class AdditivesTypes(SqlAlchemyBase):
    __tablename__ = 'additives types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
