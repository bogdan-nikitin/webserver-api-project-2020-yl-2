from . import additives_types

titles = ['photo', 'video', 'audio', 'sticker', 'file']


def set_types_table(session):
    for title in titles:
        ad_type = additives_types.AdditivesTypes()
        ad_type.title = title
        session.add(ad_type)
