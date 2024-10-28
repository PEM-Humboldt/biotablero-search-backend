from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class PrecalculatedArea(Base):
    __tablename__ = 'precalculated_areas'

    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(String, nullable=False)
    area_type = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    polygon_id = Column(Integer, ForeignKey('polygons.polygon_id'), nullable=False)

    polygon = relationship('Polygon')
