from sqlalchemy import Column, Integer, String

from app.core.db import Base


class Airline(Base):
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
