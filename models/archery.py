from sqlalchemy import Column, Integer, Float, String, Boolean, Date, Text, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from models import Base


class Rounds(Base):
    __tablename__ = 'archery_round'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, index=True)
    archery_range_id = Column(Integer, ForeignKey('archery_range.id'), nullable=True)
    distance_m = Column(Float, nullable=False)
    archery_target_id = Column(Integer, ForeignKey('archery_target.id'), nullable=True)
    archery_scoring_rule_id = Column(Integer, ForeignKey('archery_scoring_rule.id'), nullable=True)
    sight = Column(Boolean, nullable=False)
    clicker = Column(Boolean, nullable=False)
    stabilisation = Column(Boolean, nullable=False)
    archery_riser_id = Column(Integer, ForeignKey('archery_riser.id'), nullable=True)
    archery_limb_id = Column(Integer, ForeignKey('archery_limb.id'), nullable=True)
    archery_sight_id = Column(Integer, ForeignKey('archery_sight.id'), nullable=True)
    draw_weight_lb = Column(Float, nullable=True)
    archery_arrow_id = Column(Integer, ForeignKey('archery_arrow.id'), nullable=True)
    archery_arrow_rest_id = Column(Integer, ForeignKey('archery_arrow_rest.id'), nullable=True)
    total_score = Column(Integer, nullable=False)
    num_x = Column(Integer, nullable=False)
    num_10 = Column(Integer, nullable=False)
    num_9 = Column(Integer, nullable=False)
    stdev_ends = Column(Float, nullable=True)
    stdev_shots = Column(Float, nullable=True)
    avg_shots = Column(Float, nullable=True)
    num_ends = Column(Integer, nullable=False)
    num_shots = Column(Integer, nullable=False)
    condition_mental = Column(Integer, nullable=True)
    condition_env = Column(Integer, nullable=True)
    hunger = Column(Boolean, nullable=True)
    days_since_last_practice = Column(Integer, nullable=True)
    start_time = Column(String(4), nullable=True)
    end_time = Column(String(4), nullable=True)
    remark = Column(String)
    variable_distance = Column(Boolean, nullable=True)
    known_distance = Column(Boolean, nullable=True)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())

    ends = relationship('Ends', back_populates='archery_round', cascade='all, delete-orphan', lazy='joined')


class Ends(Base):
    __tablename__ = 'archery_end'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_round_id = Column(
        Integer, ForeignKey('archery_round.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False,
        index=True
    )
    end = Column(Integer, nullable=False)
    score_total = Column(Integer, nullable=False)
    num_shots = Column(Integer, nullable=False)
    shots_ordered = Column(Boolean, nullable=False)

    archery_round = relationship(Rounds, foreign_keys=archery_round_id, back_populates='ends', cascade='all')
    archery_shot = relationship('Shots', back_populates='archery_end', cascade='all, delete-orphan', lazy='joined')


class Shots(Base):
    __tablename__ = 'archery_shot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_end_id = Column(
        Integer, ForeignKey('archery_end.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    shot = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    is_x = Column(Boolean)

    archery_end = relationship(Ends, foreign_keys=archery_end_id, back_populates='archery_shot', cascade='all')


class ArcheryArrow(Base):
    __tablename__ = 'archery_arrow'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_manufacturer_id = Column(Integer, ForeignKey('archery_manufacturer.id'), nullable=True)
    name = Column(String, nullable=False)
    fletching = Column(String)
    size_mm = Column(Float)
    spine = Column(Integer)
    shaft_length_in = Column(Float)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryRiser(Base):
    __tablename__ = 'archery_riser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_manufacturer_id = Column(Integer, ForeignKey('archery_manufacturer.id'), nullable=True)
    name = Column(String, nullable=False)
    length_in = Column(Float)
    rh_lh = Column(String(2))
    archery_bow_type_id = Column(Integer, ForeignKey('archery_bow_type.id'), nullable=True)
    letoff_pct = Column(Float)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryLimb(Base):
    __tablename__ = 'archery_limb'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_manufacturer_id = Column(Integer, ForeignKey('archery_manufacturer.id'), nullable=True)
    name = Column(String, nullable=False)
    total_length_in = Column(Float)
    draw_weight_lb_min = Column(Float)
    draw_weight_lb_max = Column(Float)
    archery_bow_type_id = Column(Integer, ForeignKey('archery_bow_type.id'), nullable=True)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcherySight(Base):
    __tablename__ = 'archery_sight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_manufacturer_id = Column(Integer, ForeignKey('archery_manufacturer.id'), nullable=True)
    name = Column(String, nullable=False)
    magnification = Column(Integer)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryManufacturer(Base):
    __tablename__ = 'archery_manufacturer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryBowType(Base):
    __tablename__ = 'archery_bow_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryTarget(Base):
    __tablename__ = 'archery_target'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    minimum_score = Column(Integer, nullable=False)
    full_size_cm = Column(Float)
    actual_size_cm = Column(Float)
    cm_x = Column(Float)
    cm_ten = Column(Float)
    cm_nine = Column(Float)
    cm_eight = Column(Float)
    cm_seven = Column(Float)
    cm_six = Column(Float)
    cm_five = Column(Float)
    cm_four = Column(Float)
    cm_three = Column(Float)
    cm_two = Column(Float)
    cm_one = Column(Float)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryRange(Base):
    __tablename__ = 'archery_range'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address_street = Column(String)
    address_city = Column(String)
    address_province = Column(String)
    country_iso = Column(String(2))
    outdoor = Column(Boolean)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryScoringRule(Base):
    __tablename__ = 'archery_scoring_rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class ArcheryArrowRest(Base):
    __tablename__ = 'archery_arrow_rest'
    id = Column(Integer, primary_key=True, autoincrement=True)
    archery_manufacturer_id = Column(Integer, ForeignKey('archery_manufacturer.id'), nullable=True)
    name = Column(String)
    description = Column(Text)
    arrow_rest_type = Column(String)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())
