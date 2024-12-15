from sqlalchemy import Column, Integer, Float, String, Boolean, Date, func, SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from models import Base


class FirearmTrade(Base):
    __tablename__ = 'firearm_trade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_date = Column(Date, index=True)
    firearm_model_id = Column(Integer, ForeignKey('firearm_model.id'), nullable=False)
    serial_number = Column(String, nullable=False)
    firearm_dealer_id = Column(Integer, ForeignKey('firearm_dealer.id'), nullable=False)
    buy_sell = Column(String(4), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    price_currency = Column(String(3), nullable=False)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmManufacturer(Base):
    __tablename__ = 'firearm_manufacturer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country_iso = Column(String(2))
    address_street = Column(String)
    address_city = Column(String)
    address_province = Column(String)
    address_country = Column(String(2))
    postal_code = Column(String(10))
    website = Column(String)
    phone = Column(String(30))
    phone_country_code = Column(String(10))
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmModel(Base):
    __tablename__ = 'firearm_model'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firearm_manufacturer_id = Column(
        Integer, ForeignKey('firearm_manufacturer.id'), nullable=False
    )
    name = Column(String, nullable=False)
    firearm_action_id = Column(
        Integer, ForeignKey('firearm_action.id'), nullable=False
    )
    barrel_type = Column(String)
    barrel_length_in = Column(Float)
    barrel_length_cm = Column(Float)
    country_iso_origin = Column(String(2))
    weight_lb = Column(Float)
    weight_kg = Column(Float)
    rear_sight = Column(Boolean)
    front_sight = Column(Boolean)
    firearm_restriction_id = Column(Integer, ForeignKey('firearm_restriction.id'), nullable=False)
    firearm_cartridge_id1 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=False)
    capacity1 = Column(Integer)
    firearm_cartridge_id2 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    capacity2 = Column(Integer)
    firearm_cartridge_id3 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    capacity3 = Column(Integer)
    firearm_cartridge_id4 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    capacity4 = Column(Integer)
    firearm_cartridge_id5 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    capacity5 = Column(Integer)
    firearm_cartridge_id6 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    capacity6 = Column(Integer)
    firearm_cartridge_id7 = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    capacity7 = Column(Integer)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())
    datetime_valid_start = Column(TIMESTAMP(timezone=True), default=func.now())
    datetime_valid_end = Column(TIMESTAMP(timezone=True), default='2099-12-31 23:59:59')


class FirearmSight(Base):
    __tablename__ = 'firearm_sight'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(90))
    firearm_manufacturer_id = Column(
        Integer, ForeignKey('firearm_manufacturer.id'), nullable=True
    )
    name = Column(String, nullable=False)
    max_magnification = Column(Float)


class FirearmDealer(Base):
    __tablename__ = 'firearm_dealer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address_street = Column(String)
    address_city = Column(String)
    address_province = Column(String)
    address_country = Column(String(2))
    postal_code = Column(String(10))
    phone = Column(String(30))
    phone_country_code = Column(String(10))
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmCartridge(Base):
    __tablename__ = 'firearm_cartridge'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    strike_type = Column(String)
    length_in = Column(Float)
    length_mm = Column(Float)
    buckshot_type = Column(String)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmAmmunition(Base):
    __tablename__ = 'firearm_ammunition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firearm_cartridge_id = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    firearm_manufacturer_id = Column(Integer, ForeignKey('firearm_manufacturer.id'), nullable=True)
    name = Column(String, nullable=False)
    casing = Column(String)
    tip = Column(String)
    muzzle_velocity_fps = Column(Float)
    weight_grain = Column(Float)
    num_pellets = Column(Integer)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmRestriction(Base):
    __tablename__ = 'firearm_restriction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    restriction_type = Column(String, nullable=False)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())
    datetime_valid_start = Column(TIMESTAMP(timezone=True), default=func.now())
    datetime_valid_end = Column(TIMESTAMP(timezone=True), default='2099-12-31 23:59:59')


class FirearmAction(Base):
    __tablename__ = 'firearm_action'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmRange(Base):
    __tablename__ = 'firearm_range'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address_street = Column(String)
    address_city = Column(String)
    address_province = Column(String)
    address_country = Column(String(2))
    postal_code = Column(String(10))
    phone = Column(String(30))
    phone_country_code = Column(String(10))
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())


class FirearmTarget(Base):
    __tablename__ = 'firearm_target'
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


class FirearmVisit(Base):
    __tablename__ = 'firearm_visit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    visit_date = Column(Date, index=True, nullable=False)
    firearm_range_id = Column(Integer, ForeignKey('firearm_range.id'), nullable=True)
    time_start = Column(String(4))
    time_end = Column(String(4))
    datetime_entered = Column(TIMESTAMP(timezone=True), default=func.now())

    firearm_ends = relationship('FirearmEnd', back_populates='firearm_visit', cascade='all, delete-orphan', lazy='select')


class FirearmEnd(Base):
    __tablename__ = 'firearm_end'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firearm_visit_id = Column(
        Integer, ForeignKey('firearm_visit.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False,
        index=True
    )
    firearm_model_id = Column(Integer, ForeignKey('firearm_model.id'), nullable=True)
    firearm_cartridge_id = Column(Integer, ForeignKey('firearm_cartridge.id'), nullable=True)
    firearm_ammunition_id = Column(Integer, ForeignKey('firearm_ammunition.id'), nullable=True)
    quantity = Column(Integer)
    distance_m = Column(Float)
    firearm_target_id = Column(Integer, ForeignKey('firearm_target.id'), nullable=True)
    shots_scored = Column(Integer)
    points_of_stabilisation = Column(SmallInteger)
    firearm_sight_id = Column(Integer, ForeignKey('firearm_sight.id'), nullable=True)
    stance = Column(String(30))

    firearm_visit = relationship(FirearmVisit, foreign_keys=firearm_visit_id, back_populates='firearm_ends', cascade='all')
    firearm_shots = relationship('FirearmShot', back_populates='firearm_end', cascade='all, delete-orphan', lazy='select')


class FirearmShot(Base):
    __tablename__ = 'firearm_shot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firearm_end_id = Column(
        Integer, ForeignKey('firearm_end.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False,
        index=True
    )
    score = Column(Integer, nullable=False)
    is_x = Column(Boolean)
    num_shots = Column(Integer, nullable=False)

    firearm_end = relationship(FirearmEnd, foreign_keys=firearm_end_id, back_populates='firearm_shots', cascade='all')
