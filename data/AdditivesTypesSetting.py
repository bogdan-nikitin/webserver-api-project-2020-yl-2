from . import AdditivesTypes

titles = ['photo', 'video', 'audio', 'sticker', 'file']


def set_types_table(session):
    for title in titles:
        ad_type = AdditivesTypes.AdditivesTypes()
        ad_type.title = title
        session.add(ad_type)
