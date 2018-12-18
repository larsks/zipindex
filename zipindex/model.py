import datetime
import pony.orm as orm

db = orm.Database()


class Directory(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    path = orm.Required(str, unique=True)
    archives = orm.Set('Archive')


class Archive(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    directory = orm.Required(Directory, column='directory_id')
    path = orm.Required(str, unique=True)
    path_lower = orm.Required(str)
    files = orm.Set('File')
    last_update = orm.Required(datetime.datetime,
                               sql_default='current_timestamp')


class File(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    archive = orm.Required(Archive, column='archive_id')
    path = orm.Required(str)
    path_lower = orm.Required(str)
    orm.composite_key(archive, path)


def bind(path=':memory:', debug=False):
    db.bind(provider='sqlite', filename=path, create_db=True)
    db.generate_mapping(create_tables=True)

    if debug:
        orm.set_sql_debug(True)
