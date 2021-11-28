import datetime

from sqlalchemy import Column, Integer, String, JSON, DateTime, PrimaryKeyConstraint
from sqlalchemy.sql import func

from .base import Base


class Weather(Base):

    __dict_export_exclude_columns__ = ["requested_at", "requested_date"]

    __tablename__ = "weathers"

    id = Column(Integer)
    base = Column(String, nullable=True)
    cod = Column(String, nullable=True)
    coord = Column(JSON, nullable=True)
    dt = Column(Integer, nullable=True)
    main = Column(JSON, nullable=True)
    clouds = Column(JSON, nullable=True)
    wind = Column(JSON, nullable=True)
    rain = Column(JSON, nullable=True)
    snow = Column(JSON, nullable=True)
    name = Column(String, nullable=True)
    sys = Column(JSON, nullable=True)
    timezone = Column(Integer, nullable=True)
    visibility = Column(Integer, nullable=True)
    weather = Column(JSON, nullable=True)
    wind = Column(JSON, nullable=True)
    requested_date = Column(DateTime)
    requested_at = Column(DateTime, default=func.now())

    __table_args__ = (PrimaryKeyConstraint(id, requested_date), {})

    def as_dict(self) -> dict:
        return {
            x.name: getattr(self, x.name)
            for x in self.__table__.columns
            if x.name not in self.__dict_export_exclude_columns__
        }
