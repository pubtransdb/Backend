"""
Create transport tables.

Revision ID: 8af04e2ba4bb
Revises: None
Create Date: 2022-10-21 01:54:14.601312+00:00
"""

import sqlalchemy as sa
from alembic import op


revision = "8af04e2ba4bb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "city",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("slug", sa.String(length=20), nullable=False),
        sa.Column("full_name", sa.String(length=60), nullable=False),
        sa.CheckConstraint("CAST(id AS char(1)) = '1'", name="id_startswith_type_prefix"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "company",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=60), nullable=False),
        sa.CheckConstraint("CAST(id AS char(1)) = '2'", name="id_startswith_type_prefix"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "city_company",
        sa.Column("city_id", sa.Uuid(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("company_slug", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["city_id"], ["city.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("city_id", "company_id"),
        sa.UniqueConstraint("city_id", "company_slug"),
    )
    op.create_table(
        "route",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=12), nullable=False),
        sa.Column("number", sa.String(length=6), nullable=True),
        sa.Column("city_id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("CAST(id AS char(1)) = '3'", name="id_startswith_type_prefix"),
        sa.ForeignKeyConstraint(["city_id"], ["city.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "stop_area",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("city_id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("CAST(id AS char(1)) = '5'", name="id_startswith_type_prefix"),
        sa.ForeignKeyConstraint(["city_id"], ["city.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "company_route",
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("route_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["route_id"], ["route.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("company_id", "route_id"),
    )
    op.create_table(
        "stop",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("short_name", sa.String(length=60), nullable=False),
        sa.Column("stop_area_id", sa.Uuid(), nullable=False),
        sa.CheckConstraint("CAST(id AS char(1)) = '4'", name="id_startswith_type_prefix"),
        sa.ForeignKeyConstraint(["stop_area_id"], ["stop_area.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "route_stop",
        sa.Column("route_id", sa.Uuid(), nullable=False),
        sa.Column("stop_id", sa.Uuid(), nullable=False),
        sa.Column("leg_index", sa.SmallInteger(), nullable=False),
        sa.Column("leg_distance", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["route_id"], ["route.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["stop_id"], ["stop.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("route_id", "stop_id"),
        sa.UniqueConstraint("route_id", "stop_id", "leg_index", "leg_distance"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("route_stop")
    op.drop_table("stop")
    op.drop_table("company_route")
    op.drop_table("stop_area")
    op.drop_table("route")
    op.drop_table("city_company")
    op.drop_table("company")
    op.drop_table("city")
    # ### end Alembic commands ###
