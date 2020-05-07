from contextlib import contextmanager
from typing import Dict

from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from . import SessionFactory


def obj_as_dict(func):
    def decorator(*args, **kwargs):
        def _map(_tup):
            return {
                c.key: getattr(_tup, c.key) for c in inspect(_tup).mapper.column_attrs
            }

        obj = func(*args, **kwargs)

        if obj:
            if isinstance(obj, list):
                return [_map(tup) for tup in obj]
            else:
                return _map(obj)
        else:
            return []

    return decorator


@contextmanager
def session_commit(session: SessionFactory):
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


@obj_as_dict
def select_one(table, filter_: Dict, session: SessionFactory):
    return session.query(table).filter_by(**filter_).first()


@obj_as_dict
def select_filter(table, filter_: Dict, session: SessionFactory):
    return session.query(table).filter_by(**filter_).all()


@obj_as_dict
def select_all(table, session: SessionFactory):
    return session.query(table).all()


def delete_filter(table, filter_: Dict, session: SessionFactory):
    session.query(table).filter_by(**filter_).delete()


def delete_all(table, session: SessionFactory):
    session.query(table).delete()


def update_one(table, filter_: Dict, values: Dict, session: SessionFactory):
    result = session.query(table).filter_by(**filter_).update(values)
    return result


def insert_one(table, values: Dict, session: SessionFactory):
    result = table(**values)
    session.add(result)
    return result
