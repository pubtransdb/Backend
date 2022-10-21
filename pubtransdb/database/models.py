from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
    relationship,
)

from .utils import IDTypePrefixConstraint, TypedUUIDFactory, convert_table_name_char


class Base(MappedAsDataclass, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        camel_case = cls.__name__
        snake_case = "".join(map(convert_table_name_char, camel_case))
        snake_case = snake_case.lstrip("_")
        return snake_case


class City(Base, kw_only=True):
    __table_args__ = (IDTypePrefixConstraint("1"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=TypedUUIDFactory("1"))
    slug: Mapped[str] = mapped_column(String(20), unique=True)
    full_name: Mapped[str] = mapped_column(String(60))

    company_edges: Mapped[list[CityCompany]] = relationship(
        back_populates="city", default_factory=list
    )
    routes: Mapped[list[Route]] = relationship(back_populates="city", default_factory=list)
    stop_areas: Mapped[list[StopArea]] = relationship(back_populates="city", default_factory=list)


class Company(Base, kw_only=True):
    __table_args__ = (IDTypePrefixConstraint("2"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=TypedUUIDFactory("2"))
    full_name: Mapped[str] = mapped_column(String(60))

    city_edges: Mapped[list[CityCompany]] = relationship(
        back_populates="company", default_factory=list
    )
    route_edges: Mapped[list[CompanyRoute]] = relationship(
        back_populates="company", default_factory=list
    )


class CityCompany(Base, kw_only=True):
    __table_args__ = (UniqueConstraint("city_id", "company_slug"),)

    city_id: Mapped[UUID] = mapped_column(
        ForeignKey("city.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    city: Mapped[City] = relationship(back_populates="company_edges", init=False)
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
        primary_key=True,
    )
    company: Mapped[Company] = relationship(back_populates="city_edges", init=False)

    company_slug: Mapped[str] = mapped_column(String(20))


class Route(Base, kw_only=True):
    __table_args__ = (IDTypePrefixConstraint("3"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=TypedUUIDFactory("3"))
    name: Mapped[str] = mapped_column(String(12))
    number: Mapped[str | None] = mapped_column(String(6))

    city_id: Mapped[UUID] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    city: Mapped[City] = relationship(back_populates="routes", init=False)

    company_edges: Mapped[list[CompanyRoute]] = relationship(
        back_populates="route", default_factory=list
    )
    stop_edges: Mapped[list[RouteStop]] = relationship(back_populates="route", default_factory=list)


class CompanyRoute(Base, kw_only=True):
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), primary_key=True
    )
    company: Mapped[Company] = relationship(back_populates="route_edges", init=False)
    route_id: Mapped[UUID] = mapped_column(
        ForeignKey("route.id", ondelete="CASCADE"), primary_key=True
    )
    route: Mapped[Route] = relationship(back_populates="company_edges", init=False)


class Stop(Base, kw_only=True):
    __table_args__ = (IDTypePrefixConstraint("4"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=TypedUUIDFactory("4"))
    full_name: Mapped[str] = mapped_column(String(100))
    short_name: Mapped[str] = mapped_column(String(60))

    stop_area_id: Mapped[UUID] = mapped_column(ForeignKey("stop_area.id", ondelete="CASCADE"))
    stop_area: Mapped[StopArea] = relationship(back_populates="stops", init=False)

    route_edges: Mapped[list[RouteStop]] = relationship(back_populates="stop", default_factory=list)


class StopArea(Base, kw_only=True):
    __table_args__ = (IDTypePrefixConstraint("5"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=TypedUUIDFactory("5"))

    city_id: Mapped[UUID] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    city: Mapped[City] = relationship(back_populates="stop_areas", init=False)

    stops: Mapped[list[Stop]] = relationship(back_populates="stop_area", default_factory=list)


class RouteStop(Base, kw_only=True):
    __table_args__ = (UniqueConstraint("route_id", "stop_id", "leg_index", "leg_distance"),)

    route_id: Mapped[UUID] = mapped_column(
        ForeignKey("route.id", ondelete="CASCADE"), primary_key=True
    )
    route: Mapped[Route] = relationship(back_populates="stop_edges", init=False)
    stop_id: Mapped[UUID] = mapped_column(
        ForeignKey("stop.id", ondelete="RESTRICT"), primary_key=True
    )
    stop: Mapped[Stop] = relationship(back_populates="route_edges", init=False)

    leg_index: Mapped[int] = mapped_column(SmallInteger(), CheckConstraint("leg_index >= 0"))
    leg_distance: Mapped[int] = mapped_column(CheckConstraint("leg_distance >= 0"))
