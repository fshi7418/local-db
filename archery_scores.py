from sqlalchemy import Column, Integer, Date, Float, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Rounds(Base):
    __tablename__ = 'rounds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    location = Column(String, nullable=False)
    distance_m = Column(Float, nullable=False)
    target_size_cm = Column(Float, nullable=False)
    bow = Column(String, nullable=False)
    draw_weight_lb = Column(Float, nullable=False)
    bow_length_in = Column(Float)
    arrow_stiffness_gr = Column(Integer)
    sight = Column(Boolean, nullable=False)
    clicker = Column(Boolean, nullable=False)
    stabliser = Column(Boolean, nullable=False)
    total_score = Column(Integer, nullable=False)
    num_x = Column(Integer, nullable=False)
    num_10 = Column(Integer, nullable=False)
    num_9 = Column(Integer, nullable=False)
    self_mental_score = Column(Integer)
    hunger = Column(Boolean)
    days_since_last_practice = Column(Integer)
    remark = Column(String)
    last_updated = Column(TIMESTAMP(timezone=True), default=func.now())
