from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from .database import Base


class Info(Base):
    __tablename__ = "info"

    index = Column(Integer, primary_key=True, index=True)
    drug_N = Column(Text)
    dl_name = Column(Text)
    dl_material = Column(Text)
    effects = Column(Text)
    instructions = Column(Text)
    caution = Column(Text)
    caution_food = Column(Text)
    side_effects = Column(Text)
    di_edi_code = Column(Text)
    

    # warnings = relationship("Warning", back_populates="info")


class Warning(Base):
    __tablename__ = "warning"

    index = Column(Integer, primary_key=True, index=True)
    reference_code = Column(Integer)
    code_matches = Column(Text)
    info = Column(Text)

    #info = relationship("Info", back_populates="warnings")