from modules.constants import ADDITIVE_TYPES_TITLES
from . import additives_types
from app.data import db_session


def set_types_table():
    session = db_session.create_session()
    # Очистим таблицу и заполним её заново
    session.query(additives_types.AdditivesTypes).delete()
    for title in ADDITIVE_TYPES_TITLES:
        ad_type = additives_types.AdditivesTypes()
        ad_type.title = title
        session.add(ad_type)
    session.commit()
