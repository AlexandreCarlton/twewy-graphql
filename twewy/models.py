from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

from twewy.database import Base

class ReprMixin:
    '''Provides a convenient __repr__ method to inspect rows returned by a
    query.'''

    def __repr__(self):
        columns = [column.name for column in self.__table__.columns]
        attributes = ", ".join(f"{column}={self.__dict__[column]}"
                               for column in columns)
        return f"{self.__tablename__.title().replace('_', '')}({attributes})"


class Pin(Base, ReprMixin):

    __tablename__ = 'pin'

    number = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    brand = Column(String) # TODO: Make this an Enum
    # TODO: maybe have a evolution table (type -> number)
    bpp_yields_number = Column(Integer, ForeignKey('pin.number'), nullable=True)
    mpp_yields_number = Column(Integer, ForeignKey('pin.number'), nullable=True)
    sdpp_yields_number = Column(Integer, ForeignKey('pin.number'), nullable=True)

    # Hello!
    bpp_yields = relationship("Pin", remote_side=[number], foreign_keys=[bpp_yields_number])
    mpp_yields = relationship("Pin", remote_side=[number], foreign_keys=[mpp_yields_number])
    sdpp_yields = relationship("Pin", remote_side=[number], foreign_keys=[sdpp_yields_number])


class Noise(Base, ReprMixin):

    __tablename__ = 'noise'

    number = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    hp = Column(Integer)
    attack = Column(Integer)
    pp = Column(Integer)
    exp = Column(Integer)

    # TODO: Maybe have a drops table ?
    # Want something like:
    # noise {
    #   drops {
    #     hard = ...
    # But we may want to query all difficulties.

