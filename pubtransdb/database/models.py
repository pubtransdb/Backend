from __future__ import annotations

from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship

from .utils import IDTypePrefixConstraint, convert_table_name_char


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        camel_case = cls.__name__
        snake_case = "".join(map(convert_table_name_char, camel_case))
        snake_case = snake_case.lstrip("_")
        return snake_case


class City(Base):
    __table_args__ = (IDTypePrefixConstraint("1"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(20), unique=True)
    full_name: Mapped[str] = mapped_column(String(60))

    company_edges: Mapped[list[CityCompany]] = relationship(back_populates="city")
    routes: Mapped[list[Route]] = relationship(back_populates="city")
    stop_areas: Mapped[list[StopArea]] = relationship(back_populates="city")


class Company(Base):
    __table_args__ = (IDTypePrefixConstraint("2"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(60))

    city_edges: Mapped[list[CityCompany]] = relationship(back_populates="company")
    route_edges: Mapped[list[CompanyRoute]] = relationship(back_populates="company")


class CityCompany(Base):
    __table_args__ = (UniqueConstraint("city_id", "company_slug"),)

    city_id: Mapped[UUID] = mapped_column(
        ForeignKey("city.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    city: Mapped[City] = relationship(back_populates="company_edges")
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"),
        primary_key=True,
    )
    company: Mapped[Company] = relationship(back_populates="city_edges")

    company_slug: Mapped[str] = mapped_column(String(20))


class Route(Base):
    __table_args__ = (IDTypePrefixConstraint("3"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(12))
    number: Mapped[str | None] = mapped_column(String(6))

    city_id: Mapped[UUID] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    city: Mapped[City] = relationship(back_populates="routes")

    company_edges: Mapped[list[CompanyRoute]] = relationship(back_populates="route")
    stop_edges: Mapped[list[RouteStop]] = relationship(back_populates="route")


class CompanyRoute(Base):
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), primary_key=True
    )
    company: Mapped[Company] = relationship(back_populates="route_edges")
    route_id: Mapped[UUID] = mapped_column(
        ForeignKey("route.id", ondelete="CASCADE"), primary_key=True
    )
    route: Mapped[Route] = relationship(back_populates="company_edges")


class Stop(Base):
    __table_args__ = (IDTypePrefixConstraint("4"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    short_name: Mapped[str] = mapped_column(String(60))

    stop_area_id: Mapped[UUID] = mapped_column(ForeignKey("stop_area.id", ondelete="CASCADE"))
    stop_area: Mapped[StopArea] = relationship(back_populates="stops")

    route_edges: Mapped[list[RouteStop]] = relationship(back_populates="stop")


class StopArea(Base):
    __table_args__ = (IDTypePrefixConstraint("5"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)

    city_id: Mapped[UUID] = mapped_column(ForeignKey("city.id", ondelete="CASCADE"))
    city: Mapped[City] = relationship(back_populates="stop_areas")

    stops: Mapped[list[Stop]] = relationship(back_populates="stop_area")


class RouteStop(Base):
    __table_args__ = (UniqueConstraint("route_id", "stop_id", "leg_index", "leg_distance"),)

    route_id: Mapped[UUID] = mapped_column(
        ForeignKey("route.id", ondelete="CASCADE"), primary_key=True
    )
    route: Mapped[Route] = relationship(back_populates="stop_edges")
    stop_id: Mapped[UUID] = mapped_column(
        ForeignKey("stop.id", ondelete="RESTRICT"), primary_key=True
    )
    stop: Mapped[Stop] = relationship(back_populates="route_edges")

    leg_index: Mapped[int] = mapped_column(SmallInteger(), CheckConstraint("leg_index >= 0"))
    leg_distance: Mapped[int] = mapped_column(CheckConstraint("leg_distance >= 0"))
