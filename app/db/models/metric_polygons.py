from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MetricPolygon(Base):
    __tablename__ = 'metric_polygons'

    metric_polygon_id = Column(Integer, primary_key=True, index=True)
    polygon_id = Column(Integer, ForeignKey('polygons.polygon_id'), nullable=False)
    metric_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    values = Column(JSONB)

    polygon = relationship('Polygon', back_populates='metrics')
    items = relationship('MetricPolygonItem', back_populates='metric_polygon')
