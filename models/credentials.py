from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSONB

from models import Base


class Credentials(Base):
    __tablename__ = 'credentials'
    name = Column(String, primary_key=True)
    login = Column(String)
    password = Column(String)
    website = Column(String)
    category = Column(String)  # one of: web, credit_card, id, email, bank
    importance = Column(Integer, index=True)
    extra_info = Column(JSONB)
    last_updated = Column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now(), server_default=func.now(),
        server_onupdate=func.now()
    )
