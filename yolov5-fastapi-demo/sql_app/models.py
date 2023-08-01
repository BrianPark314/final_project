from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Info(Base):
    __tablename__ = "info"

    index = Column(Integer, primary_key=True, index=True)
    drug_N = Column(Text)
    dl_name = Column(Text)

    # warnings = relationship("Warning", back_populates="info")


class Warning(Base):
    __tablename__ = "warning"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    #info = relationship("Info", back_populates="warnings")