from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Polygon(Base):
    __tablename__ = "polygons"

    polygon_id = Column(Integer, primary_key=True, index=True)
    polygon_geometry = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    metrics = relationship("MetricPolygon", back_populates="polygon")
