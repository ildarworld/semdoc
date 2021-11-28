import logging
import os
import typing
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)


engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
metadata = MetaData(bind=engine)


@as_declarative(metadata=metadata)
class Base:
    pass


Session = sessionmaker()


@contextmanager
def session(**kwargs) -> typing.ContextManager[Session]:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception as ex:
        log.exception(ex)
        new_session.rollback()
    finally:
        new_session.close()
