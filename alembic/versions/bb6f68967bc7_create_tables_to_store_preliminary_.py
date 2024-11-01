"""Create tables to store preliminary questions

Revision ID: bb6f68967bc7
Revises:
Create Date: 2024-10-28 01:56:33.772801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bb6f68967bc7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('polygons',
        sa.Column('polygon_id', sa.Integer(), nullable=False),
        sa.Column('polygon_geometry', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint('polygon_id')
    )
    op.create_index(op.f('ix_polygons_polygon_id'), 'polygons', ['polygon_id'], unique=False)

    op.create_table('metric_polygons',
        sa.Column('metric_polygon_id', sa.Integer(), nullable=False),
        sa.Column('polygon_id', sa.Integer(), nullable=False),
        sa.Column('metric_name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['polygon_id'], ['polygons.polygon_id'], ),
        sa.PrimaryKeyConstraint('metric_polygon_id')
    )
    op.create_index(op.f('ix_metric_polygons_metric_polygon_id'), 'metric_polygons', ['metric_polygon_id'], unique=False)

    op.create_table('precalculated_areas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('area_id', sa.String(), nullable=False),
        sa.Column('area_type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('polygon_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['polygon_id'], ['polygons.polygon_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_precalculated_areas_id'), 'precalculated_areas', ['id'], unique=False)

    op.create_table('metric_polygon_items',
        sa.Column('raster_id', sa.Integer(), nullable=False),
        sa.Column('metric_polygons_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.String(length=100), nullable=False),
        sa.Column('raster_data', geoalchemy2.types.Raster(from_text='raster', name='raster'), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(['metric_polygons_id'], ['metric_polygons.metric_polygon_id'], ),
        sa.PrimaryKeyConstraint('raster_id')
    )
    op.create_index(op.f('ix_metric_polygon_items_raster_id'), 'metric_polygon_items', ['raster_id'], unique=False)

    conn = op.get_bind()
    inspector = inspect(conn)
    indices = [index['name'] for index in inspector.get_indexes('metric_polygon_items')]

    if 'idx_metric_polygon_items_raster_data' not in indices:
        op.create_index(
            'idx_metric_polygon_items_raster_data',
            'metric_polygon_items',
            [sa.text('ST_ConvexHull(raster_data)')],
            unique=False,
            postgresql_using='gist'
        )


def downgrade() -> None:
    op.drop_index(op.f('ix_metric_polygon_items_raster_id'), table_name='metric_polygon_items')
    op.drop_index('idx_metric_polygon_items_raster_data', table_name='metric_polygon_items', postgresql_using='gist')
    op.drop_table('metric_polygon_items')
    op.drop_index(op.f('ix_precalculated_areas_id'), table_name='precalculated_areas')
    op.drop_table('precalculated_areas')
    op.drop_index(op.f('ix_metric_polygons_metric_polygon_id'), table_name='metric_polygons')
    op.drop_table('metric_polygons')
    op.drop_index(op.f('ix_polygons_polygon_id'), table_name='polygons')
    op.drop_table('polygons')
