from geoalchemy2 import Raster
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class MetricPolygonItem(Base):
    __tablename__ = "metric_polygon_items"

    raster_id = Column(Integer, primary_key=True, index=True)
    metric_polygons_id = Column(
        Integer,
        ForeignKey("metric_polygons.metric_polygon_id"),
        nullable=False,
    )
    item_id = Column(String(100), nullable=False)
    raster_data = Column(Raster)
    created_at = Column(TIMESTAMP, nullable=False)

    metric_polygon = relationship("MetricPolygon", back_populates="items")
