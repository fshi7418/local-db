from sqlalchemy import Column, Integer, Float, String, Boolean, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Rounds(Base):
    __tablename__ = 'rounds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    round_date = Column(Date, nullable=False, index=True)
    distance_m = Column(Integer, nullable=False, index=True)
    target_size_cm = Column(Integer, nullable=False)
    sight = Column(Boolean, nullable=False)
    clicker = Column(Boolean, nullable=False)
    stabliser = Column(Boolean, nullable=False)
    bow = Column(String, nullable=False, index=True)
    arrow_stiffness = Column(Integer)
    bow_weight_lb = Column(Integer, nullable=False, index=True)
    bow_length_in = Column(Integer, nullable=False)
    total_score = Column(Integer, nullable=False, index=True)
    num_x = Column(Integer, nullable=False)
    num_10 = Column(Integer, nullable=False)
    num_9 = Column(Integer, nullable=False)
    num_shots = Column(Integer, nullable=False)
    location = Column(String, nullable=False, index=True)
    mental_status = Column(Integer)
    conditions = Column(Integer)
    hunger = Column(Boolean)
    days_since_last_practice = Column(Integer)
    stdev_ends = Column(Float, nullable=False)
    stdev_shots = Column(Float, nullable=False)

    ends = relationship('Ends', back_populates='round', cascade='all, delete-orphan', lazy='joined')


class Ends(Base):
    __tablename__ = 'ends'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rounds_id = Column(
        Integer, ForeignKey('rounds.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, index=True
    )
    end = Column(Integer, nullable=False)
    score_total = Column(Integer, nullable=False)
    num_shots = Column(Integer, nullable=False)
    shots_ordered = Column(Boolean, nullable=False)

    round = relationship(Rounds, foreign_keys=rounds_id, back_populates='ends', cascade='all')
    shots = relationship('Shots', back_populates='end', cascade='all, delete-orphan', lazy='joined')


class Shots(Base):
    __tablename__ = 'shots'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ends_id = Column(
        Integer, ForeignKey('ends.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    shot = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    is_x = Column(Boolean)

    end = relationship(Ends, foreign_keys=ends_id, back_populates='shots', cascade='all')
