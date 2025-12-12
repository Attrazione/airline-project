from sqlalchemy import Column, Integer, String

from app.core.db import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    timezone = Column(String(64), nullable=True)
